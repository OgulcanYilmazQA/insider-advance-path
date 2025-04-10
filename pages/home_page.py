import logging
from selenium.webdriver.common.by import By
from .base_page import BasePage

# Logger tanımı
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HomePage(BasePage):
    """
    Initialize home page with driver and default timeout.

    :param driver: Selenium WebDriver instance
    :param int timeout: Maximum wait time for element actions
    """
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
        self.navigate_to_home_page()

    def navigate_to_home_page(self):
        """
        Checks visibility of critical elements on the home page.

        :raises Exception: If any critical element is not visible
        """
        try:
            logger.info("Running initial checks for critical elements on Home Page...")
            self.wait_for_element(By.XPATH, self.COOKIE_BUTTON)
            self.wait_for_element(By.XPATH, self.COMPANY_MENU)
            logger.info("Critical elements on Home Page are visible.")
        except Exception as e:
            logger.error(f"Home Page critical element not found: {e}")
            raise

    def open(self):
        """
        Opens the Insider homepage.
        """
        logger.info("Opening Insider homepage...")
        self.driver.get(self.URL)

    def is_accessible(self):
        """
        Checks whether the homepage is accessible by verifying the title.

        :return: True if title contains 'Insider', else False
        """
        accessible = "Insider" in self.driver.title
        logger.info(f"Homepage accessibility check: {'Accessible' if accessible else 'Not Accessible'}")
        return accessible

    def accept_cookies(self):
        """
        Accepts cookies using BasePage method.
        """
        logger.info("Attempting to accept cookies...")
        super().accept_cookies(self.COOKIE_BUTTON)

    def navigate_to_careers(self):
        """
        Navigates to the Careers page through the Company menu.
        """
        logger.info("Navigating to Careers page...")
        self.click_element(By.XPATH, self.COMPANY_MENU)
        self.click_element(By.XPATH, self.CAREERS_LINK)
