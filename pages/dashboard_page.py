import allure

from pages.base_page import BasePage

class DashboardPage(BasePage):
    PATH = '/#/'

    _HOT_CONTACTS_LIST = "//li[.//p[contains(text(), 'ago')]]"
    _NAME_FROM_CONTACTS_LIST = ".//span/div[text()]"
    _DEALS_PIPELINE_LIST = "//li[.//p[contains(text(), '$')]]"
    _NAME_FROM_DEALS_LIST = ".//span/div[text()]"

    @allure.step("Открываем контакт выбранный по порядковому номеру в хот листе на странице Дашборда")
    def open_contact_from_hot_list_by_number(self, number):
        self.wait.until(self.EC.element_to_be_clickable(self._HOT_CONTACTS_LIST))
        elements_contact_list = self.driver.find_elements(*self._HOT_CONTACTS_LIST)
        elements_contact_list[number].click()

    @allure.step("Получаем имя контакта по его номеру в хот листе на странице Дашборда")
    def return_name_from_hot_list_by_number(self, number):
        self.wait.until(self.EC.element_to_be_clickable(self._HOT_CONTACTS_LIST))
        elements_contact_list = self.driver.find_elements(*self._HOT_CONTACTS_LIST)
        name_element = elements_contact_list[number].find_element(*self._NAME_FROM_CONTACTS_LIST)
        return name_element.text

    @allure.step("Открываем сделку по ее номеру на странице Дашборда")
    def open_deals_from_list_deals_by_number(self, number):
        self.wait.until(self.EC.element_to_be_clickable(self._DEALS_PIPELINE_LIST))
        elements_deals_list = self.driver.find_elements(*self._DEALS_PIPELINE_LIST)
        elements_deals_list[number].click()

    @allure.step("Получаем имя сделки по ее номеру на странице Дашборда")
    def return_name_from_deals_pipeline_by_number(self, number):
        self.wait.until(self.EC.element_to_be_clickable(self._DEALS_PIPELINE_LIST))
        elements_deals_list = self.driver.find_elements(*self._DEALS_PIPELINE_LIST)
        name_element = elements_deals_list[number].find_element(*self._NAME_FROM_DEALS_LIST)
        return name_element.text

