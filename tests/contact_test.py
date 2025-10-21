import allure
import pytest
from tests.base_test import BaseTest

@allure.epic("Тренировочный проект на https://release-crm.qa-playground.com")
@allure.parent_suite("Тренировочный проект на https://release-crm.qa-playground.com")
class TestContact(BaseTest):

    @pytest.mark.regression
    @allure.title("Открытие контакта со страницы Дашборда, ввод текста и проверка ввода через страницу Контакты")
    @allure.id("1")
    def test_open_from_hot_contacts_and_enter_text_and_check(self):
        self.dashboard_page.open_page()                 # Открываем страницу dashboard
        name = self.dashboard_page.return_name_from_hot_list_by_number(0)   # Получаем имя первого контакта из топ-листа
        self.dashboard_page.open_contact_from_hot_list_by_number(0)   # выбираем первого контакта
        text = 'AutoTestContact'
        self.contact_page.entering_text_in_contact(text)  # вписываем тест
        self.contact_page.open_page()  # Открываем страницу contact
        self.contact_page.open_contact_by_name(name)   # Ищем клиента по полученному имени выше и открываем
        text_result = self.contact_page.return_text_from_contact()  # Получаем текст
        assert text_result == text, "Введенный текст не найден"

        # Запуск теста: $env:STAGE="release"; $env:BROWSER="chrome"; pytest -sv -k "test_open_from_hot_contacts_and_enter_text_and_check"
        #$env: BROWSER - НЕ обязательно для заполнения (по дефолту будет Chrome)


