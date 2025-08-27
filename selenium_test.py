from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



FB_URL = "https://www.facebook.com/"
FB_EMAIL = "vladrekruter308@gmail.com"
FB_PASSWORD = "HGwhqgfqwtgvcq1"


def setup_driver():
    options = Options()
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(options=options)

    return driver



def accept_cookies(driver):
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

def login(driver, email, password):
    

    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(FB_EMAIL)
    password_input = driver.find_element(By.ID, "pass")
    password_input.send_keys(FB_PASSWORD, Keys.RETURN)

    time.sleep(100)
    

driver = setup_driver()
driver.get(FB_URL)
accept_cookies(driver)
login(driver, FB_EMAIL, FB_PASSWORD)