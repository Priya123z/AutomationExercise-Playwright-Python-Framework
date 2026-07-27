
from datetime import datetime

from playwright.sync_api import Page

from pages.base_page import BasePage



class Calendar(BasePage):
    MONTHS = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
              "September": 9, "October": 10, "November": 11, "December": 12}

    def __init__(self, page: Page, index: int):
        super().__init__(page)

        self._calendar = page.locator(".oxd-date-wrapper").nth(index)

        self._calendar_input = page.locator(".oxd-date-input-icon").nth(index)
        self._calendar_icon = page.locator(".oxd-date-input-icon").nth(index)

        self._month = page.locator(".oxd-calendar-selector-month-selected").nth(index)
        self._year = page.locator(".oxd-calendar-selector-year-selected").nth(index)

        self._previous_button = page.locator(".oxd-icon-button").first
        self._next_button = page.locator(".oxd-icon-button").last

        self._dates = page.locator(".oxd-calendar-date")
        self._today_button = page.get_by_text("Today")
        self._clear_button = page.get_by_text("Clear")
        self._close_button = page.get_by_text("Close")


    def open(self) -> None:
        self.click(self._calendar_icon, "Calendar")

    def select(self, date: str) -> None:
        selected_date = datetime.strptime(date, "%Y-%m-%d")
        self.open()
        self._navigate_to_year(selected_date.year)
        self._navigate_to_month(selected_date.month)
        self._select_day(selected_date.day)

    def clear(self) -> None:
        self.click(self._clear_button, "Clear")

    def close(self) -> None:
        self.click(self._close_button, "Close")

    def _navigate_to_year(self, year: int) -> None:
        while True:
            current_year = int(self._year.inner_text())
            if current_year == year:
                break
            elif current_year < year:
                self.click(self._next_button, "Next Year")
            else:
                self.click(self._previous_button, "Previous Year")

    def _navigate_to_month(self, month: int)->None:
        while True:
            current_month = self.MONTHS[self._month.inner_text().strip()]
            if current_month == month:
                break
            elif current_month > month:
                self.click(self._previous_button, "Previous Month")
            else:
                self.click(self._next_button, "Next Month")

    def _select_day(self, day: int) -> None:

        count = self._dates.count()

        for index in range(count):

            current_date = self._dates.nth(index)

            if current_date.inner_text().strip() == str(day):
                self.click(current_date, f"Select Day {day}")

                return

        raise ValueError(f"Day '{day}' not found in calendar")