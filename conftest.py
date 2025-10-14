import os
import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920,1080")   # Эта тоже нужна для Docker и нам просто нужно
    options.add_argument("--user-agent=AQA Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    options.add_argument("--disable-cache")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Опции для Docker:
    options.add_argument("--headless")  # Запускает браузер в режиме без графического интерфейса (удобно для серверов)
    options.add_argument("--no-sandbox")  # Отключает режим песочницы для предотвращения проблем с правами доступа
    options.add_argument(
        "--disable-dev-shm-usage")  # Отключает использование общей памяти /dev/shm (для Docker и серверных сред)
    options.add_argument("--disable-gpu")  # Отключает GPU, необходимое для headless-режима на некоторых системах
    # До сюда идут опции для Docker
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    browser = os.getenv('BROWSER', 'chrome')        # Если переменная не будет передана, то используем значение по дефолту chrome
    driver = None
    if browser == 'chrome':
        driver = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        driver = webdriver.Firefox()
    request.cls.driver = driver
    yield
    driver.quit()

