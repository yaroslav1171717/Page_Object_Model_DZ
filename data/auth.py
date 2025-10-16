import os
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv()
  # ищет файл .env в корневой директории вашего проекта и добавляет указанные там переменные среды в окружение программы, если существует .env, т.к. в GIT его нет

class Auth:
    if os.path.exists('.env'):                # Здесь также проверяем, если есть .env, то от туда берем данные, а если нет, то данные будут браться из ->
        if os.environ['STAGE'] == 'release':    # environment secret в GitHub, там для всех стендов переменные будут называться LOGIN и PASSWORD
            LOGIN = os.getenv("RELEASE_LOGIN")
            PASSWORD = os.getenv("RELEASE_PASSWORD")
        elif os.environ['STAGE'] == 'dev':
            LOGIN = os.getenv("DEV_LOGIN")
            PASSWORD = os.getenv("DEV_PASSWORD")
    else:
        LOGIN = os.getenv("LOGIN")
        PASSWORD = os.getenv("PASSWORD")

