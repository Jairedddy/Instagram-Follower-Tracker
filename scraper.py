import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import parse_count, update_progress_bar


MAX_SCROLL_ATTEMPTS = 2000
SCROLL_PAUSE = 0.3
WEBDRIVER_WAIT = 15
THRESHOLD_MAX_ACCOUNTS = 750


def get_profile_counts(driver, profile_username):
    profile_url = f"https://www.instagram.com/{profile_username}/"
    driver.get(profile_url)
    try:
        WebDriverWait(driver, WEBDRIVER_WAIT).until(
            EC.presence_of_element_located((By.XPATH, f"//header//h2[contains(., '{profile_username}')] | //header//h1"))
        )
    except TimeoutException:
        try:
            WebDriverWait(driver, WEBDRIVER_WAIT).until(
                EC.presence_of_element_located((By.TAG_NAME, "header"))
            )
        except TimeoutException:
            print("Profile did not load correctly.")
            return None, None
    
    followers_count = None
    following_count = None
    
    try:
        links = driver.find_elements(By.XPATH, "//header//a")
        for link in links:
            href = link.get_attribute("href") or ""
            text = link.text.strip()
            
            if "/followers/" in href:
                count_text = re.search(r'[\d.,KMkm]+', text)
                if count_text:
                    followers_count = parse_count(count_text.group())
            elif "/following/" in href:
                count_text = re.search(r'[\d.,KMkm]+', text)
                if count_text:
                    following_count = parse_count(count_text.group())
    except Exception as e:
        print(f"Error extracting counts: {e}")
    
    return followers_count, following_count


def open_profile(driver, profile_username):
    profile_url = f"https://www.instagram.com/{profile_username}/"
    driver.get(profile_url)
    try:
        WebDriverWait(driver, WEBDRIVER_WAIT).until(
            EC.presence_of_element_located((By.XPATH, f"//header//h2[contains(., '{profile_username}')] | //header//h1"))
        )
    except TimeoutException:
        try:
            WebDriverWait(driver, WEBDRIVER_WAIT).until(
                EC.presence_of_element_located((By.TAG_NAME, "header"))
            )
        except TimeoutException:
            print("Profile did not load correctly. Continuing anyway.")
            pass


def find_scrollable_container(driver):
    try:
        modal = driver.find_element(By.XPATH, "//div[@role='dialog']")
        candidates = modal.find_elements(By.XPATH, ".//div | .//ul")
        scroll_box = None
        best_scroll_diff = 0
        for c in candidates:
            style = c.get_attribute("style") or ""
            if ("overflow" in style or "max-height" in style or "overflow-y" in style or 
                "overflow-y: auto" in style.lower() or "overflow-y:scroll" in style.lower()):
                try:
                    scroll_height = driver.execute_script("return arguments[0].scrollHeight", c)
                    client_height = driver.execute_script("return arguments[0].clientHeight", c)
                    if scroll_height > client_height + 10:
                        scroll_box = c
                        break
                except Exception:
                    continue
        if scroll_box is None:
            for c in candidates:
                try:
                    scroll_height = driver.execute_script("return arguments[0].scrollHeight", c)
                    client_height = driver.execute_script("return arguments[0].clientHeight", c)
                    scroll_diff = scroll_height - client_height
                    if scroll_diff > best_scroll_diff and scroll_diff > 100:
                        best_scroll_diff = scroll_diff
                        scroll_box = c
                except Exception:
                    continue
        if scroll_box is None:
            try:
                list_elem = modal.find_element(By.XPATH, ".//ul | .//div[@role='list']")
                scroll_height = driver.execute_script("return arguments[0].scrollHeight", list_elem)
                client_height = driver.execute_script("return arguments[0].clientHeight", list_elem)
                if scroll_height > client_height + 10:
                    scroll_box = list_elem
            except Exception:
                pass
        
        if scroll_box is None:
            scroll_box = modal
        return scroll_box, modal
    except Exception:
        return None, None


def extract_list_from_modal(driver, which="followers", total_count=None):
    try:
        link = WebDriverWait(driver, WEBDRIVER_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '/{which}/')]"))
        )
        link.click()
    except TimeoutException:
        try:
            links = driver.find_elements(By.XPATH, "//header//a")
            target = None
            for a in links:
                href = a.get_attribute("href") or ""
                if href.endswith(f"/{which}/") or ("/" + which + "/") in href:
                    target = a
                    break
            if target:
                target.click()
            else:
                raise
        except Exception:
            print(f"Failed to open {which} modal.")
            return set()
    time.sleep(2)
    
    try:
        modal = WebDriverWait(driver, WEBDRIVER_WAIT).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[@style or @class]"))
        )
    except TimeoutException:
        try:
            modal = driver.find_element(By.XPATH, "//div[@role='dialog']")
        except Exception:
            print("Could not find dialog for", which)
            return set()
    
    usernames = []
    no_new_accounts_count = 0
    max_no_new_accounts = 4
    last_scroll_height = 0
    stable_height_count = 0
    
    scroll_box_refresh, modal_refresh = find_scrollable_container(driver)
    if modal_refresh is None or scroll_box_refresh is None:
        print(f"Could not find scroll container for {which} modal.")
        return set()
    
    try:
        last_scroll_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box_refresh)
    except Exception:
        last_scroll_height = 0
    
    iteration = 0
    while iteration < MAX_SCROLL_ATTEMPTS:
        iteration += 1
        prev_count = len(usernames)
        
        try:
            try:
                current_scroll_top = driver.execute_script("return arguments[0].scrollTop", scroll_box_refresh)
            except Exception:
                scroll_box_refresh, modal_refresh = find_scrollable_container(driver)
                if modal_refresh is None or scroll_box_refresh is None:
                    break
                current_scroll_top = driver.execute_script("return arguments[0].scrollTop", scroll_box_refresh)
            
            current_scroll_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box_refresh)
            client_height = driver.execute_script("return arguments[0].clientHeight", scroll_box_refresh)
            anchors = scroll_box_refresh.find_elements(By.XPATH, ".//a")
            hrefs = []
            for a in anchors:
                try:
                    href = a.get_attribute("href") or ""
                    if href:
                        hrefs.append(href)
                except Exception:
                    continue
            for href in hrefs:
                m = re.match(r"https?://(www\.)?instagram\.com/([^/?#]+)/?", href)
                if m:
                    uname = m.group(2).strip()
                    if uname and uname not in usernames:
                        usernames.append(uname)
            new_count = len(usernames)
            update_progress_bar(new_count, total_count, scroll_count=iteration)
            if new_count == prev_count:
                no_new_accounts_count += 1
            else:
                no_new_accounts_count = 0
            if current_scroll_height == last_scroll_height:
                stable_height_count += 1
            else:
                stable_height_count = 0
                last_scroll_height = current_scroll_height
            at_bottom = (current_scroll_top + client_height >= current_scroll_height - 5)
            if at_bottom and no_new_accounts_count >= max_no_new_accounts and stable_height_count >= 10:
                try:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box_refresh)
                    time.sleep(SCROLL_PAUSE * 2)
                    final_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box_refresh)
                    if final_height > current_scroll_height:
                        last_scroll_height = final_height
                        stable_height_count = 0
                    else:
                        break
                except Exception:
                    break
            try:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box_refresh)
                time.sleep(SCROLL_PAUSE)
            except Exception:
                pass
            
        except Exception:
            no_new_accounts_count += 1
            if no_new_accounts_count >= max_no_new_accounts:
                break
            time.sleep(SCROLL_PAUSE)
            continue
    print()
    try:
        close_btn = driver.find_element(By.XPATH, "//div[@role='dialog']//button[contains(., 'Close') or contains(., 'Close)]")
        try:
            close_btn.click()
        except Exception:
            pass
    except Exception:
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
        except Exception:
            pass
    
    return set(usernames)