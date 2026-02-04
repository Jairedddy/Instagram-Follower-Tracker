"""
Main CLI interface for Instagram Non-Follower Bot.
"""

import sys
import os
try:
    import msvcrt  # Windows only
    WINDOWS = True
except ImportError:
    WINDOWS = False
    import termios
    import tty
from instagram_bot import InstagramBot


def print_header():
    """Print welcome header."""
    print("=" * 60)
    print("  Instagram Non-Follower Bot")
    print("  Find accounts that don't follow you back")
    print("=" * 60)
    print()


def print_menu():
    """Print main menu options."""
    print("\n" + "-" * 60)
    print("MENU:")
    print("  1. Login to Instagram")
    print("  2. Run Analysis (Find Non-Followers)")
    print("  3. Exit")
    print("-" * 60)


def get_user_choice() -> str:
    """Get user's menu choice."""
    choice = input("\nEnter your choice (1-3): ").strip()
    return choice


def get_password_with_asterisks(prompt: str = "Enter your Instagram password: ") -> str:
    """
    Get password input with asterisks visible.
    Works on Windows using msvcrt, falls back to getpass on other systems.
    
    Args:
        prompt: The prompt message to display
        
    Returns:
        The password string entered by the user
    """
    if WINDOWS:
        print(prompt, end="", flush=True)
        password = []
        
        while True:
            try:
                char = msvcrt.getch()
                
                # Enter key (carriage return)
                if char == b'\r':
                    print()  # New line
                    break
                # Backspace
                elif char == b'\x08':
                    if len(password) > 0:
                        password.pop()
                        print('\b \b', end='', flush=True)  # Erase the asterisk
                # Escape key
                elif char == b'\x1b':
                    password = []
                    print("\nCancelled.")
                    return ""
                # Regular character
                else:
                    try:
                        char_str = char.decode('utf-8')
                        if char_str.isprintable():
                            password.append(char_str)
                            print('*', end='', flush=True)
                    except (UnicodeDecodeError, AttributeError):
                        pass
            except KeyboardInterrupt:
                print("\n\nCancelled.")
                return ""
        
        return ''.join(password)
    else:
        # Fallback for non-Windows systems (Linux/Mac)
        import getpass
        return getpass.getpass(prompt)


def login_flow(bot: InstagramBot) -> bool:
    """
    Handle login flow with username, password, and optional 2FA.
    
    Returns:
        True if login successful, False otherwise
    """
    print("\n" + "-" * 60)
    print("LOGIN")
    print("-" * 60)
    
    username = input("Enter your Instagram username: ").strip()
    if not username:
        print("✗ Username cannot be empty.")
        return False
    
    password = get_password_with_asterisks("Enter your Instagram password: ")
    if not password:
        print("✗ Password cannot be empty.")
        return False
    
    print("\nLogging in...")
    success = bot.login(username, password)
    
    if success:
        print("\n✓ Login successful! You can now run the analysis.")
    else:
        print("\n✗ Login failed. Please check your credentials and try again.")
    
    return success


def run_analysis(bot: InstagramBot):
    """Run the analysis to find non-followers."""
    if not bot.is_logged_in:
        print("\n✗ You must login first before running the analysis.")
        return
    
    print("\n" + "-" * 60)
    print("RUNNING ANALYSIS")
    print("-" * 60)
    print("\nThis may take a few minutes depending on the number of")
    print("followers and accounts you follow...")
    print("Please be patient and don't close the browser window.")
    
    try:
        non_followers = bot.find_non_followers()
        
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        
        if non_followers:
            print(f"\nFound {len(non_followers)} account(s) that don't follow you back:\n")
            for i, username in enumerate(non_followers, 1):
                print(f"  {i}. @{username}")
            print()
        else:
            print("\n✓ Great news! Everyone you follow also follows you back!")
            print()
        
        print("-" * 60)
        
    except KeyboardInterrupt:
        print("\n\n✗ Analysis interrupted by user.")
        print("You can try running the analysis again.")
    except Exception as e:
        error_msg = str(e)
        print(f"\n✗ Error during analysis: {error_msg}")
        
        if "rate limit" in error_msg.lower() or "rate-limited" in error_msg.lower():
            print("\n⚠ Instagram has rate-limited your requests.")
            print("Please wait 10-15 minutes before trying again.")
            print("You can stay logged in and try again later.")
        elif "network" in error_msg.lower() or "connection" in error_msg.lower():
            print("\n⚠ Network error detected.")
            print("Please check your internet connection and try again.")
        elif "timeout" in error_msg.lower():
            print("\n⚠ Request timed out. Instagram may be loading slowly.")
            print("Please try again.")
        else:
            print("\nPlease try again. If the problem persists, try logging in again.")


def main():
    """Main entry point."""
    print_header()
    
    bot = None
    
    try:
        bot = InstagramBot(headless=False)
        
        while True:
            print_menu()
            choice = get_user_choice()
            
            if choice == "1":
                login_flow(bot)
            elif choice == "2":
                run_analysis(bot)
            elif choice == "3":
                print("\nThank you for using Instagram Non-Follower Bot!")
                break
            else:
                print("\n✗ Invalid choice. Please enter 1, 2, or 3.")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n✗ An unexpected error occurred: {str(e)}")
        print("Please try again or restart the application.")
    finally:
        if bot:
            bot.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
