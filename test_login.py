from core.selenium_utils import setup_driver
from core.fb_bot import login, search_groups
from config import FB_EMAIL, FB_PASSWORD, DEFAULT_QUERY

driver = setup_driver(headless=False)
login(driver, FB_EMAIL, FB_PASSWORD)
search_groups(driver, DEFAULT_QUERY)
input("Press Enter to close the browser...")
driver.quit()