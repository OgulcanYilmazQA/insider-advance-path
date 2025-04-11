import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.base_page import BasePage

class CareerPage(BasePage):
    """Career Page: Handles key actions and verifications on the page."""

    COOKIE_ACCEPT = "//*[@id='wt-cli-accept-all-btn']"
    LOCATIONS_XPATH = "//*[@id='career-our-location']/div/div/div/div[1]"
    TEAMS_PATH = "//*[@id='career-find-our-calling']/div/div/a"
    LIFE_AT_INSIDER = "//h2[contains(text(), 'Life at Insider')]"
    SEE_ALL_TEAMS = "//a[contains(text(), 'See all teams')]"
    QA_CAREER = "//h3[contains(text(), 'Quality Assurance')]"
    QA_OPEN_POSITIONS = "//h3[contains(text(), 'Quality Assurance')]/following-sibling::a[contains(text(), 'Open Positions')]"

    def __init__(self, driver):
        super().__init__(driver)
        self._verify_page_loaded()

    def _verify_page_loaded(self):
        """Verifies that key page elements are loaded and visible."""
        self.wait_for_element(By.XPATH, self.LOCATIONS_XPATH)
        self.wait_for_element(By.XPATH, self.TEAMS_PATH)
        self.wait_for_element(By.XPATH, self.LIFE_AT_INSIDER)

    def is_accessible(self):
        """Checks if the page is accessible by validating the title or URL."""
        self.wait_for_page_to_load()
        title = self.driver.title.lower()
        url = self.driver.current_url.lower()
        return "careers" in title or "quality assurance" in title or "/careers" in url

    def verify_sections(self):
        """Checks visibility of Locations, Teams, and Life at Insider sections."""
        self.wait_for_element(By.XPATH, self.LOCATIONS_XPATH)
        self.wait_for_element(By.XPATH, self.TEAMS_PATH)
        self.wait_for_element(By.XPATH, self.LIFE_AT_INSIDER)
        return True

    def go_to_qa_careers(self):
        """Navigates to the QA Careers section and clicks on the Open Positions link."""
        self.scroll_to_element(By.XPATH, self.SEE_ALL_TEAMS)
        time.sleep(1)

        self.click_element(By.XPATH, self.SEE_ALL_TEAMS)
        self.wait_for_page_to_load()
        time.sleep(2)

        self.scroll_to_element(By.XPATH, self.QA_CAREER)
        time.sleep(1)

        qa_open_link = self.wait_for_element_to_be_clickable(By.XPATH, self.QA_OPEN_POSITIONS)
        self.scroll_to_element(By.XPATH, self.QA_OPEN_POSITIONS)
        time.sleep(1)

        qa_open_link.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'See all QA jobs')]")))
