"""
Instagram Bot for identifying accounts that don't follow back.
Uses Selenium WebDriver to automate browser interactions with Instagram.
"""

import time
from typing import List, Set, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException,
    WebDriverException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager


class InstagramBot:
    """Main bot class for Instagram automation."""
    
    def __init__(self, headless: bool = False):
        """
        Initialize the Instagram bot.
        
        Args:
            headless: If True, run browser in headless mode (no GUI)
        """
        self.driver = None
        self.is_logged_in = False
        self.username = None
        self.headless = headless
        self._setup_driver()
    
    def _setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
        except WebDriverException as e:
            raise Exception(f"Failed to initialize browser: {str(e)}. Make sure Chrome is installed.")
        except Exception as e:
            raise Exception(f"Unexpected error setting up browser: {str(e)}")
    
    def login(self, username: str, password: str) -> bool:
        """
        Log into Instagram with username and password.
        Handles 2FA if enabled.
        
        Args:
            username: Instagram username
            password: Instagram password
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            print("[DEBUG] Starting login process...")
            print(f"[DEBUG] Username: {username}")
            print(f"[DEBUG] Password length: {len(password)} characters")
            
            print("\n[STEP 1/6] Navigating to Instagram login page...")
            try:
                login_url = "https://www.instagram.com/accounts/login/"
                print(f"[DEBUG] Loading URL: {login_url}")
                self.driver.get(login_url)
                print(f"[DEBUG] Current URL after navigation: {self.driver.current_url}")
                time.sleep(2)
                print(f"[DEBUG] Page title: {self.driver.title}")
            except WebDriverException as e:
                print(f"\n✗ Network error: Could not connect to Instagram. {str(e)}")
                print("Please check your internet connection and try again.")
                return False
            
            # Wait for login form to load
            print("\n[STEP 2/6] Waiting for login form to load...")
            wait = WebDriverWait(self.driver, 15)
            
            # Find and fill username
            print("[STEP 3/6] Looking for username input field...")
            try:
                print("[DEBUG] Searching for username/email input field...")
                print("[DEBUG] Waiting up to 15 seconds for username field...")
                
                # Try multiple selectors (Instagram uses 'username', Facebook login uses 'email')
                username_input = None
                selectors_to_try = [
                    (By.NAME, "username"),
                    (By.NAME, "email"),  # Facebook-style login
                    (By.XPATH, "//input[@name='username']"),
                    (By.XPATH, "//input[@name='email']"),  # Facebook-style login
                    (By.XPATH, "//input[@type='text' and contains(@aria-label, 'Phone number')]"),
                    (By.XPATH, "//input[@type='text' and contains(@aria-label, 'Username')]"),
                    (By.XPATH, "//input[@type='text' and contains(@aria-label, 'Email')]"),
                    (By.XPATH, "//input[@type='text' and contains(@placeholder, 'Phone number')]"),
                    (By.XPATH, "//input[@type='text' and contains(@placeholder, 'Username')]"),
                ]
                
                for selector_type, selector_value in selectors_to_try:
                    try:
                        print(f"[DEBUG] Trying selector: {selector_type}={selector_value}")
                        username_input = wait.until(
                            EC.presence_of_element_located((selector_type, selector_value))
                        )
                        print(f"[DEBUG] Username input field found with selector: {selector_type}={selector_value}")
                        break
                    except TimeoutException:
                        continue
                
                if not username_input:
                    raise TimeoutException("Could not find username input field with any selector")
                
                print("[DEBUG] Username input field found!")
                print(f"[DEBUG] Username input is displayed: {username_input.is_displayed()}")
                print(f"[DEBUG] Username input is enabled: {username_input.is_enabled()}")
                print(f"[DEBUG] Username input location: {username_input.location}")
                print(f"[DEBUG] Username input size: {username_input.size}")
                
                username_input.clear()
                print(f"[DEBUG] Entering username: {username}")
                username_input.send_keys(username)
                time.sleep(1)
                
                # Verify username was entered
                entered_value = username_input.get_attribute('value')
                print(f"[DEBUG] Username field value after entry: {entered_value}")
                print("[DEBUG] Username entered successfully")
            except TimeoutException as e:
                print("[DEBUG] Timeout waiting for username field")
                print(f"[DEBUG] Current URL: {self.driver.current_url}")
                print(f"[DEBUG] Page title: {self.driver.title}")
                print("[DEBUG] Checking for available input fields on page...")
                try:
                    all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    print(f"[DEBUG] Found {len(all_inputs)} input elements on page")
                    for i, inp in enumerate(all_inputs[:5]):  # Show first 5
                        print(f"[DEBUG]   Input {i+1}: name='{inp.get_attribute('name')}', type='{inp.get_attribute('type')}', id='{inp.get_attribute('id')}'")
                except:
                    pass
                print("[DEBUG] Page source snippet (first 1000 chars):")
                print(self.driver.page_source[:1000])
                raise
            
            # Find and fill password
            print("\n[STEP 4/6] Looking for password input field...")
            try:
                print("[DEBUG] Searching for password input field...")
                print("[DEBUG] Waiting up to 15 seconds for password field...")
                
                # Try multiple selectors (Instagram uses 'password', Facebook login uses 'pass')
                password_input = None
                password_selectors_to_try = [
                    (By.NAME, "password"),
                    (By.NAME, "pass"),  # Facebook-style login
                    (By.XPATH, "//input[@name='password']"),
                    (By.XPATH, "//input[@name='pass']"),  # Facebook-style login
                    (By.XPATH, "//input[@type='password']"),
                ]
                
                for selector_type, selector_value in password_selectors_to_try:
                    try:
                        print(f"[DEBUG] Trying password selector: {selector_type}={selector_value}")
                        password_input = wait.until(
                            EC.presence_of_element_located((selector_type, selector_value))
                        )
                        print(f"[DEBUG] Password input field found with selector: {selector_type}={selector_value}")
                        break
                    except TimeoutException:
                        continue
                
                if not password_input:
                    raise TimeoutException("Could not find password input field with any selector")
                
                print("[DEBUG] Password input field found!")
                print(f"[DEBUG] Password input is displayed: {password_input.is_displayed()}")
                print(f"[DEBUG] Password input is enabled: {password_input.is_enabled()}")
                
                password_input.clear()
                print("[DEBUG] Entering password (masked)")
                password_input.send_keys(password)
                time.sleep(1)
                print("[DEBUG] Password entered successfully")
            except TimeoutException:
                print("[DEBUG] Timeout waiting for password field")
                print(f"[DEBUG] Current URL: {self.driver.current_url}")
                raise
            
            # Submit login form - Use Enter key method (most reliable for Facebook-style forms)
            print("\n[STEP 5/6] Submitting login form...")
            print("[DEBUG] Using Enter key method to submit form (most reliable)")
            try:
                password_input.send_keys(Keys.RETURN)
                print("[DEBUG] Enter key pressed on password field")
                time.sleep(3)
                print(f"[DEBUG] URL after Enter key: {self.driver.current_url}")
            except Exception as e:
                print(f"[DEBUG] Error pressing Enter: {str(e)}")
                # Fallback: Try to find and click login button
                print("[DEBUG] Fallback: Trying to find login button...")
                try:
                    login_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']"))
                    )
                    print("[DEBUG] Login button found, clicking...")
                    login_button.click()
                    time.sleep(3)
                    print(f"[DEBUG] URL after button click: {self.driver.current_url}")
                except TimeoutException:
                    print("[DEBUG] Could not find login button, Enter key method should have worked")
                    raise Exception("Failed to submit login form")
            
            # Check for 2FA prompt
            print("\n[STEP 6/6] Checking for 2FA...")
            if self._check_for_2fa():
                print("\nTwo-factor authentication detected.")
                verification_code = input("Enter your 2FA verification code: ").strip()
                if not self._handle_2fa(verification_code):
                    print("2FA verification failed.")
                    return False
            
            # Handle "Save Login Info" dialog
            print("[DEBUG] Checking for 'Save Login Info' dialog...")
            self._handle_save_login_dialog()
            
            # Check if login was successful
            print("[DEBUG] Waiting for page to load after login...")
            time.sleep(3)
            current_url = self.driver.current_url
            print(f"[DEBUG] Final URL: {current_url}")
            print(f"[DEBUG] Page title: {self.driver.title}")
            
            # Check for rate limiting or suspicious activity warnings
            print("[DEBUG] Checking page content for warnings...")
            page_source = self.driver.page_source.lower()
            if "try again later" in page_source or "suspicious activity" in page_source:
                print("\n✗ Login failed: Instagram has detected unusual activity.")
                print("Please wait a few minutes and try again, or try logging in from a browser first.")
                return False
            
            if "accounts/login" not in current_url:
                self.is_logged_in = True
                self.username = username
                print(f"\n✓ Successfully logged in as {username}!")
                print(f"[DEBUG] Login successful! Redirected to: {current_url}")
                return True
            else:
                print("[DEBUG] Still on login page, checking for error messages...")
                # Check for error messages
                try:
                    error_selectors = [
                        "//div[contains(text(), 'Sorry, your password was incorrect')]",
                        "//div[contains(text(), 'The username you entered')]",
                        "//div[contains(text(), 'incorrect')]",
                        "//p[contains(text(), 'incorrect')]",
                        "//span[contains(text(), 'incorrect')]"
                    ]
                    for selector in error_selectors:
                        try:
                            error_element = self.driver.find_element(By.XPATH, selector)
                            if error_element and error_element.is_displayed():
                                error_text = error_element.text
                                print(f"[DEBUG] Found error message: {error_text}")
                                print("\n✗ Login failed: Invalid username or password.")
                                return False
                        except NoSuchElementException:
                            continue
                    
                    # Check for any visible error indicators
                    print("[DEBUG] Checking for generic error indicators...")
                    error_indicators = self.driver.find_elements(
                        By.XPATH, 
                        "//div[contains(@class, 'error') or contains(@id, 'error')]"
                    )
                    for indicator in error_indicators:
                        if indicator.is_displayed():
                            print(f"[DEBUG] Found error indicator: {indicator.text}")
                            
                except Exception as e:
                    print(f"[DEBUG] Error while checking for error messages: {str(e)}")
                
                print("\n✗ Login failed: Unknown error. Please check your credentials and try again.")
                print(f"[DEBUG] Current URL: {current_url}")
                print("[DEBUG] Page may have changed. Check the browser window for details.")
                return False
                
        except TimeoutException as e:
            print(f"\n✗ Login failed: Timeout waiting for page elements.")
            print(f"[DEBUG] Timeout exception: {str(e)}")
            print(f"[DEBUG] Current URL: {self.driver.current_url}")
            print(f"[DEBUG] Page title: {self.driver.title}")
            print("Instagram may be loading slowly. Please try again.")
            return False
        except WebDriverException as e:
            print(f"\n✗ Login failed: Network or browser error. {str(e)}")
            print(f"[DEBUG] WebDriver exception type: {type(e).__name__}")
            return False
        except Exception as e:
            print(f"\n✗ Login failed: {str(e)}")
            print(f"[DEBUG] Exception type: {type(e).__name__}")
            import traceback
            print("[DEBUG] Full traceback:")
            traceback.print_exc()
            return False
    
    def _check_for_2fa(self) -> bool:
        """Check if 2FA verification code prompt is present."""
        try:
            # Look for common 2FA input fields
            wait = WebDriverWait(self.driver, 3)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@name='verificationCode' or @name='security_code' or contains(@aria-label, 'Security Code')]")
                )
            )
            return True
        except TimeoutException:
            return False
    
    def _handle_2fa(self, verification_code: str) -> bool:
        """Handle 2FA verification code input."""
        try:
            wait = WebDriverWait(self.driver, 10)
            # Try different possible selectors for 2FA input
            code_input_selectors = [
                "//input[@name='verificationCode']",
                "//input[@name='security_code']",
                "//input[contains(@aria-label, 'Security Code')]",
                "//input[@type='text']"
            ]
            
            code_input = None
            for selector in code_input_selectors:
                try:
                    code_input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    break
                except TimeoutException:
                    continue
            
            if not code_input:
                print("Could not find 2FA input field.")
                return False
            
            code_input.clear()
            code_input.send_keys(verification_code)
            time.sleep(1)
            
            # Find and click submit button
            submit_selectors = [
                "//button[contains(text(), 'Confirm')]",
                "//button[contains(text(), 'Verify')]",
                "//button[@type='submit']"
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.XPATH, selector)
                    if submit_button.is_displayed():
                        break
                except NoSuchElementException:
                    continue
            
            if not submit_button:
                print("Could not find submit button for 2FA.")
                return False
            
            submit_button.click()
            time.sleep(3)
            
            # Check if verification was successful
            if "accounts/login" not in self.driver.current_url:
                return True
            else:
                # Check for error message
                try:
                    error_msg = self.driver.find_element(
                        By.XPATH,
                        "//div[contains(text(), 'incorrect') or contains(text(), 'invalid')]"
                    )
                    if error_msg:
                        print("Invalid verification code. Please try again.")
                except NoSuchElementException:
                    pass
                return False
        except TimeoutException:
            print("Timeout while handling 2FA. Please try again.")
            return False
        except Exception as e:
            print(f"Error handling 2FA: {str(e)}")
            return False
    
    def _handle_save_login_dialog(self):
        """Handle 'Save Login Info' dialog that appears after login."""
        try:
            wait = WebDriverWait(self.driver, 5)
            # Look for "Not Now" or "Save Info" buttons
            not_now_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Not Now') or contains(text(), 'Not now')]")
                )
            )
            not_now_button.click()
            time.sleep(1)
            print("Handled 'Save Login Info' dialog.")
        except (TimeoutException, NoSuchElementException):
            # Dialog might not appear, which is fine
            pass
        except ElementClickInterceptedException:
            # Try alternative approach
            try:
                self.driver.execute_script("arguments[0].click();", not_now_button)
            except:
                pass
    
    def get_followers(self) -> List[str]:
        """
        Get the complete list of accounts that follow the user.
        
        Returns:
            List of usernames that follow the user
            
        Raises:
            Exception: If not logged in or extraction fails
        """
        if not self.is_logged_in:
            raise Exception("Not logged in. Please login first.")
        
        try:
            print("\nExtracting followers list...")
            followers = self._extract_user_list("followers")
            if not followers:
                raise Exception("Failed to extract followers list. Instagram may have rate-limited the request.")
            print(f"✓ Found {len(followers)} followers.")
            return followers
        except Exception as e:
            if "rate" in str(e).lower() or "limit" in str(e).lower():
                print("\n⚠ Instagram may have rate-limited your requests.")
                print("Please wait a few minutes and try again.")
            raise
    
    def get_following(self) -> List[str]:
        """
        Get the complete list of accounts that the user follows.
        
        Returns:
            List of usernames that the user follows
            
        Raises:
            Exception: If not logged in or extraction fails
        """
        if not self.is_logged_in:
            raise Exception("Not logged in. Please login first.")
        
        try:
            print("\nExtracting following list...")
            following = self._extract_user_list("following")
            if not following:
                raise Exception("Failed to extract following list. Instagram may have rate-limited the request.")
            print(f"✓ Found {len(following)} accounts you follow.")
            return following
        except Exception as e:
            if "rate" in str(e).lower() or "limit" in str(e).lower():
                print("\n⚠ Instagram may have rate-limited your requests.")
                print("Please wait a few minutes and try again.")
            raise
    
    def _extract_user_list(self, list_type: str) -> List[str]:
        """
        Extract followers or following list by scrolling and loading all users.
        
        Args:
            list_type: Either "followers" or "following"
            
        Returns:
            List of usernames
        """
        try:
            # Navigate to user's profile
            print(f"[DEBUG] Navigating to profile: https://www.instagram.com/{self.username}/")
            try:
                self.driver.get(f"https://www.instagram.com/{self.username}/")
                time.sleep(3)
                print(f"[DEBUG] Profile page loaded. Current URL: {self.driver.current_url}")
                print(f"[DEBUG] Page title: {self.driver.title}")
            except WebDriverException as e:
                print(f"[DEBUG] Network error loading profile: {str(e)}")
                raise Exception(f"Network error: Could not load profile page. {str(e)}")
            
            # Check for rate limiting or account restrictions (more specific checks)
            print("[DEBUG] Checking page content for warnings or restrictions...")
            page_source = self.driver.page_source.lower()
            page_url = self.driver.current_url.lower()
            
            # More specific checks for restrictions
            restriction_indicators = [
                "try again later",
                "rate limit",
                "too many requests"
            ]
            
            for indicator in restriction_indicators:
                if indicator in page_source:
                    print(f"[DEBUG] Found restriction indicator: {indicator}")
                    raise Exception("Instagram rate limit detected. Please wait before trying again.")
            
            # Check URL for restriction pages
            if "challenge" in page_url or "restricted" in page_url:
                print(f"[DEBUG] Restricted URL detected: {page_url}")
                raise Exception("Account may be restricted. Please check your Instagram account.")
            
            # Check for specific error messages in page
            error_messages = self.driver.find_elements(
                By.XPATH,
                "//div[contains(text(), 'restricted') or contains(text(), 'suspended') or contains(text(), 'blocked')]"
            )
            if error_messages:
                for msg in error_messages:
                    if msg.is_displayed():
                        error_text = msg.text
                        print(f"[DEBUG] Found error message on page: {error_text}")
                        if "restricted" in error_text.lower() or "suspended" in error_text.lower():
                            raise Exception("Account may be restricted. Please check your Instagram account.")
            
            print("[DEBUG] No restrictions detected, proceeding...")
            
            # Click on followers or following link
            print(f"[DEBUG] Looking for {list_type} link...")
            wait = WebDriverWait(self.driver, 15)
            if list_type == "followers":
                # Try multiple selectors for followers link
                link_selectors = [
                    f"//a[contains(@href, '/{self.username}/followers')]",
                    "//a[contains(@href, '/followers/')]",
                    "//a[contains(@href, '/followers')]",
                    f"//a[@href='/{self.username}/followers/']",
                    "//span[contains(text(), 'followers')]/parent::a",
                    "//span[contains(text(), 'follower')]/parent::a"
                ]
            else:
                # Try multiple selectors for following link
                link_selectors = [
                    f"//a[contains(@href, '/{self.username}/following')]",
                    "//a[contains(@href, '/following/')]",
                    "//a[contains(@href, '/following')]",
                    f"//a[@href='/{self.username}/following/']",
                    "//span[contains(text(), 'following')]/parent::a"
                ]
            
            link = None
            for selector in link_selectors:
                try:
                    print(f"[DEBUG] Trying {list_type} link selector: {selector}")
                    link = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    print(f"[DEBUG] Found {list_type} link!")
                    print(f"[DEBUG] Link href: {link.get_attribute('href')}")
                    print(f"[DEBUG] Link text: {link.text}")
                    break
                except TimeoutException:
                    continue
            
            if not link:
                print(f"[DEBUG] Could not find {list_type} link with any selector")
                print("[DEBUG] Checking for all links on profile page...")
                try:
                    all_links = self.driver.find_elements(By.TAG_NAME, "a")
                    print(f"[DEBUG] Found {len(all_links)} links on page")
                    for i, lnk in enumerate(all_links[:20]):  # Show first 20
                        try:
                            href = lnk.get_attribute('href') or 'N/A'
                            text = lnk.text or 'N/A'
                            if 'follow' in href.lower() or 'follow' in text.lower():
                                print(f"[DEBUG]   Link {i+1}: href='{href}', text='{text}'")
                        except:
                            pass
                except Exception as e:
                    print(f"[DEBUG] Error checking links: {str(e)}")
                raise Exception(f"Could not find {list_type} link")
            
            print(f"[DEBUG] Clicking {list_type} link...")
            link.click()
            time.sleep(3)
            print(f"[DEBUG] After clicking {list_type} link, URL: {self.driver.current_url}")
            
            # Find the dialog/modal that contains the list
            print("[DEBUG] Looking for dialog/modal containing the list...")
            dialog_xpath = "//div[@role='dialog']"
            try:
                dialog = wait.until(EC.presence_of_element_located((By.XPATH, dialog_xpath)))
                print("[DEBUG] Dialog found!")
            except TimeoutException:
                print("[DEBUG] Dialog not found with standard selector")
                print("[DEBUG] Checking page structure...")
                print(f"[DEBUG] Current URL: {self.driver.current_url}")
                print(f"[DEBUG] Page title: {self.driver.title}")
                
                # Check if we're on a different page (maybe Instagram redirected)
                if f"/{self.username}/" not in self.driver.current_url:
                    print(f"[DEBUG] Unexpected URL after clicking {list_type} link")
                    raise Exception(f"Instagram redirected to unexpected page: {self.driver.current_url}")
                
                # Try alternative dialog selectors
                alternative_dialogs = [
                    "//div[contains(@class, 'modal')]",
                    "//div[contains(@class, 'dialog')]",
                    "//div[contains(@style, 'position: fixed')]",
                    "//div[@role='presentation']"
                ]
                
                dialog = None
                for alt_selector in alternative_dialogs:
                    try:
                        print(f"[DEBUG] Trying alternative dialog selector: {alt_selector}")
                        dialog = self.driver.find_element(By.XPATH, alt_selector)
                        if dialog.is_displayed():
                            print(f"[DEBUG] Found dialog with selector: {alt_selector}")
                            break
                    except NoSuchElementException:
                        continue
                
                if not dialog:
                    print("[DEBUG] Could not find dialog with any selector")
                    print("[DEBUG] Page source snippet (first 2000 chars):")
                    print(self.driver.page_source[:2000])
                    raise Exception(f"Could not find {list_type} dialog. Instagram may have changed their interface.")
            
            # Find the scrollable container within the dialog
            # Instagram uses a specific structure - find the actual scrollable list
            print("[DEBUG] Finding scrollable container...")
            scrollable_container = None
            
            # Try to find the actual scrollable list element
            scrollable_selectors = [
                ".//div[@role='dialog']//div[contains(@style, 'overflow')]",
                ".//div[@role='dialog']//div[contains(@class, '_aano')]",  # Instagram's scrollable class
                ".//div[@role='dialog']//ul",
                ".//div[@role='dialog']//div[contains(@style, 'height')]",
                ".//div[contains(@class, 'scroll')]",
                ".//ul",
            ]
            
            for selector in scrollable_selectors:
                try:
                    containers = dialog.find_elements(By.XPATH, selector)
                    print(f"[DEBUG] Found {len(containers)} containers with selector: {selector}")
                    for container in containers:
                        try:
                            # Check if it's actually scrollable
                            scroll_height = self.driver.execute_script("return arguments[0].scrollHeight", container)
                            client_height = self.driver.execute_script("return arguments[0].clientHeight", container)
                            if scroll_height > client_height:
                                scrollable_container = container
                                print(f"[DEBUG] Found scrollable container! scrollHeight={scroll_height}, clientHeight={client_height}")
                                break
                        except:
                            continue
                    if scrollable_container:
                        break
                except Exception as e:
                    print(f"[DEBUG] Error with selector {selector}: {str(e)}")
                    continue
            
            # Fallback: use the dialog itself or find by scrolling
            if not scrollable_container:
                print("[DEBUG] No scrollable container found, trying dialog itself...")
                try:
                    scroll_height = self.driver.execute_script("return arguments[0].scrollHeight", dialog)
                    client_height = self.driver.execute_script("return arguments[0].clientHeight", dialog)
                    if scroll_height > client_height:
                        scrollable_container = dialog
                        print(f"[DEBUG] Using dialog as scrollable container")
                    else:
                        # Try to find any div inside dialog that can scroll
                        all_divs = dialog.find_elements(By.XPATH, ".//div")
                        for div in all_divs:
                            try:
                                sh = self.driver.execute_script("return arguments[0].scrollHeight", div)
                                ch = self.driver.execute_script("return arguments[0].clientHeight", div)
                                if sh > ch and sh > 100:  # Must have some content
                                    scrollable_container = div
                                    print(f"[DEBUG] Found scrollable div: scrollHeight={sh}, clientHeight={ch}")
                                    break
                            except:
                                continue
                except:
                    scrollable_container = dialog
            
            if not scrollable_container:
                scrollable_container = dialog
                print("[DEBUG] Using dialog as fallback scrollable container")
            
            # Scroll and extract usernames
            print(f"[DEBUG] Starting to extract {list_type}...")
            print(f"[DEBUG] Dialog size: {dialog.size}")
            print(f"[DEBUG] Scrollable container found: {scrollable_container is not None}")
            
            usernames = set()
            last_count = 0
            no_change_count = 0
            max_no_change = 3  # Stop after 3 consecutive scrolls with no new users
            scroll_delay = 2  # Wait 2 seconds for content to load after scroll
            
            print(f"Loading {list_type}...", end="", flush=True)
            
            while no_change_count < max_no_change:
                # Extract usernames from visible elements
                try:
                    # Re-find dialog if stale
                    try:
                        user_elements = dialog.find_elements(
                            By.XPATH,
                            ".//a[contains(@href, '/')]"
                        )
                    except StaleElementReferenceException:
                        print("\n[DEBUG] Stale element reference, re-finding dialog...")
                        dialog = wait.until(EC.presence_of_element_located((By.XPATH, dialog_xpath)))
                        user_elements = dialog.find_elements(By.XPATH, ".//a[contains(@href, '/')]")
                    
                    # Extract usernames from current visible elements
                    before_extraction = len(usernames)
                    for element in user_elements:
                        try:
                            href = element.get_attribute('href')
                            if href and 'instagram.com' in href:
                                # Extract username from URL (format: instagram.com/username/)
                                parts = href.rstrip('/').split('/')
                                if len(parts) > 0:
                                    username = parts[-1]
                                    # Validate username (should not contain special characters or be Instagram pages)
                                    if (username and 
                                        username != self.username and
                                        username not in ['explore', 'reels', 'accounts', 'direct', 'stories', 'p'] and
                                        not username.startswith('?') and
                                        not username.startswith('#') and
                                        not username.startswith('@')):
                                        usernames.add(username)
                        except:
                            continue
                    
                    current_count = len(usernames)
                    if current_count > last_count:
                        print(f"\rLoading {list_type}... {current_count} found", end="", flush=True)
                        last_count = current_count
                        no_change_count = 0  # Reset counter when we find new users
                    else:
                        no_change_count += 1
                        if no_change_count >= max_no_change:
                            print(f"\n[DEBUG] No new users found after {max_no_change} scrolls, stopping...")
                            break
                    
                except Exception as e:
                    print(f"\n[DEBUG] Error extracting usernames: {str(e)}")
                    no_change_count += 1
                    if no_change_count >= max_no_change:
                        break
                
                # Scroll down in the dialog
                scroll_success = False
                try:
                    # Get current scroll position and height
                    last_scroll_top = self.driver.execute_script(
                        "return arguments[0].scrollTop", scrollable_container
                    )
                    last_scroll_height = self.driver.execute_script(
                        "return arguments[0].scrollHeight", scrollable_container
                    )
                    
                    # Scroll to bottom
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight",
                        scrollable_container
                    )
                    
                    # Wait for new content to load
                    time.sleep(scroll_delay)
                    
                    # Check if we've scrolled and if new content loaded
                    new_scroll_top = self.driver.execute_script(
                        "return arguments[0].scrollTop", scrollable_container
                    )
                    new_scroll_height = self.driver.execute_script(
                        "return arguments[0].scrollHeight", scrollable_container
                    )
                    
                    if new_scroll_top > last_scroll_top or new_scroll_height > last_scroll_height:
                        scroll_success = True
                        if no_change_count == 0:  # Only print debug on first scroll
                            print(f"\n[DEBUG] Scrolled: top={last_scroll_top}->{new_scroll_top}, height={last_scroll_height}->{new_scroll_height}")
                    
                    # If scroll height didn't change and we're at the bottom, we might be done
                    if new_scroll_height == last_scroll_height and new_scroll_top >= new_scroll_height - 10:
                        # Check one more time for new users after a brief wait
                        time.sleep(1)
                        if len(usernames) == last_count:
                            print(f"\n[DEBUG] Reached bottom with no new users, stopping")
                            break
                    
                except Exception as e:
                    print(f"\n[DEBUG] Error scrolling container: {str(e)}")
                
                # If container scroll didn't work, try keyboard scrolling on the scrollable container
                if not scroll_success:
                    try:
                        # Focus on the scrollable container and scroll with keyboard
                        self.driver.execute_script("arguments[0].focus();", scrollable_container)
                        scrollable_container.send_keys(Keys.PAGE_DOWN)
                        time.sleep(scroll_delay)
                        scroll_success = True
                    except Exception as e:
                        # Try sending keys to dialog instead
                        try:
                            dialog.send_keys(Keys.PAGE_DOWN)
                            time.sleep(scroll_delay)
                            scroll_success = True
                        except:
                            pass
                
                # Final fallback: scroll the last visible element into view
                if not scroll_success:
                    try:
                        # Find username links and scroll the last one into view
                        user_links = dialog.find_elements(By.XPATH, ".//a[contains(@href, '/')]")
                        if user_links and len(user_links) > 0:
                            # Scroll the last visible link into view
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});",
                                user_links[-1]
                            )
                            time.sleep(scroll_delay)
                            scroll_success = True
                    except Exception as e:
                        pass
                
                if not scroll_success:
                    no_change_count += 1
                    if no_change_count >= max_no_change:
                        print(f"\n[DEBUG] Could not scroll after {max_no_change} attempts, stopping")
                        break
            
            print()  # New line after progress
            
            if not usernames:
                raise Exception(f"No {list_type} found. This may indicate an error or your account has no {list_type}.")
            
            return sorted(list(usernames))
            
        except TimeoutException:
            error_msg = f"Timeout while extracting {list_type}. Instagram may be loading slowly."
            print(f"\n✗ {error_msg}")
            raise Exception(error_msg)
        except WebDriverException as e:
            error_msg = f"Network error while extracting {list_type}: {str(e)}"
            print(f"\n✗ {error_msg}")
            raise Exception(error_msg)
        except StaleElementReferenceException:
            error_msg = f"Page elements changed while extracting {list_type}. Please try again."
            print(f"\n✗ {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error extracting {list_type}: {str(e)}"
            print(f"\n✗ {error_msg}")
            raise
    
    def find_non_followers(self) -> List[str]:
        """
        Find accounts that the user follows but who don't follow back.
        
        Returns:
            List of usernames that don't follow back
            
        Raises:
            Exception: If not logged in or extraction fails
        """
        if not self.is_logged_in:
            raise Exception("Not logged in. Please login first.")
        
        try:
            print("\nAnalyzing followers and following lists...")
            followers = self.get_followers()
            following = self.get_following()
            
            if not followers or not following:
                raise Exception("Could not retrieve complete lists. Please try again.")
            
            # Convert to sets for comparison
            followers_set = set(followers)
            following_set = set(following)
            
            # Find accounts in following but not in followers
            non_followers = following_set - followers_set
            
            return sorted(list(non_followers))
        except Exception as e:
            # Re-raise with context
            if "rate" in str(e).lower() or "limit" in str(e).lower():
                raise Exception("Instagram rate limit detected. Please wait a few minutes before trying again.")
            raise
    
    def close(self):
        """Close the browser and cleanup."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                # Ignore errors during cleanup
                pass
            finally:
                self.is_logged_in = False
                self.driver = None
