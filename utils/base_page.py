from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Tüm sayfa nesneleri için temel sınıf. Ortak işlemleri içerir.

    :param driver: Selenium WebDriver örneği
    :param int timeout: Varsayılan bekleme süresi (saniye)
    """

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(self, by, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.presence_of_element_located((by, locator)))

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.element_to_be_clickable((by, locator)))

    def click_element(self, by, locator):
        element = self.wait_for_element_to_be_clickable(by, locator)
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_element(self, by, locator):
        element = self.wait_for_element(by, locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def scroll_to_web_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def accept_cookies(self, cookie_xpath):
        cookie_button = self.wait_for_element_to_be_clickable(By.XPATH, cookie_xpath)
        cookie_button.click()

    def wait_for_page_to_load(self):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def get_element_text(self, by, locator):
        element = self.wait_for_element(by, locator)
        return element.text.strip()

    def wait_for_element_text_to_be(self, by, locator, expected_text, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element((by, locator), expected_text))
