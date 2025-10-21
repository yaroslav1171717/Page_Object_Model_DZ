import pytest
import allure
from tests.base_test import BaseTest

@allure.epic("Тренировочный проект на https://release-crm.qa-playground.com")
@allure.parent_suite("Тренировочный проект на https://release-crm.qa-playground.com")
class TestLogin(BaseTest):

    @pytest.mark.smoke
    @allure.title("Тестирование авторизации")
    @allure.id("4")
    def test_authorization(self):
        self.contact_page.open_page()          # Открываем страницу контактов
        self.contact_page.exit_user()          # выходим из пользователя
        self.login_page.authorization(self.auth.LOGIN, self.auth.PASSWORD)      # Авторизуемся на странице логина
        assert self.login_page.check_url('https://release-crm.qa-playground.com/#/'), 'Авторизация не выполнена'  # Чекаем авторизацию
