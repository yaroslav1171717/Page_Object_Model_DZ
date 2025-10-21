import allure
import pytest
from tests.base_test import BaseTest

@allure.epic("Тренировочный проект на https://release-crm.qa-playground.com")
@allure.parent_suite("Тренировочный проект на https://release-crm.qa-playground.com")
class TestDeals(BaseTest):

    @pytest.mark.regression
    @allure.title("Открытие сделки со страницы Дашборда, ввод текста и проверка ввода через страницу Сделок")
    @allure.id("3")
    def test_open_deals_and_add_note_and_check(self):
        self.dashboard_page.open_page()           # Открываем страницу dashboard
        name = self.dashboard_page.return_name_from_deals_pipeline_by_number(0)      # Получаем имя первой сделки
        self.dashboard_page.open_deals_from_list_deals_by_number(0)        # Открываем сделку
        text = 'AutoTestDeals'
        self.deals_page.entering_text_in_deals(text)                    # Вписываем текст
        self.deals_page.open_page()                                    # Открываем страницу deals
        self.deals_page.open_deals_by_name(name)                       # Открываем сделку по имени
        text_result = self.deals_page.return_text_from_deals()   # Получаем текст
        assert text_result == text, "Введенный текст не найден"
