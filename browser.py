import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def create_driver_prefer_browser():
    try:
        chrome_opts = ChromeOptions()
        chrome_opts.add_argument("--start-maximized")
        chrome_opts.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=chrome_opts)
        return driver, "chrome"
    except Exception:
        pass

    brave_paths = [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe")
    ]
    for path in brave_paths:
        try:
            chrome_opts = ChromeOptions()
            chrome_opts.binary_location = path
            chrome_opts.add_argument("--start-maximized")
            chrome_opts.add_argument("--disabled-blink-features=AutomationControlled")
            driver = webdriver.Chrome(options=chrome_opts)
            return driver, "brave"
        except Exception:
            continue
        
    try:
        edge_opts = EdgeOptions()
        edge_opts.use_chromium = True
        edge_opts.add_argument("--start-maximized")
        driver = webdriver.Edge(options=edge_opts)
        return driver, "edge"
    except Exception:
        pass
    
    try:
        firefox_opts = FirefoxOptions()
        firefox_opts.add_argument("--width=1200")
        firefox_opts.add_argument("--height=900")
        driver = webdriver.Firefox(options=firefox_opts)
        return driver, "firefox"
    except Exception:
        pass
    
    print("\nERROR: Could not start any supported browser automatically.")
    print("Selenium Manager normally auto-downloads drivers for Chrome, Edge and Firefox.")
    print("If automatic driver installation fails, please install one browser driver manually:")
    print(" - ChromeDriver: https://sites.google.com/chromium.org/driver/")
    print(" - EdgeDriver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
    print(" - GeckoDriver: https://github.com/mozilla/geckodriver/releases")
    print("Then retry. (If you installed a driver, ensure it's on your PATH.)")
    sys.exit(1)