import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pages.home_page import HomePage
from pages.career_page import CareerPage
from pages.qa_page import QaPage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InsiderCareerPageTest(unittest.TestCase):

    def setUp(self):
        self.browsers = ["chrome", "firefox"]

    def init_driver(self, browser):
        if browser == "chrome":
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        elif browser == "firefox":
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)
        driver.maximize_window()
        return driver

    def test_insider_career_page(self):
        for browser in self.browsers:
            with self.subTest(browser=browser):
                driver = self.init_driver(browser)
                try:
                    logger.info("🚀 Open Insider website")
                    page_home = HomePage(driver)
                    page_home.open()
                    self.assertTrue(page_home.is_accessible(), "❌ Error, page not found")

                    logger.info("✅ Cookies accepted")
                    page_home.accept_cookies()

                    logger.info("✅ Redirect to the Career page")
                    page_home.navigate_to_careers()
                    careers_page = CareerPage(driver)
                    self.assertTrue(careers_page.is_accessible(), "❌ Error: Career page not found")

                    logger.info("✅ Sayfa bölümleri kontrol ediliyor.")
                    self.assertTrue(careers_page.verify_sections(), "❌ Error: Careers section not correct!")

                    logger.info("✅ Redirecting to the QA Careers page.")
                    careers_page.go_to_qa_careers()
                    qa_careers_page = QaPage(driver)

                    logger.info("🔍 Checking for the QA Careers page.")
                    self.assertTrue(qa_careers_page.is_accessible(), "❌ Error: QA Careers page not found!")

                    logger.info("✅ 'See all QA jobs' button checked and click.")
                    qa_careers_page.click_see_all_qa_jobs()

                    logger.info("✅ The Department is expected to be 'Quality Assurance' and the location is being selected.")
                    qa_careers_page.select_location_if_department_is_qa()
                    qa_careers_page.wait_for_job_cards_to_be_replaced()

                    qa_careers_page.wait_for_job_cards_to_load()
                    logger.info("✅ Job postings are being verified.")
                    self.assertTrue(qa_careers_page.verify_job_listings(), "❌Error: Job postings do not meet the criteria!")

                    logger.info("✅ View Role butonu kontrol ediliyor...")
                    self.assertTrue(qa_careers_page.verify_view_role_redirects(), "❌Error: View Role button does not redirect!")

                    logger.info("🎉 All tests completed successfully!")
                    logger.info(f"🌐 Last URL: {driver.current_url}")

                finally:
                    driver.quit()

if __name__ == "__main__":
    unittest.main()
