import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from metaclasses.meta_locator import MetaLocator
from data.links import Links


class BasePage(metaclass=MetaLocator):
    _HEADER_MENU_DASHBOARD = "//a[text()='Dashboard']"
    _HEADER_MENU_CONTACTS = "//a[text()='Contacts']"
    _HEADER_MENU_COMPANIES = "//a[text()='Companies']"
    _HEADER_MENU_DEALS = "//a[text()='Deals']"
    _HEADER_MENU_CRM = "//a[text()='CRM']"
    _BUTTON_USER = "//button[@aria-label='Profile']"
    _LOGOUT_USER = "//span[text()='Logout']"
    _BUTTON_RESET_DB = "//button[@aria-label='Reset DB']"

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(self.driver, 10, 1)
        self.EC = EC

    def open_page(self):
        with allure.step(f"Открытие страницы {Links.HOST}{self.PATH}"):
            self.driver.get(f'{Links.HOST}{self.PATH}')   # клеим путь, PATH со страниц берем

    def open_page_in_menu_by_name(self, value_menu):
        with allure.step(f"Открываем меню {value_menu} в шапке"):
            menu_name = {
                'dashboard': self._HEADER_MENU_DASHBOARD,
                'contacts': self._HEADER_MENU_CONTACTS,
                'companies': self._HEADER_MENU_COMPANIES,
                'deals': self._HEADER_MENU_DEALS,
                'crm': self._HEADER_MENU_CRM
            }
            button_menu_element = self.wait.until(self.EC.element_to_be_clickable(menu_name[value_menu]))
            button_menu_element.click()

    @allure.step("Проверяем url")
    def check_url(self, url):
        return self.driver.current_url == url

    @allure.step("Разлогиниваемся из пользователя")
    def exit_user(self):
        button_user_element = self.wait.until(self.EC.element_to_be_clickable(self._BUTTON_USER))
        button_user_element.click()
        logout_element = self.wait.until(self.EC.element_to_be_clickable(self._LOGOUT_USER))
        logout_element.click()

