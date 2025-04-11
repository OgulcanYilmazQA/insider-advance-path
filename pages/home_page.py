from selenium.webdriver.common.by import By
from utils.base_page import BasePage

class HomePage(BasePage):
    """Home Page: Defines core actions for the main landing page."""

    URL = "https://useinsider.com"
    COOKIE_BUTTON = "//*[@id='wt-cli-accept-all-btn']"
    COMPANY_MENU = "(//*[@id='navbarDropdownMenuLink'])[5]"
    CAREERS_LINK = "//*[@id='navbarNavDropdown']/ul[1]/li[6]/div/div[2]/a[2]"

    def __init__(self, driver):
        super().__init__(driver)
        self.navigate_to_home_page()

    def navigate_to_home_page(self):
        """Verifies that critical homepage elements are present."""
        self.wait_for_element(By.XPATH, self.COOKIE_BUTTON)
        self.wait_for_element(By.XPATH, self.COMPANY_MENU)

    def open(self):
        """Navigates to the Insider homepage."""
        self.driver.get(self.URL)

    def is_accessible(self):
        """Checks if homepage is accessible by verifying the title."""
        return "insider" in self.driver.title.lower()

    def accept_cookies(self):
        """Accepts cookies using the BasePage helper method."""
        super().accept_cookies(self.COOKIE_BUTTON)

    def navigate_to_careers(self):
        """Navigates to the Careers page through the Company dropdown."""
        self.click_element(By.XPATH, self.COMPANY_MENU)
        self.click_element(By.XPATH, self.CAREERS_LINK)
