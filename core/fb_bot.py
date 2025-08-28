from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.selenium_utils import setup_driver
from selenium.webdriver.common.action_chains import ActionChains
import time
from db import Session
from models import Group 
import random
from datetime import datetime
import re

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



def save_group_to_db(group_url):
    session = Session()
    if not session.query(Group).filter_by(url=group_url).first():  # проверка на дубликаты
        group = Group(url=group_url, joined_at=datetime.now())
        session.add(group)
        session.commit()
        print(f"💾 Group saved to DB: {group_url}")
    session.close()




def save_groups_to_db(driver, max_groups=50):
    session = Session()
    saved_count = 0
    processed_groups = set()

    while saved_count < max_groups:
        # Находим все ссылки на группы
        group_elements = driver.find_elements(
            By.XPATH, "//a[contains(@href, '/groups/') and not(contains(@href, 'search'))]"
        )

        for element in group_elements:
            if saved_count >= max_groups:
                break

            try:
                group_url = element.get_attribute("href")
                if not group_url or "facebook.com/groups/" not in group_url:
                    continue

                if group_url in processed_groups:
                    continue
                processed_groups.add(group_url)

                # Проверка, есть ли группа в БД
                exists = session.query(Group).filter_by(url=group_url).first()
                if exists:
                    print(f"⚠️ Already in DB: {group_url}")
                    continue

                # Сохраняем в БД
                group = Group(url=group_url)
                session.add(group)
                session.commit()
                saved_count += 1
                print(f"✅ Saved group {saved_count}: {group_url}")

            except Exception as e:
                print(f"❌ Error saving group: {e}")
                continue

        # Скроллим вниз, чтобы загрузились новые группы
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(2)

    session.close()
    return saved_count




def join_groups(driver, max_groups=50):
    joined_count = 0
    scroll_attempts = 0
    max_scroll_attempts = 50
    processed_groups = set()

    while joined_count < max_groups and scroll_attempts < max_scroll_attempts:
        group_elements = driver.find_elements(
            By.XPATH,
            "//a[contains(@href, '/groups/') and not(contains(@href, 'search'))]"
        )
        print(f"🔍 Found {len(group_elements)} group links on page")

        new_groups_found = False

        for group_element in group_elements:
            if joined_count >= max_groups:
                break

            try:
                group_url = group_element.get_attribute("href")
                if not group_url or "facebook.com/groups/" not in group_url:
                    continue

                if group_url in processed_groups:
                    continue
                processed_groups.add(group_url)

                print(f"➡️ Checking group: {group_url}")

                # скролл к группе
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", group_element)
                time.sleep(random.uniform(1.0, 2.0))

                # ждём кнопку Join
                try:
                    join_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//span[text()='Join']/ancestor::div[@role='button']"
                        ))
                    )
                except:
                    join_button = None

                if join_button:
                    ActionChains(driver).move_to_element(join_button).click().perform()
                    print(f"✅ Joined group {joined_count + 1}: {group_url}")
                    joined_count += 1
                    new_groups_found = True

                    save_group_to_db(group_url)  # запись в БД

                    time.sleep(random.uniform(1.5, 3.5))
                else:
                    print("⚠️ No join button (maybe already joined)")

            except Exception as e:
                print(f"❌ Error processing group: {e}")
                continue

        if new_groups_found:
            scroll_attempts = 0
        else:
            driver.execute_script("window.scrollBy(0, arguments[0]);", random.randint(600, 1200))
            scroll_attempts += 1
            print(f"📜 Scrolled down ({scroll_attempts}/{max_scroll_attempts})")
            time.sleep(random.uniform(1.5, 2.5))

    return joined_count


