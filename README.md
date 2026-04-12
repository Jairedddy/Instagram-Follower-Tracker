# Instagram Non-Follower Bot

A Python bot that helps you identify which Instagram accounts you follow that don't follow you back.

## Features

- Secure login with username and password
- Two-factor authentication (2FA) support
- Automatic handling of Instagram dialogs (e.g., "Save Login Info")
- Progress tracking while extracting followers and following lists
- Session persistence - run multiple analyses without re-logging in
- Clear, numbered display of accounts that don't follow back

## Requirements

- Python 3.7 or higher
- Google Chrome browser installed
- ChromeDriver (automatically managed by webdriver-manager)

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the bot:
```bash
python main.py
```

2. When prompted, enter your Instagram username and password

3. If your account has 2FA enabled, enter the verification code when prompted

4. The bot will automatically handle any Instagram dialogs that appear

5. Once logged in, you can run the analysis to see which accounts don't follow you back

6. You can run the analysis multiple times without logging in again

7. Type 'exit' to quit the bot

## How It Works

1. The bot uses Selenium WebDriver to automate a Chrome browser
2. It logs into Instagram using your credentials
3. It navigates to your profile and extracts your complete followers list
4. It extracts your complete following list
5. It compares the two lists to find accounts you follow who don't follow you back
6. Results are displayed in a numbered list

## Important Notes

- This bot uses browser automation which may violate Instagram's Terms of Service
- Use at your own risk - Instagram may detect automation and restrict your account
- The bot includes delays to avoid triggering rate limits, but be cautious with frequent use
- All data processing happens locally - your credentials are never stored

## Troubleshooting

- **Login fails**: Check your username and password. If 2FA is enabled, make sure to enter the code promptly
- **ChromeDriver issues**: The bot uses webdriver-manager to automatically download the correct ChromeDriver version
- **Slow loading**: Instagram may load content slowly. The bot includes progress indicators and will wait for content to load
- **Element not found errors**: Instagram's interface may have changed. Check for updates to the bot

## License

This project is for educational purposes only. Use responsibly and in accordance with Instagram's Terms of Service.
