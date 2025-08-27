from core.selenium_utils import setup_driver
from core.join_and_add_groups import join_all_groups_from_search
from db.database import init_db
from core.fb_bot import login, search_groups
import time
from config import FB_EMAIL, FB_PASSWORD, DEFAULT_QUERY

driver =  setup_driver()
def main():
    init_db()

    login(driver, FB_EMAIL, FB_PASSWORD)
    search_groups(driver, DEFAULT_QUERY)

    time.sleep(5)

    join_all_groups_from_search(driver)

    driver.quit()


if __name__ == "__main__":
    main()
