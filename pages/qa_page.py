import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

# Logger tanımı
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QaPage(BasePage):
    """
    Initialize QA page with driver and default timeout.

    :param driver: Selenium WebDriver instance
    :param int timeout: Maximum wait time for element actions
    """
    # Locators
    DEPARTMANT_CONTANIER = "select2-filter-by-department-container"
    DEPARTMANT_DROPDOWN = "//select[@id='department']"
    VIEW_ROLE = "//a[contains(text(), 'View Role')]"
    SEE_ALL_QA_JOBS = "//a[contains(text(), 'See all QA jobs')]"
    JOB_CARD = "//div[contains(@class, 'position-list-item')]"
    JOB_LIST = "//div[@id='jobs-list']//div[contains(@class, 'position-list-item')]"
    LOCATION_CONTAINER = "select2-filter-by-location-container"
    LOCATION_ISTANBUL = "//li[contains(@class, 'select2-results__option') and normalize-space(text())='Istanbul, Turkiye']"
    LOCATION_DROPDOWN = "//select[@id='location']"

    def __init__(self, driver):
        super().__init__(driver)
        self.check()

    def check(self):
        try:
            logger.info("Checking visibility of critical QA page elements...")
            self.wait_for_element(By.XPATH, self.SEE_ALL_QA_JOBS)
            self.wait_for_element(By.XPATH, self.VIEW_ROLE)
            logger.info("Critical QA page elements are visible.")
        except Exception as e:
            logger.error(f"QA Page critical elements not found: {e}")
            raise

    def is_accessible(self):
        try:
            self.wait_for_page_to_load()
            self.wait_for_element(By.XPATH, self.VIEW_ROLE)
            current_url = self.driver.current_url
            accessible = "quality-assurance" in current_url or "QA" in current_url
            logger.info(f"QA page accessibility: {'Accessible' if accessible else 'Not Accessible'}")
            return accessible
        except Exception as e:
            logger.error(f"Error while checking QA page accessibility: {e}")
            return False

    def filter_jobs(self, location, department):
        logger.info(f"Filtering jobs by Location: {location}, Department: {department}")
        location_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.LOCATION_DROPDOWN)
        if location_dropdown:
            location_dropdown.send_keys(location)
        else:
            logger.warning("Location dropdown not found.")

        department_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.DEPARTMANT_DROPDOWN)
        if department_dropdown:
            department_dropdown.send_keys(department)
        else:
            logger.warning("Department dropdown not found.")

    def select_location_if_department_is_qa(self):
        for attempt in range(3):
            logger.info(f"Attempt {attempt + 1}: Scrolling to department container and checking for 'Quality Assurance'")
            self.scroll_to_element(By.ID, self.DEPARTMANT_CONTANIER)
            success = self.wait_for_element_text_to_be(By.ID, self.DEPARTMANT_CONTANIER, "Quality Assurance", timeout=10)

            if success:
                logger.info("Quality Assurance department detected. Selecting Istanbul location.")
                self.wait_for_job_cards_to_be_replaced()
                self.click_element(By.ID, self.LOCATION_CONTAINER)
                self.click_element(By.XPATH, self.LOCATION_ISTANBUL)
                self.wait_for_element(By.XPATH, self.JOB_CARD)
                return
            else:
                logger.warning("Quality Assurance department not loaded yet. Retrying...")
                time.sleep(2)

        logger.error("Failed to detect 'Quality Assurance' department after 3 attempts.")

    def wait_for_job_cards_to_load(self, timeout=15):
        logger.info("Waiting for job cards to load...")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, self.JOB_LIST))
        )
        logger.info("Job cards loaded.")

    def wait_for_job_cards_to_be_replaced(self):
        logger.info("Waiting for job cards to be replaced...")
        try:
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.JOB_CARD)))
        except:
            self.wait.until(lambda d: len(d.find_elements(By.XPATH, self.JOB_CARD)) > 0)
        logger.info("Job cards replaced.")

    def verify_job_listings(self):
        logger.info("Verifying job listings for 'Quality Assurance' and 'Istanbul'...")
        job_texts = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(".position-list-item")).map(el => el.innerText);
        """)

        valid_jobs = 0
        for i, text in enumerate(job_texts, 1):
            lower_text = text.lower()
            if "quality assurance" in lower_text and "istanbul" in lower_text:
                valid_jobs += 1
            else:
                logger.warning(f"Job {i} does not match criteria.")

        logger.info(f"Total valid QA job listings: {valid_jobs}")
        return valid_jobs > 0

    def verify_view_role_redirects(self):
        logger.info("Verifying 'View Role' redirection to lever.co...")
        try:
            self.wait_for_element(By.XPATH, self.JOB_CARD, timeout=15)

            for attempt in range(3):
                try:
                    view_role_buttons = self.driver.find_elements(By.XPATH, self.VIEW_ROLE)
                    if view_role_buttons:
                        view_role_button = view_role_buttons[0]
                        self.scroll_to_web_element(view_role_button)
                        time.sleep(1)

                        try:
                            view_role_button.click()
                        except Exception as e:
                            logger.warning(f"Click failed with error: {e}. Retrying with JS click.")
                            self.driver.execute_script("arguments[0].click();", view_role_button)

                        break
                    else:
                        logger.warning("No 'View Role' buttons found.")
                        return False

                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(2)

            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[1])

            self.wait_for_page_to_load()
            redirected = "lever.co" in self.driver.current_url
            logger.info(f"Redirection {'successful' if redirected else 'failed'}: {self.driver.current_url}")
            return redirected

        except Exception as e:
            logger.error(f"Error verifying 'View Role' redirection: {e}")
            return False

    def click_see_all_qa_jobs(self):
        logger.info("Clicking 'See all QA jobs' button...")
        button = self.wait_for_element_to_be_clickable(By.XPATH, self.SEE_ALL_QA_JOBS)
        if button:
            self.scroll_to_element(By.XPATH, self.SEE_ALL_QA_JOBS)
            button.click()
            logger.info("'See all QA jobs' clicked.")
        else:
            logger.error("'See all QA jobs' button could not be found.")
