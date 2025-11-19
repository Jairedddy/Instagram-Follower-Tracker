import time
from browser import create_driver_prefer_browser
from login import login_instagram
from scraper import get_profile_counts, open_profile, extract_list_from_modal, THRESHOLD_MAX_ACCOUNTS


def run_analysis(driver, profile_to_check):
    print(f"\nAnalyzing your account: {profile_to_check}")
    followers_count, following_count = get_profile_counts(driver, profile_to_check)
    
    if followers_count is None or following_count is None:
        print("Could not extract follower/following counts.")
        return False
    
    print(f"Found {followers_count} followers and {following_count} following.")
    if followers_count >= THRESHOLD_MAX_ACCOUNTS or following_count >= THRESHOLD_MAX_ACCOUNTS:
        print(f"\nError: Cannot proceed. Found {followers_count} followers and {following_count} following.")
        print(f"This tool only works for accounts with both followers and following less than {THRESHOLD_MAX_ACCOUNTS}.")
        return False
    
    print(f"\nExtracting followers (total: {followers_count})...")
    followers = extract_list_from_modal(driver, which="followers", total_count=followers_count)
    print(f"\nCollected {len(followers)} followers.")
    
    time.sleep(2)
    
    open_profile(driver, profile_to_check)
    time.sleep(1)
    print(f"\nExtracting following (total: {following_count})...")
    following = extract_list_from_modal(driver, which="following", total_count=following_count)
    print(f"\nCollected {len(following)} following.")
    not_following_back = sorted(set(following) - set(followers), key=lambda s: s.lower())
    if not not_following_back:
        print("\nAll accounts you follow also follow you back (or lists are identical).")
    else:
        print("\nAccounts you follow but who don't follow you back: ")
        for idx, u in enumerate(not_following_back, 1):
            print(f"{idx}. {u}")
    
    return True


def main():
    print("Instagram follow-back checker (Selenium)")
    print("---------------------")
    print("Starting browser... (Selenium Manager will try to provide driver automatically)")
    driver, browser_name = create_driver_prefer_browser()
    print("Using browser: ", browser_name)
    driver.implicitly_wait(3)
    
    try:
        try:
            logged_in_username = login_instagram(driver)
            print("\n✅ Login successful!")
            time.sleep(2)
        except ValueError as login_error:
            print("\n❌ Login failed")
            print("\nPossible reasons:")
            print("  - Incorrect username or password")
            print("  - Incorrect 2FA OTP code")
            print("  - Account temporarily locked")
            print("  - Network connectivity issues")
            print("\nPlease check your credentials and try again.")
            return
        while True:
            try:
                run_analysis(driver, logged_in_username)
                print("\n" + "="*50)
                user_choice = input("Would you like to run the analysis again? (yes/no): ").strip().lower()
                if user_choice in ['yes', 'y']:
                    print("\nRunning analysis again...")
                    continue
                elif user_choice in ['no', 'n']:
                    print("\nExiting application. Thank you!")
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    continue
            except KeyboardInterrupt:
                print("\n\nUser interrupted. Exiting.")
                break
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")
                retry = input("Would you like to try again? (yes/no): ").strip().lower()
                if retry not in ['yes', 'y']:
                    break
    except KeyboardInterrupt:
        print("\nUser interrupted. Exiting.")
    except Exception as e:
        print("An unexpected error occurred: ", e)
    finally:
        try:
            print("\nClosing browser...")
            driver.quit()
        except Exception:
            pass
if __name__ == "__main__":
    try:
        main()
    except ImportError as imp_e:
        print("Missing dependency. Please install Selenium and try again: ")
        print("      pip install selenium")
        raise