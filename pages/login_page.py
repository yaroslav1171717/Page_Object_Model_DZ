import allure
from pages.base_page import BasePage

class LoginPage(BasePage):
    PATH = '/#/login'

    _USERNAME = "//input[@id='username']"
    _PASSWORD = "//input[@id='password']"
    _BUTTON_SIGN_IN = "//button[text()='Sign in']"

    @allure.step("Ввод логина и пароля на странице Авторизации")
    def authorization(self, login, password):
        """
        Проверка значения на соответствие
        :param login: логин
        :param password: пароль
        """
        login_element = self.wait.until(self.EC.visibility_of_element_located(self._USERNAME))
        password_element = self.wait.until(self.EC.visibility_of_element_located(self._PASSWORD))
        sign_in_element = self.wait.until(self.EC.visibility_of_element_located(self._BUTTON_SIGN_IN))
        login_element.send_keys(login)
        password_element.send_keys(password)
        sign_in_element.click()


