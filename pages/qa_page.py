import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.base_page import BasePage

class QaPage(BasePage):
    """QA Page: Defines selectors and actions related to QA job listings."""

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
        """
        Verify visibility of key elements on the QA page.

        """
        self.wait_for_element(By.XPATH, self.SEE_ALL_QA_JOBS)
        self.wait_for_element(By.XPATH, self.VIEW_ROLE)

    def is_accessible(self):
        """
        Check if the current page is QA-related based on the URL.

        """
        self.wait_for_page_to_load()
        self.wait_for_element(By.XPATH, self.VIEW_ROLE)
        current_url = self.driver.current_url.lower()
        return "quality-assurance" in current_url or "qa" in current_url

    def filter_jobs(self, location, department):
        """
        Filter job listings by location and department.

        """
        self.wait_for_element_to_be_clickable(By.XPATH, self.LOCATION_DROPDOWN).send_keys(location)
        self.wait_for_element_to_be_clickable(By.XPATH, self.DEPARTMANT_DROPDOWN).send_keys(department)

    def select_location_if_department_is_qa(self):
        """
        If QA department is selected, filter jobs by Istanbul location.

        """
        for _ in range(3):
            self.scroll_to_element(By.ID, self.DEPARTMANT_CONTANIER)
            if self.wait_for_element_text_to_be(By.ID, self.DEPARTMANT_CONTANIER, "Quality Assurance", timeout=10):
                self.wait_for_job_cards_to_be_replaced()
                self.click_element(By.ID, self.LOCATION_CONTAINER)
                self.click_element(By.XPATH, self.LOCATION_ISTANBUL)
                self.wait_for_element(By.XPATH, self.JOB_CARD)
                return
            time.sleep(2)

    def wait_for_job_cards_to_load(self, timeout=15):
        """
        Wait until job cards are visible on the page.

        """
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, self.JOB_LIST))
        )

    def wait_for_job_cards_to_be_replaced(self):
        """
        Wait for job cards to refresh.

        """
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.JOB_CARD)))
        self.wait.until(lambda d: len(d.find_elements(By.XPATH, self.JOB_CARD)) > 0)

    def verify_job_listings(self):
        """
        Check if job listings match QA and Istanbul criteria.

        """
        job_texts = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(".position-list-item")).map(el => el.innerText);
        """)
        valid_jobs = [text for text in job_texts if "quality assurance" in text.lower() and "istanbul" in text.lower()]
        return len(valid_jobs) > 0

    def verify_view_role_redirects(self):
        """
        Check that 'View Role' links redirect to lever.co.

        """
        self.wait_for_element(By.XPATH, self.JOB_CARD, timeout=15)
        view_role_buttons = self.driver.find_elements(By.XPATH, self.VIEW_ROLE)

        if not view_role_buttons:
            return False

        view_role_button = view_role_buttons[0]
        self.scroll_to_web_element(view_role_button)
        time.sleep(1)

        try:
            view_role_button.click()
        except:
            self.driver.execute_script("arguments[0].click();", view_role_button)

        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])

        self.wait_for_page_to_load()
        return "lever.co" in self.driver.current_url

    def click_see_all_qa_jobs(self):
        """
        Click the 'See all QA jobs' button if it's available.

        """
        button = self.wait_for_element_to_be_clickable(By.XPATH, self.SEE_ALL_QA_JOBS)
        self.scroll_to_element(By.XPATH, self.SEE_ALL_QA_JOBS)
        button.click()
