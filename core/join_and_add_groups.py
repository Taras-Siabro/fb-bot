import time
from selenium.webdriver.common.by import By
from db.database import add_group


def join_all_groups_from_search(driver):
    """Скроллим страницу поиска и вступаем во все группы"""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        groups = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/')]")

        for g in groups:
            try:
                name = g.text.strip()
                url = g.get_attribute("href")

                # ищем кнопку "Join"
                join_button = g.find_element(By.XPATH, ".//span[text()='Join']")
                join_button.click()
                print(f"✅ Вступил в группу: {name}")

                # добавляем в БД
                add_group(name, url)

                time.sleep(2)

            except Exception:
                continue

        # скроллим вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # дошли до конца
            break
        last_height = new_height
