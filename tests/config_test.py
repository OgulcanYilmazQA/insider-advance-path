import pytest
import os
from datetime import datetime
from DBController import insert_test_result_to_influxdb


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook to handle test result reporting:
    - Inserts test result to InfluxDB
    - Captures screenshot on test failure

    :param item: pytest test item

    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "CALL":
        test_name = item.name
        status = "PASSED" if report.passed else "FAIL"
        duration = getattr(report, 'duration', 0)
        timestamp = datetime.utcnow()

        try:
            insert_test_result_to_influxdb(
                test_name=test_name,
                status=status,
                duration=duration,
                timestamp=timestamp
            )
        except Exception as e:
            print(f"❌ Writing to the InfluxDB failed: {e}")

        if report.failed:
            driver = item.funcargs.get("driver", None)
            if driver:
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
                driver.save_screenshot(screenshot_path)
                print(f"🖼 Screenshot done: {screenshot_path}")
