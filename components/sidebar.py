from playwright.sync_api import Page

from pages import leave_page
from pages.base_page import BasePage
from pages.leave_page import LeavePage


class Sidebar(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self._dashboard_menu = page.get_by_role("link", name="Dashboard")
        self._admin_menu = page.get_by_role("link", name="Admin")
        self._pim_menu = page.get_by_role("link", name="PIM")
        self._leave_menu = page.get_by_role("link", name="Leave")
        self._time_menu = page.get_by_role("link", name="Time")
        self._recruitment_menu = page.get_by_role("link", name="Recruitment")
        self._my_info_menu = page.get_by_role("link", name="My Info")
        self._performance_menu = page.get_by_role("link", name="Performance")
        self._directory_menu = page.get_by_role("link", name="Directory")
        self._maintenance_menu = page.get_by_role("link", name="Maintenance")
        self._claim_menu = page.get_by_role("link", name="Claim")
        self._buzz_menu = page.get_by_role("link", name="Buzz")

    def open_dashboard(self):
        self.click(self._dashboard_menu, "Dashboard Menu")
    def open_admin(self):
        self.click(self._admin_menu, "Admin Menu")
    def open_pim(self):
        self.click(self._pim_menu, "PIM Menu")
    def open_leave(self) -> LeavePage:
        self.click(self._leave_menu, "Leave Menu")
        leave_page = LeavePage(self.page)
        leave_page.is_loaded()
        return leave_page

    def open_time(self):
        self.click(self._time_menu, "Time Menu")
    def open_recruitment(self):
        self.click(self._recruitment_menu, "Recruitment Menu")
    def open_my_info(self):
        self.click(self._my_info_menu, "My Info Menu")
    def open_performance(self):
        self.click(self._performance_menu, "Performance Menu")
    def open_directory(self):
        self.click(self._directory_menu, "Directory Menu")
    def open_maintenance(self):
        self.click(self._maintenance_menu, "Maintenance Menu")
    def open_claim(self):
        self.click(self._claim_menu, "Claim Menu")
    def open_buzz(self):
        self.click(self._buzz_menu, "Buzz Menu")