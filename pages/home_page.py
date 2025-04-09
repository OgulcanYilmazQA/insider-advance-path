from selenium.webdriver.common.by import By
from .base_page import base_page


class home_page(base_page):
    # Locator definitions
    URL = "https://useinsider.com"
    COOKIE_BUTTON = "//*[@id='wt-cli-accept-all-btn']"
    COMPANY_MENU = "(//*[@id='navbarDropdownMenuLink'])[5]"
    CAREERS_LINK = "//*[@id='navbarNavDropdown']/ul[1]/li[6]/div/div[2]/a[2]"

    def __init__(self, driver):
        """
        HomePage constructor.

        :param driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.check()

    def check(self):
        """
        Checks visibility of critical elements on the home page.

        :raises Exception: If any critical element is not visible
        """
        try:
            print("✅ Running initial checks for critical elements on Home Page...")
            self.wait_for_element(By.XPATH, self.COOKIE_BUTTON)
            self.wait_for_element(By.XPATH, self.COMPANY_MENU)
            print("✅ Critical elements on Home Page are visible.")
        except Exception as e:
            print(f"❌ Home Page critical element not found: {e}")
            raise

    def open(self):
        """
        Opens the Insider homepage.
        """
        self.driver.get(self.URL)

    def is_accessible(self):
        """
        Checks whether the homepage is accessible by verifying the title.

        :return: True if title contains 'Insider', else False
        """
        return "Insider" in self.driver.title

    def accept_cookies(self):
        """
        Accepts cookies using BasePage method.
        """
        super().accept_cookies(self.COOKIE_BUTTON)

    def navigate_to_careers(self):
        """
        Navigates to the Careers page through the Company menu.
        """
        self.click_element(By.XPATH, self.COMPANY_MENU)
        self.click_element(By.XPATH, self.CAREERS_LINK)
