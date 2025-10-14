from pages.dashboard_page import DashboardPage
from pages.contacts_page import ContactPage
from pages.login_page import LoginPage
from pages.deals_page import DealsPage
from data.auth import Auth
class BaseTest:

    def setup_method(self):
        self.dashboard_page = DashboardPage(self.driver)
        self.contact_page = ContactPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.deals_page = DealsPage(self.driver)
        self.auth = Auth()

