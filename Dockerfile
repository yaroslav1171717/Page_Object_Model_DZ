FROM python:3.11.13-alpine3.22

# Установка Chrome
RUN apk update
RUN apk add --no-cache chromium chromium-chromedriver

# Установка зависимостей для Chrome
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk

# Установка Allure
RUN apk update && \
    apk add openjdk11-jre curl tar && \
    curl -o allure-2.13.8.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz && \
    tar -zxvf allure-2.13.8.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm allure-2.13.8.tgz

WORKDIR /usr/workspace
COPY ./requirements.txt /usr/workspace
RUN pip3 install -r requirements.txt

# CMD не пишем !!!, будем запускать код командой по типу docker run <IMAGE>:<TAG> sh -c "python code.py" или в docker-compose пропишем команду и будем уже
# его запускать через терминал или через CI/CD в пайплане

#Опции для драйвера в Docker - прописать в conftest:  !!!!!!!!!!!!

#options.add_argument("--headless")  # Запускает браузер в режиме без графического интерфейса (удобно для серверов)
#options.add_argument("--no-sandbox")  # Отключает режим песочницы для предотвращения проблем с правами доступа
#options.add_argument("--disable-dev-shm-usage")  # Отключает использование общей памяти /dev/shm (для Docker и серверных сред)
#options.add_argument("--disable-gpu")  # Отключает GPU, необходимое для headless-режима на некоторых системах
#options.add_argument("--window-size=1920,1080")  # Устанавливает фиксированный размер окна браузера

# Сборка:
# docker build -f Dockerfile -t pom_dz:v1 .

# Команда для запуска тестов в контейнере со связкой директории проекта (любые изменения в коде сразу сами подтянутся)
# docker run -it --rm -e STAGE=release -e BROWSER=chrome -v ./:/usr/workspace pom_dz:v1 sh -c "pytest -sv"    :
    # -v ./:/usr/workspace - таким образом связываем каталоги нашего проекта с рабочей директорией в контейнере
    # -it - интерактивный режим
    # --rm - удаляем контейнер после запуска
    # -e STAGE=release - указываем переменные окружения (вроде как, если не знаем какие нужны, можно просто запустить все командой pytest и посмотреть какие
    # ошибки будут. на что ругается, например KeyError: 'BASE_URL')
    # pom_dz:v1 - указали образ с тегом
    # sh -c "pytest -sv" - выполням команду для запуска тестов
    # sh -c "pytest -sv -k 'test_open_from_hot'" - для запуска конкретного теста (с поиском)(в одинарных кавычках имя теста или маркера)
# (в requirements стоял selenium==4.34.0, просто могут быть ошибки из-за версии Selenium)


