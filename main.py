from core.selenium_utils import setup_driver

from core.fb_bot import login, search_groups, join_groups, save_groups_to_db
import time
from config import FB_EMAIL, FB_PASSWORD, DEFAULT_QUERY

driver =  setup_driver()
def main():

    login(driver, FB_EMAIL, FB_PASSWORD)
    search_groups(driver, DEFAULT_QUERY)

    time.sleep(5)

    save_groups_to_db(driver, max_groups=10000)
    #print(f"Successfully joined {joined_count} groups")


if __name__ == "__main__":
    main()
