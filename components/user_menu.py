from playwright.sync_api import Page

from pages.base_page import BasePage


class UserMenu(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self._user_dropdown = page.locator(".oxd-userdropdown-name")
        self._dropdown_menu = page.locator(".oxd-dropdown-menu")

    def open(self) -> None:
        self.click(self._user_dropdown,"User Dropdown")

    def logout(self) -> None:
        self.open()
        logout_option = self._dropdown_menu.get_by_text("Logout",exact=True)
        self.click(logout_option,"Logout")

    def open_about(self) -> None:
        self.open()
        about_option = self._dropdown_menu.get_by_text("About",exact=True)
        self.click(about_option,"About")

    def open_support(self) -> None:
        self.open()
        support_option = self._dropdown_menu.get_by_text("Support",exact=True)
        self.click(support_option,"Support")

    def open_change_password(self) -> None:
        self.open()
        change_password_option = self._dropdown_menu.get_by_text("Change Password",exact=True)
        self.click(change_password_option,"Change Password")