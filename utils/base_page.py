from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Base class for all page objects. Contains common actions and utilities.

    :param driver: Selenium WebDriver instance
    :param int timeout: Default wait time in seconds
    """

    def __init__(self, driver, timeout=20):
        """
        Constructor for BasePage. Initializes the WebDriver and wait object.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(self, by, locator, timeout=None):
        """
        Waits for the presence of an element located by the given selector.

        :param by: Locator strategy (e.g., By.ID, By.XPATH)
        :param locator: Locator value
        :param timeout: Optional custom timeout
        :return: WebElement if found, otherwise False
        """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            print(f"❌ ERROR: Element not found: {locator}")
            return False

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        """
        Waits until the specified element is clickable.

        :param by: Locator strategy
        :param locator: Locator value
        :param timeout: Optional custom timeout
        :return: WebElement if clickable, otherwise False
        """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            print(f"❌ ERROR: Element not clickable: {locator}")
            return False

    def click_element(self, by, locator):
        """
        Clicks on the specified element. Falls back to JavaScript click if needed.

        :param by: Locator strategy
        :param locator: Locator value
        """
        element = self.wait_for_element_to_be_clickable(by, locator)
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_element(self, by, locator):
        """
        Scrolls the page to bring the specified element into view.

        :param by: Locator strategy
        :param locator: Locator value
        """
        element = self.wait_for_element(by, locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def scroll_to_web_element(self, element):
        """
        Scrolls the page to bring the provided WebElement into view.

        :param element: WebElement object
        """
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def accept_cookies(self, cookie_xpath):
        """
        Clicks on the cookie acceptance button.

        :param cookie_xpath: XPath of the cookie acceptance button
        """
        cookie_button = self.wait_for_element_to_be_clickable(By.XPATH, cookie_xpath)
        cookie_button.click()

    def wait_for_page_to_load(self):
        """
        Waits until the page's readyState is 'complete'.
        """
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def get_element_text(self, by, locator):
        """
        Retrieves and returns the trimmed text of the specified element.

        :param by: Locator strategy
        :param locator: Locator value
        :return: Element's text as a string
        """
        element = self.wait_for_element(by, locator)
        return element.text.strip()

    def wait_for_element_text_to_be(self, by, locator, expected_text, timeout=10):
        """
        Waits until the specified element contains the expected text.

        :param by: Locator strategy
        :param locator: Locator value
        :param expected_text: Text to wait for
        :param timeout: Maximum wait time in seconds
        :return: True if text is found within timeout, raises TimeoutException otherwise
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element((by, locator), expected_text))
