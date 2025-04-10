from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


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
            print(f"❌ Error: {locator} element not found.")
            return None

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            print(f"❌ Error: {locator} element is not clickable.")
            return None

    def click_element(self, by, locator):
        element = self.wait_for_element_to_be_clickable(by, locator)
        if element:
            try:
                element.click()
                print(f"✅ Click Success: {locator}")
            except Exception:
                print(f"⚠️ Selenium could not clicked, Clicking with JavaScript: {locator}")
                self.driver.execute_script("arguments[0].click();", element)
        else:
            print(f"⚠️ Warning: {locator} element could not clicked.")

    def scroll_to_element(self, by, locator):
        element = self.wait_for_element(by, locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            print(f"🔽 Page scrolled: {locator}")
        else:
            print(f"⚠️ Warning: {locator} couldn't scroll, element not found.")

    def scroll_to_web_element(self, element):
        """
        Scrolls the given WebElement into view.

        :param element: WebElement instance
        """
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            print("🔽 Page scrolled to element (via WebElement).")
        else:
            print("⚠️ Warning: Provided WebElement is None, cannot scroll.")

    def accept_cookies(self, cookie_xpath):
        try:
            print("🔄 Cookies")
            cookie_button = self.wait_for_element_to_be_clickable(By.XPATH, cookie_xpath)
            if cookie_button:
                cookie_button.click()
                print("✅ Cookies accepted!")
            else:
                print("⚠️ Cookies not found.")
        except NoSuchElementException:
            print("⚠️ Cookie skipped.")

    def wait_for_page_to_load(self):
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            print("✅ Page done")
        except TimeoutException:
            print("⚠️ Page loading could not finish.")

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
            print(f"✅ Element text changed as '{expected_text}'.")
            return True
        except TimeoutException:
            actual_text = self.get_element_text(by, locator)
            print(f"❌ Error: Element text could not changed '{expected_text}'. Last change: '{actual_text}'")
            return False
