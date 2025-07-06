
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def check_slots_and_book():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://seller.wildberries.ru/")
        time.sleep(2)

        login = os.getenv("WB_LOGIN")
        password = os.getenv("WB_PASSWORD")
        driver.find_element(By.NAME, "email").send_keys(login)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(5)

        driver.get("https://seller.wildberries.ru/fbo/slots")
        time.sleep(5)

        slots = driver.find_elements(By.CLASS_NAME, "slot-free")
        if slots:
            slots[0].click()
            return "✅ Найден свободный слот и забронирован!"
        else:
            return "⏳ Свободных слотов пока нет."

    except Exception as e:
        return f"Ошибка: {e}"
    finally:
        driver.quit()
