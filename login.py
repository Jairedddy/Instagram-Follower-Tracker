import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import input_to_browser_real_time


WEBDRIVER_WAIT = 15


def safe_click(driver, by, selector, timeout=WEBDRIVER_WAIT):
    try:
        el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, selector)))
        el.click()
        return True
    except Exception:
        return False

def check_login_errors(driver):
    error_selectors = [
        "//p[contains(@id, 'slfError')]",
        "//div[contains(@id, 'slfError')]",
        "//span[contains(@id, 'slfError')]",
        "//p[contains(., 'incorrect')]",
        "//p[contains(., 'wrong')]",
        "//p[contains(., 'invalid')]",
        "//p[contains(., 'try again')]",
        "//div[contains(., 'incorrect')]",
        "//div[contains(., 'wrong')]",
        "//div[contains(., 'invalid')]",
        "//span[contains(., 'incorrect')]",
        "//span[contains(., 'wrong')]",
        "//span[contains(., 'invalid')]",
    ]
    
    for selector in error_selectors:
        try:
            error_elements = driver.find_elements(By.XPATH, selector)
            for error_el in error_elements:
                error_text = error_el.text.strip().lower()
                if error_text and any(keyword in error_text for keyword in ['incorrect', 'wrong', 'invalid', 'try again', 'error', 'sorry']):
                    return True, error_el.text.strip()
        except Exception:
            continue
    
    return False, None


def check_2fa_errors(driver):
    error_selectors = [
        "//p[contains(., 'code') and (contains(., 'incorrect') or contains(., 'wrong') or contains(., 'invalid'))]",
        "//div[contains(., 'code') and (contains(., 'incorrect') or contains(., 'wrong') or contains(., 'invalid'))]",
        "//span[contains(., 'code') and (contains(., 'incorrect') or contains(., 'wrong') or contains(., 'invalid'))]",
        "//p[contains(., 'verification') and (contains(., 'incorrect') or contains(., 'wrong') or contains(., 'invalid'))]",
        "//div[contains(., 'verification') and (contains(., 'incorrect') or contains(., 'wrong') or contains(., 'invalid'))]",
        "//p[contains(., 'try again')]",
        "//div[contains(., 'try again')]",
    ]
    
    for selector in error_selectors:
        try:
            error_elements = driver.find_elements(By.XPATH, selector)
            for error_el in error_elements:
                error_text = error_el.text.strip().lower()
                if error_text and any(keyword in error_text for keyword in ['code', 'verification', 'incorrect', 'wrong', 'invalid', 'try again']):
                    return True, error_el.text.strip()
        except Exception:
            continue
    
    return False, None


def login_instagram(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    wait = WebDriverWait(driver, WEBDRIVER_WAIT)
    
    try:
        user_el = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        pass_el = driver.find_element(By.NAME, "password")
    except Exception:
        print("❌ Error: Login page did not load properly. Exiting.")
        driver.quit()
        raise ValueError("Login page failed to load")
    user_el.clear()
    pass_el.clear()
    
    username = input_to_browser_real_time(driver, user_el, "Your instagram username: ", is_password=False)
    
    if not username.strip():
        print("❌ Error: Username cannot be empty.")
        driver.quit()
        raise ValueError("Empty username provided")
    password = input_to_browser_real_time(driver, pass_el, "Your instagram password: ", is_password=True)
    if not password.strip():
        print("❌ Error: Password cannot be empty.")
        driver.quit()
        raise ValueError("Empty password provided")
    try:
        btn = driver.find_element(By.XPATH, "//button[@type='submit'][not(@disabled)]")
        btn.click()
    except Exception:
        try:
            safe_click(driver, By.XPATH, "//button[contains(., 'Log In')]")
        except Exception:
            print("❌ Error: Could not click login button.")
            driver.quit()
            raise ValueError("Login button not found or not clickable")
    time.sleep(3)
    has_error, error_message = check_login_errors(driver)
    if has_error:
        print(f"\n❌ Login Error: {error_message}")
        print("This could be due to:")
        print("  - Incorrect username")
        print("  - Incorrect password")
        print("  - Account temporarily locked")
        driver.quit()
        raise ValueError(f"Login failed: {error_message}")
    twofa_required = False
    twofa_input = None
    
    try:
        twofa_selectors = [
            (By.NAME, "verificationCode"),
            (By.NAME, "verification_code"),
            (By.XPATH, "//input[contains(@aria-label,'authentication code') or contains(@aria-label, 'security code') or contains(@placeholder, 'Enter 6-digit')]"),
            (By.XPATH, "//input[contains(@id, 'verification') or contains(@id, 'security')]"),
            (By.XPATH, "//input[@type='tel' or @inputmode='numeric']"),
        ]
        
        for by, sel in twofa_selectors:
            try:
                el = driver.find_element(by, sel)
                twofa_required = True
                twofa_input = el
                break
            except Exception:
                continue
    except Exception:
        pass
    
    if twofa_required and twofa_input:
        otp = input_to_browser_real_time(driver, twofa_input, "Two-factor Authentication required. Enter OTP code from Instagram: ", is_password=False)
        
        if not otp.strip():
            print("❌ Error: OTP code cannot be empty.")
            driver.quit()
            raise ValueError("Empty OTP code provided")
        try:
            twofa_input.send_keys("\n")
        except Exception:
            try:
                submit_btn = driver.find_element(By.XPATH, "//button[@type='submit'] | //button[contains(., 'Confirm')] | //button[contains(., 'Verify')]")
                submit_btn.click()
            except Exception:
                pass
        time.sleep(3)
        has_2fa_error, error_message = check_2fa_errors(driver)
        if has_2fa_error:
            print(f"\n❌ 2FA Error: {error_message}")
            print("The OTP code you entered is incorrect or has expired.")
            print("Please try again with a fresh OTP code.")
            driver.quit()
            raise ValueError(f"2FA failed: {error_message}")
        
        has_error, error_message = check_login_errors(driver)
        if has_error:
            print(f"\n❌ Login Error after 2FA: {error_message}")
            driver.quit()
            raise ValueError(f"Login failed after 2FA: {error_message}")
    
    time.sleep(2)
    has_error, error_message = check_login_errors(driver)
    if has_error:
        print(f"\n❌ Login Error: {error_message}")
        driver.quit()
        raise ValueError(f"Login failed: {error_message}")
    try:
        logged_in_indicators = [
            "//a[contains(@href, '/direct/')]",
            "//a[contains(@href, '/explore/')]",
            "//a[contains(@href, '/accounts/')]",
            "//nav",
        ]
        
        logged_in = False
        for indicator in logged_in_indicators:
            try:
                driver.find_element(By.XPATH, indicator)
                logged_in = True
                break
            except Exception:
                continue
        
        if not logged_in:
            if "accounts/login" in driver.current_url:
                print("❌ Error: Still on login page. Login may have failed.")
                driver.quit()
                raise ValueError("Login verification failed - still on login page")
    except Exception:
        pass
    try:
        ok_buttons = driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ok')]")
        if ok_buttons:
            ok_buttons[0].click()
            time.sleep(1)
    except Exception:
        pass
    try:
        not_now_buttons = driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'not now')]")
        if not_now_buttons:
            not_now_buttons[0].click()
            time.sleep(1)
    except Exception:
        pass
    return username.strip()