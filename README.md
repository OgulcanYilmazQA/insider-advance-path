Automation Testing for Career Page
This repository contains automation tests for verifying the functionality of a career page, focusing on QA job listings, job details, and the filtering options available on the page. The tests are written using Selenium WebDriver, Python, and pytest.

Project Setup
1. Prerequisites
Python 3.x: Ensure that Python 3.x is installed on your machine.

Selenium: A Python library that provides tools to automate browsers.

pytest: A framework for writing simple and scalable test cases.

WebDriver Manager: A tool for automatically managing browser drivers.

2. Installation Steps
To get started with the project, follow these steps:

Clone the repository:

bash
Copy
Edit
git clone <repository-url>
cd <project-directory>
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
The requirements.txt includes the following dependencies:

selenium

pytest

webdriver-manager

Install WebDriver:

WebDriver Manager will automatically install the correct version of the browser drivers (e.g., ChromeDriver, GeckoDriver) based on the browser being used for the tests.

3. Running the Tests
Once you have everything set up, you can run the tests with the following command:

bash
Copy
Edit
pytest -v
This command will run the tests and output detailed information about each test.

4. Configuration
In the tests, the following browsers are supported:

Chrome

Firefox

The browser for testing can be selected using a pytest fixture. The test will run once for each browser, as defined in the fixture:

python
Copy
Edit
@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        # Chrome WebDriver setup
    elif request.param == "firefox":
        # Firefox WebDriver setup
5. Test Structure
The tests are organized into the following page object classes:

base_page.py: Contains reusable methods for interacting with web elements.

home_page.py: Contains methods for interacting with the home page.

career_page.py: Contains methods for interacting with the career page.

qa_page.py: Contains methods specific to the QA career page.

6. Test Scenarios
The following scenarios are tested:

Testing the Career Page: Verifies the accessibility and sections of the career page.

Navigating to the QA Careers Page: Checks if the QA job listings page is accessible.

Job Filtering: Filters the job listings by location and department.

Job Listings Verification: Ensures that all job listings match the expected criteria (QA department, Istanbul location).

View Role Button: Verifies that clicking the "View Role" button redirects to the correct job detail page.

7. Logger Integration
A logging system has been integrated to replace print statements. All actions are now logged for better traceability and debugging.

8. Pull Requests
When you make changes to the repository, create a new branch and submit a pull request for review and merging.

9. Branch Naming Convention
When creating a new feature or fixing a bug, use the following branch naming convention:

feature/description: For new features.

bugfix/description: For fixing bugs.

hotfix/description: For urgent fixes.

Example: feature/add-logger or bugfix/fix-view-role-redirect.

Contributing
If you would like to contribute, please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes and push them to your forked repository.

Submit a pull request to the main branch.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
If you have any questions or suggestions, feel free to open an issue in the repository or contact me directly.
