from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup_driver(headless=False):
    options = Options()
    prefs = {
    "profile.default_content_setting_values.notifications": 2  # 2 = Block, 1 = Allow
        }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--profile-directory=Default")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_argument("--disable-save-password-bubble")
    if headless:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
        """
    })
    return driver
