
new_checker = '''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
import os

COOKIES_FILE = "cookies.pkl"

def login_and_save_cookies(driver):
    driver.get("https://seller.wildberries.ru/")
    input("🔐 Введи СМС-код вручную в открывшемся окне, потом нажми Enter здесь...")

    # Сохраняем куки после входа
    with open(COOKIES_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("✅ Куки сохранены. Теперь бот может работать автоматически.")

def load_cookies(driver):
    if not os.path.exists(COOKIES_FILE):
        return False
    with open(COOKIES_FILE, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    return True

def check_slots_and_book():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://seller.wildberries.ru/")
        time.sleep(2)

        # Пытаемся загрузить куки
        if os.path.exists(COOKIES_FILE):
            driver.get("https://seller.wildberries.ru/")
            time.sleep(2)
            load_cookies(driver)
            driver.refresh()
            time.sleep(3)
        else:
            login_and_save_cookies(driver)
            return "✅ Первый вход выполнен. Куки сохранены."

        driver.get("https://seller.wildberries.ru/fbo/slots")
        time.sleep(5)

        slots = driver.find_elements(By.CLASS_NAME, "slot-free")
        if slots:
            slots[0].click()
            return "✅ Найден свободный слот и забронирован!"
        else:
            return "⏳ Свободных слотов пока нет."

    except Exception as e:
        return f"❌ Ошибка: {e}"
    finally:
        driver.quit()
'''

checker_path = "/mnt/data/checker.py"
with open(checker_path, "w", encoding="utf-8") as f:
    f.write(new_checker)

checker_path
