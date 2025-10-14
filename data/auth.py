import os
from dotenv import load_dotenv

load_dotenv()   # ищет файл .env в корневой директории вашего проекта и добавляет указанные там переменные среды в окружение программы

class Auth:

    if os.environ['STAGE'] == 'release':
        LOGIN = os.getenv("RELEASE_LOGIN")
        PASSWORD = os.getenv("RELEASE_PASSWORD")
    elif os.environ['STAGE'] == 'qa':
        LOGIN = os.getenv("QA_LOGIN")
        PASSWORD = os.getenv("QA_PASSWORD")

