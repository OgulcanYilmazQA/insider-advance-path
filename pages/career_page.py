import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

# Logger tanımı
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CareerPage(BasePage):
    """ Initialize career page with driver and default timeout.

    :param driver: Selenium WebDriver instance
    :param int timeout: Maximum wait time for element actions"""

    COOKIE_ACCEPT = "//*[@id='wt-cli-accept-all-btn']"
    LOCATIONS_XPATH = "//*[@id='career-our-location']/div/div/div/div[1]"
    TEAMS_PATH = "//*[@id='career-find-our-calling']/div/div/a"
    LIFE_AT_INSIDER = "//h2[contains(text(), 'Life at Insider')]"
    SEE_ALL_TEAMS = "//a[contains(text(), 'See all teams')]"
    QA_CAREER = "//h3[contains(text(), 'Quality Assurance')]"
    QA_OPEN_POSITIONS = "//h3[contains(text(), 'Quality Assurance')]/following-sibling::a[contains(text(), 'Open Positions')]"

    def __init__(self, driver):
        super().__init__(driver)
        self.check()

    def check(self):
        """Checks visibility of critical locators to confirm page integrity."""
        try:
            logger.info("Running initial checks for critical elements...")
            self.wait_for_element(By.XPATH, self.LOCATIONS_XPATH)
            self.wait_for_element(By.XPATH, self.TEAMS_PATH)
            self.wait_for_element(By.XPATH, self.LIFE_AT_INSIDER)
            logger.info("All critical elements are visible.")
        except Exception as e:
            logger.error(f"Critical element not found during check: {e}")
            raise

    def is_accessible(self):
        """
        Verifies if the Careers page is accessible.
        :return: True if title or URL contains career-related keywords, else False
        """
        try:
            logger.info("QA page title check")
            self.wait_for_page_to_load()
            title = self.driver.title.lower()
            url = self.driver.current_url.lower()
            logger.debug(f"QA Page Title: {title}")
            logger.debug(f"QA Page URL: {url}")
            return "careers" in title or "quality assurance" in title or "/careers" in url
        except Exception as e:
            logger.error(f"QA page error: {e}")
            return False

    def verify_sections(self):
        """
        Verifies the presence of key sections: Locations, Teams, and Life at Insider.
        :return: True if all sections are found, else False
        """
        try:
            logger.info("Waiting for Location part...")
            self.wait_for_element(By.XPATH, self.LOCATIONS_XPATH)
            logger.info("Locations part found!")

            logger.info("Waiting for Teams part...")
            self.wait_for_element(By.XPATH, self.TEAMS_PATH)
            logger.info("Teams part found!")

            self.wait_for_element(By.XPATH, self.LIFE_AT_INSIDER)
            logger.info("Life at Insider part found!")

            return True
        except Exception as e:
            logger.error(f"Error: Element could not be found: {e}")
            return False

    def go_to_qa_careers(self):
        """
        Navigates to the QA Careers page, using fallback methods if necessary.
        :raises Exception: If navigation fails
        """
        try:
            logger.info("Waiting for 'See All Teams' button...")
            see_all_teams_button = self.wait_for_element_to_be_clickable(By.XPATH, self.SEE_ALL_TEAMS)

            self.scroll_to_element(By.XPATH, self.SEE_ALL_TEAMS)
            time.sleep(1)
            self.scroll_to_element(By.XPATH, self.SEE_ALL_TEAMS)
            time.sleep(1)

            see_all_teams_button.click()
            logger.info("'See All Teams' button clicked.")

            logger.info("Waiting for page load...")
            self.wait_for_page_to_load()
            time.sleep(2)

            logger.info("'QA Careers' button checked...")
            self.scroll_to_element(By.XPATH, self.QA_CAREER)
            time.sleep(1)

            qa_careers_section = self.wait_for_element(By.XPATH, self.QA_CAREER)
            qa_open_link = self.wait_for_element_to_be_clickable(By.XPATH, self.QA_OPEN_POSITIONS)

            if qa_open_link:
                logger.info("Clicking on the 'Open Positions' button")
                self.scroll_to_element(By.XPATH, self.QA_OPEN_POSITIONS)
                time.sleep(1)
                qa_open_link.click()
                logger.info("Changed to the 'QA Careers' page.")
            else:
                logger.warning("Link not found, clicking with JavaScript")
                self.driver.execute_script("arguments[0].click();", qa_careers_section)
                logger.info("'QA Careers' button clicked with JS.")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
            )
        except Exception as e:
            logger.error(f"'QA Careers' page could not be found: {e}")
