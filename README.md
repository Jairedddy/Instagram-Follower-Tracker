# 🔍 Instagram Follow-Back Checker

<div align="center">

**An intelligent, automated solution for analyzing Instagram follow-back relationships**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://selenium-python.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Technical Details](#-technical-details)
- [Browser Support](#-browser-support)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Limitations](#-limitations)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **Instagram Follow-Back Checker** is a sophisticated Python-based automation tool designed to analyze your Instagram account and identify which accounts you follow that don't follow you back. This solution eliminates the need for manual checking by automating the entire process through intelligent browser automation.

### What It Does

1. **Automated Login**: Secure login with real-time character-by-character input
2. **Profile Analysis**: Automatically analyzes your logged-in account
3. **Complete Extraction**: Scrolls through all followers and following lists
4. **Smart Comparison**: Identifies accounts that don't follow you back
5. **Repeatable Analysis**: Run multiple analyses without re-logging in

### Use Cases

- **Follow-Back Analysis**: Identify accounts that don't follow you back
- **Account Cleanup**: Maintain a clean following list
- **Relationship Tracking**: Monitor mutual follows over time
- **Time-Saving Automation**: Eliminate manual checking of hundreds of accounts

---

## ✨ Key Features

### 🔐 Secure Login with Real-Time Input

- **Character-by-Character Input**: See your username and password (as asterisks) as you type
- **Browser Synchronization**: Characters appear in browser fields as you type in terminal
- **2FA Support**: Handles two-factor authentication seamlessly
- **Auto-Dialog Handling**: Automatically closes Instagram's "Save Info" and "Ok" dialogs

### 📊 Smart Extraction Algorithm

- **Progress Tracking**: Visual progress bar showing extraction status in real-time
- **Scroll Optimization**: Efficiently scrolls through Instagram's lazy-loaded content
- **Complete Extraction**: Ensures all accounts are captured, not just initial visible ones
- **Height Tracking**: Monitors scroll height to detect when all content is loaded

### 🎨 User Experience

- **Interactive Prompts**: Clear instructions and user-friendly interface
- **Repeatable Analysis**: Run multiple analyses without re-logging in
- **Error Handling**: Graceful error handling with retry options
- **Progress Visualization**: Real-time progress bar with scroll count

### ⚡ Performance Optimizations

- **Fast Scrolling**: Optimized scroll algorithm (0.3s pause between scrolls)
- **Threshold Protection**: Prevents analysis on accounts with >750 followers/following
- **Memory Efficient**: Uses sets for fast lookups and comparisons
- **Stale Element Handling**: Automatically re-finds elements when they become stale

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                  User Authentication                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Username   │  │   Password   │  │     2FA      │   │
│  │   Input      │  │   Input      │  │     OTP     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  Browser Initialization                 │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐                 │
│  │Chrome│→ │Brave │→ │ Edge │→ │Firefox│                │
│  └──────┘  └──────┘  └──────┘  └──────┘                 │
│     │         │         │         │                     │
│     └─────────┴─────────┴─────────┘                     │
│              (Automatic Fallback)                       │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    Profile Analysis                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Extract    │  │   Check     │  │   Validate   │   │
│  │   Counts     │  │  Threshold  │  │   Limits     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  List Extraction                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Open       │  │   Scroll     │  │   Extract   │   │
│  │   Modal      │  │   & Load     │  │  Usernames  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  Comparison & Results                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Calculate  │  │   Display    │  │   Prompt     │   │
│  │   Difference │  │   Results    │  │   Retry      │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.9+ |
| **Automation Framework** | Selenium WebDriver | 4.0+ |
| **Driver Management** | Selenium Manager | Built-in |
| **Browser Support** | Chrome, Brave, Edge, Firefox | Latest |

### Module Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      app.py                             │
│              (Main Orchestration Layer)                 │
└─────────────────────────────────────────────────────────┘
         │           │           │           │
         ▼           ▼           ▼           ▼
┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│  browser.py │ │ login.py │ │scraper.py│ │ utils.py │
│             │ │          │ │          │ │          │
│  Browser    │ │  Login   │ │ Profile  │ │  Helper  │
│  Setup      │ │  Auth    │ │ Scraping │ │ Functions│
└─────────────┘ └──────────┘ └──────────┘ └──────────┘
```

---

## 📦 Prerequisites

### System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: Version 3.9 or higher
- **Internet Connection**: Required for web scraping and driver downloads
- **Browser**: At least one of the following installed:
  - Google Chrome
  - Brave Browser
  - Microsoft Edge
  - Mozilla Firefox

### Python Installation

1. **Download Python**:
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.9 or higher
   - **Important**: Check "Add Python to PATH" during installation

2. **Verify Installation**:
   ```bash
   python --version
   # Should display: Python 3.9.x or higher
   ```

### Browser Installation

The bot will automatically detect installed browsers. Ensure at least one is installed:

- **Chrome**: [Download Chrome](https://www.google.com/chrome/)
- **Brave**: [Download Brave](https://brave.com/download/)
- **Edge**: Pre-installed on Windows 10/11
- **Firefox**: [Download Firefox](https://www.mozilla.org/firefox/)

---

## 🔧 Installation

### Step 1: Clone or Download the Project

```bash
# Using Git
git clone <repository-url>
cd Instagram-Bot

# Or download and extract the ZIP file
```

### Step 2: Install Python Dependencies

```bash
# Navigate to the project directory
cd Instagram-Bot

# Install required packages
pip install selenium>=4.0.0

# Or create requirements.txt and install
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
# Test Python import
python -c "import selenium; print(selenium.__version__)"

# Run the application
python app.py
```

**Note**: Selenium Manager will automatically download the appropriate browser driver when you first run the script. No manual driver installation needed!

---

## 🚀 Usage

### Basic Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Login Process**:
   - Enter your Instagram username (characters appear in browser as you type)
   - Enter your password (shown as asterisks `*` in terminal)
   - If 2FA is enabled, enter the OTP code when prompted

3. **Wait for Analysis**:
   - The tool automatically analyzes your logged-in account
   - Watch the progress bar as it extracts followers and following lists
   - Results are displayed automatically

4. **Review Results**:
   - See which accounts don't follow you back
   - Choose to run the analysis again or exit

### Expected Output

```
Instagram follow-back checker (Selenium)
---------------------
Starting browser... (Selenium Manager will try to provide driver automatically)
Using browser: chrome
Your instagram username: your_username
Your instagram password: ********

Login successful!

Analyzing your account: your_username
Found 624 followers and 504 following.

Extracting followers (total: 624)...
(####################) 100% accounts loaded (624 out of 624). Scroll: 45

Collected 624 followers.

Extracting following (total: 504)...
(####################) 100% accounts loaded (504 out of 504). Scroll: 38

Collected 504 following.

Accounts you follow but who don't follow you back: 
1. account1
2. account2
3. account3
...

==================================================
Would you like to run the analysis again? (yes/no): no

Exiting application. Thank you!
```

### Advanced Usage

#### Running Multiple Analyses

After the first analysis completes, you can choose to run again without re-logging:

```
Would you like to run the analysis again? (yes/no): yes

Running analysis again...
Analyzing your account: your_username
...
```

---

## 🔍 Technical Details

### Execution Flow

1. **Browser Initialization** (`browser.py`)
   - Attempts browsers in priority order: Chrome → Brave → Edge → Firefox
   - Uses Selenium Manager for automatic driver management
   - Provides helpful error messages if all browsers fail

2. **Login Process** (`login.py`)
   - Navigates to Instagram login page
   - Real-time character-by-character input synchronization
   - Handles 2FA if required
   - Closes dialog boxes automatically

3. **Profile Analysis** (`scraper.py`)
   - Navigates to logged-in user's profile
   - Extracts follower and following counts
   - Validates threshold (<750 for both)

4. **List Extraction** (`scraper.py`)
   - Opens followers/following modal
   - Finds scrollable container using multiple strategies
   - Scrolls to bottom triggering lazy loading
   - Extracts all visible usernames
   - Tracks progress with real-time progress bar

5. **Comparison & Results** (`app.py`)
   - Calculates difference between following and followers
   - Displays sorted list of accounts not following back
   - Prompts for re-analysis or exit

### Scroll Detection Algorithm

The bot uses a sophisticated multi-layer approach:

#### Layer 1: Scroll Height Tracking
```python
# Monitors scrollHeight vs clientHeight
# Detects when content stops growing
```

#### Layer 2: Account Count Tracking
```python
# Tracks number of accounts found per iteration
# Detects when no new accounts appear
```

#### Layer 3: Bottom Detection
```python
# Checks if scrollTop + clientHeight >= scrollHeight
# Confirms we've reached the end
```

#### Layer 4: Final Verification
```python
# Performs one final scroll to ensure nothing loads
# Only terminates if all conditions met
```

### Element Selectors

| Element | Selector Type | Selector | Purpose |
|---------|---------------|----------|---------|
| Username Field | NAME | `username` | Locate login username input |
| Password Field | NAME | `password` | Locate login password input |
| 2FA Input | Multiple | Various | Locate OTP input field |
| Followers Link | XPath | `//a[contains(@href, '/followers/')]` | Open followers modal |
| Following Link | XPath | `//a[contains(@href, '/following/')]` | Open following modal |
| Modal Dialog | XPath | `//div[@role='dialog']` | Locate modal container |
| Scroll Container | Multiple | Dynamic | Find scrollable element |
| Account Links | XPath | `.//a` | Extract account URLs |

### Timing and Waits

- **Page Load Wait**: 2 seconds after navigation
- **Modal Wait**: 2 seconds for modal to appear
- **Scroll Pause**: 0.3 seconds between scrolls
- **WebDriverWait Timeout**: 15 seconds for element interactions
- **Stable Height Count**: 10 iterations before termination
- **No New Accounts Threshold**: 4 consecutive scrolls

---

## 🌐 Browser Support

### Supported Browsers

| Browser | Driver | Automatic Support | Manual Configuration |
|---------|--------|-------------------|----------------------|
| **Chrome** | ChromeDriver | ✅ Yes | ✅ Yes |
| **Brave** | ChromeDriver | ✅ Yes | ✅ Yes |
| **Edge** | EdgeDriver | ✅ Yes | ✅ Yes |
| **Firefox** | GeckoDriver | ✅ Yes | ✅ Yes |

### Browser Priority Order

The bot attempts to initialize browsers in this order:

1. **Chrome** (Primary)
2. **Brave** (Fallback 1)
3. **Edge** (Fallback 2)
4. **Firefox** (Fallback 3)

### Automatic Driver Management

**Default Behavior**: The bot uses Selenium Manager (built into Selenium 4.6+) to automatically:

- Detect browser version
- Download matching driver
- Manage driver lifecycle
- Update drivers as needed

**Benefits**:
- ✅ No manual driver downloads required
- ✅ Automatic version matching
- ✅ No configuration needed
- ✅ Always up-to-date drivers

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. ❌ Browser Driver Not Found

**Error Message**:
```
WebDriverException: ... driver not found
```

**Solutions**:
1. Ensure you have the latest version of your browser installed
2. Selenium Manager should auto-download drivers, but if it fails:
   - Chrome: Download from [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - Edge: Download from [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
   - Firefox: Download from [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

#### 2. ❌ Login Fails

**Error Message**:
```
Login page did not load properly
```

**Solutions**:
1. Check your internet connection
2. Verify your username and password are correct
3. Ensure Instagram is accessible (not blocked)
4. Try again after a few minutes (rate limiting)

#### 3. ⚠️ Extraction Stops Early

**Symptoms**: Progress bar stops before reaching 100%

**Solutions**:
1. This usually means Instagram hasn't loaded all content yet
2. The tool includes multiple checks to ensure complete extraction
3. If it consistently stops early, Instagram's page structure may have changed
4. Try running the analysis again

#### 4. ❌ Modal Doesn't Open

**Error Message**:
```
Could not find scroll container for followers modal
```

**Solutions**:
1. Wait a moment and try again
2. Ensure your account has followers/following to display
3. Check if Instagram's interface has changed
4. Verify you're logged in correctly

#### 5. ⚠️ Progress Bar Prints Multiple Lines

**Symptoms**: Progress bar creates new lines instead of updating

**Solutions**:
1. This is fixed in the current version
2. Ensure you're using the latest code
3. Some terminals may not support `\r` properly - try a different terminal
4. Windows PowerShell and CMD should work correctly

#### 6. ModuleNotFoundError: No module named 'selenium'

**Error Message**:
```
ModuleNotFoundError: No module named 'selenium'
```

**Solution**:
```bash
pip install selenium
# Or
python3 -m pip install selenium
```

#### 7. ❌ Threshold Exceeded

**Error Message**:
```
Error: Cannot proceed. Found X followers and Y following.
```

**Solutions**:
1. This tool only works for accounts with <750 followers and <750 following
2. This is a design limitation to ensure reliable extraction
3. Consider using Instagram's official API for larger accounts

#### 8. ⚠️ 2FA Not Working

**Symptoms**: OTP input doesn't appear or doesn't work

**Solutions**:
1. Ensure you enter the OTP code quickly (they expire)
2. Check that the OTP field is detected correctly
3. Try manually entering the OTP if automatic detection fails

---

## 📁 Project Structure

```
Instagram-Bot/
│
├── app.py              # Main application entry point
├── browser.py          # Browser setup and driver creation
├── login.py            # Instagram login functionality
├── scraper.py          # Profile and list extraction
├── utils.py            # Utility functions (parsing, progress bar, input)
└── README.md           # This documentation
```

### File Descriptions

| File | Description | Key Functions |
|------|-------------|---------------|
| `app.py` | Main orchestration, user interaction, analysis loop | `main()`, `run_analysis()` |
| `browser.py` | Browser driver creation (Chrome, Edge, Firefox, Brave) | `create_driver_prefer_browser()` |
| `login.py` | Instagram authentication, 2FA handling, dialog management | `login_instagram()`, `safe_click()` |
| `scraper.py` | Profile count extraction, modal scrolling, account list extraction | `get_profile_counts()`, `extract_list_from_modal()`, `find_scrollable_container()` |
| `utils.py` | Helper functions for parsing counts, progress display, real-time input | `parse_count()`, `update_progress_bar()`, `input_to_browser_real_time()` |

### Code Organization

- **`browser.py`**: Browser initialization with automatic fallback
- **`login.py`**: Login flow with real-time input and 2FA support
- **`scraper.py`**: All scraping logic including scroll detection and extraction
- **`utils.py`**: Reusable utility functions
- **`app.py`**: Main application flow and user interaction

---

## ⚠️ Limitations

1. **Account Size**: Only works for accounts with <750 followers and <750 following
2. **Rate Limiting**: Instagram may rate limit if you run too many analyses
3. **Page Changes**: Instagram may update their page structure, requiring code updates
4. **Private Accounts**: Cannot analyze private accounts you don't have access to
5. **Browser Dependency**: Requires a browser to be installed and working
6. **Internet Required**: Needs stable internet connection for scraping

---

## 🔮 Future Enhancements

Potential improvements for future versions:

- [ ] **Export Results**: Export results to CSV/Excel/JSON
- [ ] **Database Storage**: Store analysis history in SQLite/PostgreSQL
- [ ] **Scheduled Execution**: Cron jobs or task scheduler integration
- [ ] **Email Notifications**: Send email alerts for new non-followers
- [ ] **Web Dashboard**: Web interface to view analysis history
- [ ] **REST API**: Programmatic access via API endpoints
- [ ] **File Logging**: Persistent logging for debugging and audit trails
- [ ] **Headless Mode**: Run without opening browser window
- [ ] **Parallel Processing**: Check multiple accounts simultaneously
- [ ] **Retry Logic**: Automatic retries for failed extractions
- [ ] **Telegram Bot Integration**: Real-time notifications via Telegram
- [ ] **Docker Support**: Containerized deployment
- [ ] **Multi-Account Support**: Analyze multiple accounts in one session

---

## 🤝 Contributing

Contributions are welcome! Areas for contribution:

- **Bug Fixes**: Report and fix issues
- **Feature Additions**: Implement new features from the roadmap
- **Documentation**: Improve documentation and examples
- **Code Optimization**: Performance improvements and refactoring
- **Testing**: Add unit tests and integration tests
- **Browser Support**: Add support for additional browsers

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

**Important Notes**:
- **Rate Limiting**: The bot includes delays between actions to avoid overwhelming Instagram's servers
- **Website Changes**: If Instagram's page structure changes, selectors may need updating
- **Legal Compliance**: Ensure compliance with Instagram's terms of service
- **Browser Version**: Keep browsers and drivers updated for best compatibility

---

## 👤 Author

Created for automating Instagram follow-back analysis.

---

## 🙏 Acknowledgments

- **Selenium WebDriver Team**: Excellent browser automation framework
- **Microsoft**: EdgeDriver and Edge browser
- **Google**: ChromeDriver and Chrome browser
- **Mozilla**: GeckoDriver and Firefox browser
- **Brave Software**: Brave browser
- **Instagram**: Platform and API

---

## 📞 Support

For issues, questions, or contributions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Check the code comments for implementation details

---

<div align="center">

**Last Updated**: December 2024  
**Version**: 2.0.0  
**Python Version**: 3.9+  
**Selenium Version**: 4.0+

Made with ❤️ for Instagram users

⭐ Star this repo if you find it useful!

</div>
