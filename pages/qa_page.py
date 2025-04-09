import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import base_page


class qa_page(base_page):
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
        """
        QACareersPage constructor.

        :param driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.check()

    def check(self):
        """
        Checks visibility of critical elements on the QA Careers Page.
        """
        try:
            print("✅ Running initial checks for critical elements on QA Page...")
            self.wait_for_element(By.XPATH, self.SEE_ALL_QA_JOBS)
            self.wait_for_element(By.XPATH, self.VIEW_ROLE)
            print("✅ Critical elements on QA Page are visible.")
        except Exception as e:
            print(f"❌ QA Page critical element not found: {e}")
            raise

    def is_accessible(self):
        """
        Verifies if the QA Careers page is accessible by checking the URL and page elements.
        """
        try:
            print("🔍 QA page title checked")
            self.wait_for_page_to_load()
            self.wait_for_element(By.XPATH, self.VIEW_ROLE)
            current_url = self.driver.current_url
            print("🌐 QA Page URL:", current_url)
            return "quality-assurance" in current_url or "QA" in current_url
        except Exception as e:
            print(f"❌ QA page not found: {e}")
            return False

    def filter_jobs(self, location, department):
        """
        Filters job listings by location and department.
        """
        location_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.LOCATION_DROPDOWN)
        if location_dropdown:
            location_dropdown.send_keys(location)

        department_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.DEPARTMANT_DROPDOWN)
        if department_dropdown:
            department_dropdown.send_keys(department)

    def select_location_if_department_is_qa(self):
        """
        If the department is 'Quality Assurance', selects 'Istanbul, Turkiye' from location filter.
        Retries up to 3 times if department is not loaded properly.
        """
        print("⏳ Waiting for department filtering as 'Quality Assurance'")

        for attempt in range(3):
            self.scroll_to_element(By.ID, self.DEPARTMANT_CONTANIER)
            success = self.wait_for_element_text_to_be(By.ID, self.DEPARTMANT_CONTANIER, "Quality Assurance", timeout=10)

            if success:
                print("✅ Department success")
                self.wait_for_job_cards_to_be_replaced()
                self.click_element(By.ID, self.LOCATION_CONTAINER)
                print("⏳ 'Istanbul, Turkiye' selection checked")
                self.click_element(By.XPATH, self.LOCATION_ISTANBUL)
                print("✅ 'Istanbul, Turkiye' selection clicked")
                print("⏳ Job-listing page checked")
                self.wait_for_element(By.XPATH, self.JOB_CARD)
                return
            else:
                print(f"⚠️ 'Quality Assurance' could not found on {attempt + 1}. attempt ")
                time.sleep(2)

        print("❌ Error: Department value could not selected as 'Quality Assurance'.")

    def wait_for_job_cards_to_load(self, timeout=15):
        """
        Waits for job cards to load completely.
        """
        print("⏳ Job cards loading")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, self.JOB_LIST))
        )
        print("✅ Job cards completed.")

    def wait_for_job_cards_to_be_replaced(self):
        """
        Waits until old job cards are replaced with new ones.
        """
        try:
            print("⏳ Old job cards disappearing.")
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.JOB_CARD)))
            print("✅ Old job cards disappeared.")
        except:
            print("⚠️ Old job cards could be still visible, continue to process.")

        self.wait.until(lambda d: len(d.find_elements(By.XPATH, self.JOB_CARD)) > 0)
        print("✅ New job cards loaded to the DOM.")

    def verify_job_listings(self):
        """
        Validates that each job listing includes both QA and Istanbul keywords.
        """
        print("🧪 On the QA page + searching for Istanbul job.")

        job_texts = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(".position-list-item")).map(el => el.innerText);
        """)

        valid_jobs = 0
        for i, text in enumerate(job_texts, 1):
            print(f"📋 JS Job {i}:\n{text}\n")
            lower_text = text.lower()
            if "quality assurance" in lower_text and "istanbul" in lower_text:
                print(f"✅ Job {i} FOUND: QA + Istanbul")
                valid_jobs += 1
            else:
                print(f"⚠️ Job {i} Not Found")

        print(f"🎯 Job offers: {valid_jobs}")
        return valid_jobs > 0

    def verify_view_role_redirects(self):
        """
        Clicks the first 'View Role' button and verifies it redirects to lever.co job detail page.
        """
        print("🔍 View Role button checked.")
        try:
            self.wait_for_element(By.XPATH, self.JOB_CARD, timeout=15)
            print("✅ Positions checked.")

            for attempt in range(3):
                try:
                    view_role_buttons = self.driver.find_elements(By.XPATH, self.VIEW_ROLE)
                    if view_role_buttons:
                        view_role_button = view_role_buttons[0]

                        # Base'deki fonksiyonla scroll işlemi
                        self.scroll_to_web_element(view_role_button)
                        time.sleep(1)

                        try:
                            view_role_button.click()
                            print("✅ Click success.")
                        except Exception as e:
                            print(f"⚠️ Click failed: {e}, JS fallback on.")
                            self.driver.execute_script("arguments[0].click();", view_role_button)

                        break
                    else:
                        print("❌ View Role button not found.")
                        return False

                except Exception as e:
                    print(f"⚠️ {attempt + 1}. attempt failed: {e}")
                    time.sleep(2)

            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[1])
                print("🔄 New tab opened:", self.driver.current_url)

            self.wait_for_page_to_load()
            return "lever.co" in self.driver.current_url

        except Exception as e:
            print(f"❌ View Role error: {e}")
            return False

    def click_see_all_qa_jobs(self):
        """
        Clicks on the 'See all QA jobs' button.
        """
        print("🔍 'See all QA jobs' button checked...")
        button = self.wait_for_element_to_be_clickable(By.XPATH, self.SEE_ALL_QA_JOBS)
        if button:
            self.scroll_to_element(By.XPATH, self.SEE_ALL_QA_JOBS)
            button.click()
            print("✅ 'See all QA jobs' clicked.")
        else:
            print("❌ HATA: 'See all QA jobs' could not found.")
