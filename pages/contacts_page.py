import allure

from pages.base_page import BasePage


class ContactPage(BasePage):
    PATH = '/#/contacts'

    _CONTACTS_LIST = "//li[contains(@class, 'MuiListItem-container')]"
    _TEXT_FIELD = "//textarea"
    _BUTTON_ADD_TEXT = "//button[text()='Add this note']"
    _TEXT_ENTERED = "//p[contains(@class, 'MuiBox-root')]"

    @allure.step("Открываем контакт по имени")
    def open_contact_by_name(self, name):
        contact_element_locator = ("xpath", f"//li[.//span[text()='{name}']]")
        contact = self.wait.until(self.EC.element_to_be_clickable(contact_element_locator))
        contact.click()

    @allure.step("Ввод текста на страница выбранного контакта")
    def entering_text_in_contact(self, text):
        text_field = self.wait.until(self.EC.visibility_of_element_located(self._TEXT_FIELD))
        text_field.send_keys(text)
        self.wait.until(self.EC.element_to_be_clickable(self._BUTTON_ADD_TEXT)).click()

    @allure.step("Получаем введенный тест со страница выбранного контакта")
    def return_text_from_contact(self):
        self.driver.refresh()
        text_element = self.wait.until(self.EC.visibility_of_element_located(self._TEXT_ENTERED))
        return text_element.text

