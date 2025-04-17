import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import chromedriver_autoinstaller

from pages.home_page import HomePage
from pages.career_page import CareerPage
from pages.qa_page import QaPage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InsiderCareerPageTest(unittest.TestCase):

    def setUp(self):
        self.browsers = ["chrome", "firefox"]
        self.driver = None

    def init_driver(self, browser):
        if browser == "chrome":
            chromedriver_autoinstaller.install()  # Otomatik uyumlu chromedriver yükler
            driver = webdriver.Chrome()
        elif browser == "firefox":
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.maximize_window()
        return driver

    def test_insider_career_page(self):
        for browser in self.browsers:
            with self.subTest(browser=browser):
                self.driver = self.init_driver(browser)
                # 1. Open Insider website
                logger.info("🚀 1. Open Insider website")
                page_home = HomePage(self.driver)
                self.assertTrue(page_home.is_accessible(), "Homepage not accessible")
                page_home.accept_cookies()

                # 2. Redirect to the Career page
                logger.info("➡️ 2. Redirect to the Career page")
                page_home.navigate_to_careers()
                careers_page = CareerPage(self.driver)
                self.assertTrue(careers_page.is_accessible(), "Career page not accessible")
                self.assertTrue(careers_page.verify_sections(), "Career sections verification failed")

                # 3. Redirecting to the QA Careers page
                logger.info("➡️ 3. Redirecting to the QA Careers page")
                careers_page.go_to_qa_careers()
                qa_page = QaPage(self.driver)
                self.assertTrue(qa_page.is_accessible(), "QA Careers page not accessible")

                # 4. Click "See all QA jobs"
                qa_page.click_see_all_qa_jobs()

                # 5. Filter jobs by QA department and Istanbul location
                qa_page.select_location_if_department_is_qa()
                qa_page.wait_for_job_cards_to_be_replaced()
                qa_page.wait_for_job_cards_to_load()

                # 6. Verify QA job listings
                self.assertTrue(qa_page.verify_job_listings(), "QA job listings do not match expected criteria")

                # 7. Check 'View Role' redirection
                self.assertTrue(qa_page.verify_view_role_redirects(), "'View Role' button redirection failed")

                logger.info("All QA career page tests completed successfully")

    def tearDown(self):
        if self.driver:
            self.driver.quit()
