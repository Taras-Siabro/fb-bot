from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.selenium_utils import setup_driver
from selenium.webdriver.common.action_chains import ActionChains
import time

FB_URL = "https://www.facebook.com/"

def login(driver, email, password):
    driver.get(FB_URL)
    try:
        accept_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Allow all cookies']")
            )
        )
        ActionChains(driver).move_to_element(accept_btn).click().perform()
        print("Cookies accepted via span")
    except:
        print("Cookies banner not found")

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_input.send_keys(email)

    pass_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pass"))
    )
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)
    time.sleep(5)


def search_groups(driver, query):
    """Search for Facebook groups with specific selectors"""
    try:
        print("Starting group search...")
        
        # Поиск поисковой строки
        search_selectors = [
            "//input[@placeholder='Search Facebook']",
            "//input[contains(@aria-label, 'Search')]",
            "//input[@type='search']",
            "//div[@role='search']//input",
            "//input[@name='q']"
        ]
        
        search_input = None
        for selector in search_selectors:
            try:
                search_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"Found search input with selector: {selector}")
                break
            except:
                continue
        
        if not search_input:
            raise Exception("Could not find search input")
        
        # Ввод запроса и поиск
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)
        print("Search query submitted")
        
        # Ждем загрузки результатов поиска
        time.sleep(3)
        
        # Кликаем на вкладку "Groups" с вашим селектором
        try:
            groups_tab = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x6prxxf xvq8zen xk50ysn xzsf02u' and text()='Groups']"))
            )
            groups_tab.click()
            print("Clicked on Groups tab")
        except Exception as e:
            print(f"Could not find Groups tab with specific selector: {e}")
            
    except:
        print("Groups not found")