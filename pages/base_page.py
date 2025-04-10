import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# Logger tanımı
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BasePage:
    """
    Initialize BasePage with driver and default timeout.

    :param driver: Selenium WebDriver instance
    :param int timeout: Maximum wait time for element actions
    """

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(self, by, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            return None

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            logger.error(f"Element is not clickable: {locator}")
            return None

    def click_element(self, by, locator):
        element = self.wait_for_element_to_be_clickable(by, locator)
        if element:
            try:
                element.click()
                logger.info(f"Click Success: {locator}")
            except Exception:
                logger.warning(f"Selenium couldn't click, using JavaScript: {locator}")
                self.driver.execute_script("arguments[0].click();", element)
        else:
            logger.warning(f"Element could not be clicked: {locator}")

    def scroll_to_element(self, by, locator):
        element = self.wait_for_element(by, locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            logger.info(f"Page scrolled to: {locator}")
        else:
            logger.warning(f"Couldn't scroll to element, not found: {locator}")

    def scroll_to_web_element(self, element):
        """Scrolls the given WebElement into view."""
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            logger.info("Page scrolled to WebElement.")
        else:
            logger.warning("Provided WebElement is None, cannot scroll.")

    def accept_cookies(self, cookie_xpath):
        try:
            logger.info("Looking for cookie accept button...")
            cookie_button = self.wait_for_element_to_be_clickable(By.XPATH, cookie_xpath)
            if cookie_button:
                cookie_button.click()
                logger.info("Cookies accepted!")
            else:
                logger.warning("Cookie button not found.")
        except NoSuchElementException:
            logger.warning("Cookie button skipped due to NoSuchElementException.")

    def wait_for_page_to_load(self):
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            logger.info("Page fully loaded.")
        except TimeoutException:
            logger.warning("Page loading did not finish in time.")

    def get_element_text(self, by, locator):
        element = self.wait_for_element(by, locator)
        if element:
            return element.text.strip()
        return ""

    def wait_for_element_text_to_be(self, by, locator, expected_text, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, locator), expected_text)
            )
            logger.info(f"Element text changed to '{expected_text}'.")
            return True
        except TimeoutException:
            actual_text = self.get_element_text(by, locator)
            logger.error(f"Expected text '{expected_text}' not found. Current text: '{actual_text}'")
            return False
