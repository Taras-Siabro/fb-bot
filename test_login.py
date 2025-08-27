from core.selenium_utils import setup_driver
from core.fb_bot import login, search_groups
from config import FB_EMAIL, FB_PASSWORD, DEFAULT_QUERY
from core.join_groups import join_all_groups_from_search

driver = setup_driver(headless=False)
login(driver, FB_EMAIL, FB_PASSWORD)
search_groups(driver, DEFAULT_QUERY)
join_all_groups_from_search(driver)
input("Press Enter to close the browser...")
driver.quit()