import allure
from pages.base_page import BasePage

class DealsPage(BasePage):
    PATH = '/#/deals'

    _TEXT_FIELD = "//textarea[@rows='3']"
    _BUTTON_ADD_THIS_NOTE = "//button[text()='Add this note']"
    _TEXT_ENTERED_IN_DEALS = "//p[contains(@class, 'MuiBox-root')]"

    @allure.step("Открываем сделку по ее имени на странице Сделок")
    def open_deals_by_name(self, name):
        deals_element_locator = ("xpath", f"//p[text()='{name}']")
        contact = self.wait.until(self.EC.element_to_be_clickable(deals_element_locator))
        contact.click()

    @allure.step("Ввод текста в выбранную сделку на странице Сделок")
    def entering_text_in_deals(self, text):
        text_field = self.wait.until(self.EC.visibility_of_element_located(self._TEXT_FIELD))
        text_field.send_keys(text)
        self.wait.until(self.EC.element_to_be_clickable(self._BUTTON_ADD_THIS_NOTE)).click()

    @allure.step("Получаем введенный текст в сделке на странице Сделок")
    def return_text_from_deals(self):
        self.driver.refresh()
        self.wait.until(self.EC.visibility_of_element_located(self._TEXT_ENTERED_IN_DEALS))
        elements_with_text = self.driver.find_elements(*self._TEXT_ENTERED_IN_DEALS)
        text_element = elements_with_text[0].text
        return text_element

