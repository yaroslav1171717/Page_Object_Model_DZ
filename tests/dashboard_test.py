import time
import allure
import pytest

from tests.base_test import BaseTest

@allure.epic("Тренировочный проект на https://release-crm.qa-playground.com")
@allure.parent_suite("Тренировочный проект на https://release-crm.qa-playground.com")
class TestDashboard(BaseTest):

    @pytest.mark.regression
    @allure.title("Проверка кнопок меню в шапке со страницы Дашборды")
    @allure.id("2")
    def test_open_menus_by_name(self):
        self.dashboard_page.open_page()
        self.dashboard_page.open_page_in_menu_by_name("contacts")
        assert self.dashboard_page.check_url("https://release-crm.qa-playground.com/#/contacts"), "Неверный url страницы"
        self.dashboard_page.open_page_in_menu_by_name("dashboard")
        assert self.dashboard_page.check_url("https://release-crm.qa-playground.com/#/"), "Неверный url страницы"
        self.dashboard_page.open_page_in_menu_by_name("companies")
        assert self.dashboard_page.check_url("https://release-crm.qa-playground.com/#/companies"), "Неверный url страницы"
        self.dashboard_page.open_page_in_menu_by_name("deals")
        assert self.dashboard_page.check_url("https://release-crm.qa-playground.com/#/deals"), "Неверный url страницы"
        self.dashboard_page.open_page_in_menu_by_name("crm")
        assert self.dashboard_page.check_url("https://release-crm.qa-playground.com/"), "Неверный url страницы"




