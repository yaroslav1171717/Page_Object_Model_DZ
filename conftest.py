import os
import pytest
from selenium import webdriver
import requests  # библиотека для HTTP-запросов
import pytest     # фреймворк для тестирования
import datetime   # модуль для работы с датой и временем

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

# Нотификационный бот для Telegram, размещать лучше здесь в conftest
# Токен бота Telegram для отправки сообщений
TOKEN = "8350224918:AAE8PTGknxskZOwG6LESrS424fIf_sVbxA0"
# Идентификатор чата в Telegram, куда отправлять результаты
CHAT_ID = "1778765155"
# Базовый URL для ссылки на файлы репозитория на GitLab
GITHUB_PAGE_URL = ("https://github.com/yaroslav1171717/Page_Object_Model_DZ/actions/workflows/pages/"
                   "pages-build-deployment")

def pytest_terminal_summary(terminalreporter):
    """
    Хук pytest, выполняющийся после завершения всех тестов.
    Собирает статистику по результатам и отправляет сводку в Telegram.
    """

    config = terminalreporter.config   # Это нужно для того чтобы хук не срабатывал повторно в каждом потоке запуска тестов, при параллельном запуске (n=4) ->
    if hasattr(config, "workerinput"):  # Т.е. это для того, чтобы отчет отправился только 1 раз по завершении всех тестов
        return

    # Фиксируем время запуска сборки (под конец, хотя обычно это начало)
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Структура для хранения агрегированных результатов по каждому файлу тестов
    suite_results = {}  # заранее создаем словарь, в которой будем добавлять результаты тестов, а потом из него создавать сообщение для телеграмма

    # Проходим по всем результатам, которые pytest сохранил в terminalreporter.stats
    for outcome, reports in terminalreporter.stats.items():
        # Здесь для данного проекта получается 2 итерации, в первой для каждого теста почему-то по 2 раза результат написан в reports, но outcome пустой, и поэтому ->
        # ниже, где +=1 мы не добавляем счетчики, т.к. не подходит ни под одно условие (passed и т.д.). А во второй итерации нормально по 1 разу для каждого теста ->
        # результат и outcome заполнен, поэтому нормально добавляется в каждый файл теста по 1 пройденному тесту (всего 4 теста). НО предполагаю что outcome надо ->
        # брать в цикле ниже, потому что в этом цикле мы берем какой-то общий outcome, а ниже перебираем reports, и там в каждом написан результат теста, пример: ->
        # TestReport 'tests/login_test.py::TestLogin::test_authorization' when='call' outcome='passed'>
        for report in reports:
            # в report.nodeid выглядит как: test_users.py::TestUser::test_create_user
            # в outcome статусы "passed" / "failed" / "skipped" / "error"
            suite_name = report.nodeid.split("::")[0]  # вытаскиваем только имя файла тестов - test_users.py

            # Если встретился новый файл тестов, создаем в словаре suite_results соответсвующий ключ и значением является словарь со результатами тестов
            if suite_name not in suite_results and outcome in ("passed", "failed", "skipped", "error"):
            # Добавил условие после and, т.к. первый раз во внешнем цикле когда идем там outcome пустой и там почему-то все тестовые файлы, в том числе и те, ->
            # которые не попали в выборку по запуску тестов (например по маркеру), и в отчете в телеграмм получался в том числе набор тестов с пустыми результатами
                suite_results[suite_name] = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0}

            # Увеличиваем соответствующий счётчик
            if outcome == "passed":
                suite_results[suite_name]["passed"] += 1
            elif outcome == "failed":
                suite_results[suite_name]["failed"] += 1
            elif outcome == "skipped":
                suite_results[suite_name]["skipped"] += 1
            elif outcome == "error":
                suite_results[suite_name]["errors"] += 1

    # Формируем текст сообщения для Telegram
    message = f"*РЕЗУЛЬТАТЫ ТЕСТОВ:*\n*Время запуска:* {start_time}\n\n"
    for suite, results in suite_results.items():
        message += (
            f"*Набор тестов:* `{suite}`\n"
            f"✅ *Пройдено:* {results['passed']}\n"
            f"❌ *Не пройдено:* {results['failed']}\n"
            f"⏭ *Пропущено:* {results['skipped']}\n"
            f"⚠️ *Ошибки:* {results['errors']}\n"
            f"-----------------------------\n\n"
        )

    # Добавляем ссылку на GitLab
    message += f"[Подробнее на GitHub Pages]({GITHUB_PAGE_URL})"  # Markdown позволяет создавать гиперссылки следующим образом: [текст ссылки](URL)
    # Python сам по себе не поддерживает вывод Markdown непосредственно в консоль, но есть специальные библиотеки, такие как rich, markdown для этого и текст
    # выведется в консоль с поддержкой Markdownё
    try:
        # Отправляем POST-запрос к Telegram Bot API
        response = requests.post(
            url=f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            headers={"Content-Type": "application/json"},
            json={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
        )
        # Проверяем, нет ли ошибок в ответе
        response.raise_for_status()  # Этот метод проверяет статус HTTP-ответа, если ошибка (4xx или 5xx), метод вызывает исключение requests.HTTPError, и мы ->
                                                                                                                        # можем обработать эту ошибку
    except requests.RequestException as e:  # а requests.RequestException базовый класс для всех исключений библиотеки Requests и это лучшая практика ловить ->
                        # наиболее общий класс исключений, охватывающий большинство потенциальных проблем, чтобы обеспечить надежность обработки ошибок
        if e.response is not None:      # Если запрос не удался, выводим содержимое ответа для отладки, переменная e сохраняет экземпляр исключения, ->
            print("Ответ Телеграмма:", e.response.json())  # вызванного при выполнении запроса. У экземпляра e имеется свойство response, которое содержит ->
            # объект ответа (если таковой имел место - мы проверяем). Методом e.response.json() мы извлекаем тело ответа в формате JSON, чтобы увидеть ->
            # подробную информацию об ошибке. (Свойство response доступно исключительно для объектов исключений, специфичных для библиотеки Requests, ->
            # а точнее, для классов, наследующих от requests.RequestException, все зависит от того с какой бибилиотекой работаем, зависит от реализации, ->
            # стандартные классы исключений Python (например, ValueError) не содержат специального атрибута response, а сторонние библиотеки могут иметь ->
            # собственные типы исключений, которые предоставляют уникальные атрибуты и методы)
