import os
import time
import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options


# ============================================================
# Configuration
# ============================================================

APP_PACKAGE = os.getenv(
    "APP_PACKAGE",
    "com.epam.mobitru"
)

DEVICE_NAME = os.getenv(
    "PCLOUDY_DEVICE",
    ""
)

PCLOUDY_EMAIL = os.environ["PCLOUDY_EMAIL"]
PCLOUDY_ACCESS_KEY = os.environ["PCLOUDY_ACCESS_KEY"]

PCLOUDY_APPIUM_URL = (
    "https://device.pcloudy.com/appiumcloud/wd/hub"
)

# ============================================================
# Performance Data
#
# true  -> Performance data enabled
# false -> Performance data disabled
#
# Default is true
# ============================================================

PERFORMANCE_DATA = os.getenv(
    "PCLOUDY_ENABLE_PERFORMANCE_DATA",
    "true"
).lower() == "true"


# ============================================================
# Create pCloudy Appium Driver
# ============================================================

def create_driver():

    if not DEVICE_NAME:
        raise RuntimeError(
            "PCLOUDY_DEVICE is empty"
        )

    options = UiAutomator2Options()

    # ========================================================
    # pCloudy Configuration
    # ========================================================

    options.set_capability(
        "pCloudy_Username",
        PCLOUDY_EMAIL
    )

    options.set_capability(
        "pCloudy_ApiKey",
        PCLOUDY_ACCESS_KEY
    )

    options.set_capability(
        "pCloudy_ApplicationName",
        "firebase-app.apk"
    )

    options.set_capability(
        "pCloudy_DeviceFullName",
        DEVICE_NAME
    )

    options.set_capability(
        "pCloudy_DurationInMinutes",
        15
    )

    # ========================================================
    # pCloudy Performance Data
    # ========================================================

    options.set_capability(
        "pCloudy_EnablePerformanceData",
        PERFORMANCE_DATA
    )

    # ========================================================
    # Android Configuration
    # ========================================================

    options.set_capability(
        "platformName",
        "Android"
    )

    options.set_capability(
        "appium:automationName",
        "UiAutomator2"
    )

    options.set_capability(
        "appium:appPackage",
        APP_PACKAGE
    )

    options.set_capability(
        "appium:noReset",
        False
    )

    options.set_capability(
        "appium:autoGrantPermissions",
        True
    )

    options.set_capability(
        "appium:newCommandTimeout",
        300
    )

    # ========================================================
    # Print Configuration
    # ========================================================

    print("")
    print("==========================================")
    print("Starting pCloudy Appium session")
    print("==========================================")
    print(f"Device           : {DEVICE_NAME}")
    print(f"Package          : {APP_PACKAGE}")
    print(
        f"Performance Data : {PERFORMANCE_DATA}"
    )
    print(
        "=========================================="
    )

    # ========================================================
    # Retry Appium Session
    # ========================================================

    last_error = None

    for attempt in range(1, 4):

        try:

            print(
                f"Creating pCloudy Appium session "
                f"(attempt {attempt}/3)..."
            )

            driver = webdriver.Remote(
                command_executor=PCLOUDY_APPIUM_URL,
                options=options
            )

            print(
                "Appium session created successfully"
            )

            return driver

        except Exception as exc:

            last_error = exc

            print(
                f"Appium session attempt "
                f"{attempt} failed:"
            )

            print(str(exc))

            if attempt < 3:

                print(
                    "Waiting 15 seconds "
                    "before retry..."
                )

                time.sleep(15)

    raise RuntimeError(
        "Could not create pCloudy Appium "
        "session after 3 attempts "
        f"for device: {DEVICE_NAME}"
    ) from last_error


# ============================================================
# App Lifecycle Test
# ============================================================

@pytest.mark.lifecycle
def test_app_lifecycle():

    driver = None

    try:

        # ====================================================
        # Create Appium Session
        # ====================================================

        driver = create_driver()

        print("")
        print("==========================================")
        print("Appium session created successfully")
        print("==========================================")
        print(f"Device           : {DEVICE_NAME}")
        print(f"Package          : {APP_PACKAGE}")
        print(
            f"Performance Data : {PERFORMANCE_DATA}"
        )
        print(
            "=========================================="
        )

        # ====================================================
        # 1. Launch Application
        # ====================================================

        print("")
        print(
            "Step 1: Launching application"
        )

        time.sleep(10)

        current_package = driver.current_package

        print(
            f"Current package: {current_package}"
        )

        assert current_package == APP_PACKAGE, (
            f"Expected {APP_PACKAGE}, "
            f"but found {current_package}"
        )

        print(
            "Application launch verified"
        )

        # ====================================================
        # 2. Wait for Application
        # ====================================================

        print("")
        print(
            "Step 2: Waiting for application"
        )

        time.sleep(5)

        print(
            "Application wait completed"
        )

        # ====================================================
        # 3. Background Application
        # ====================================================

        print("")
        print(
            "Step 3: Sending application "
            "to background"
        )

        driver.background_app(5)

        print(
            "Application backgrounded successfully"
        )

        # ====================================================
        # 4. Bring Application to Foreground
        # ====================================================

        print("")
        print(
            "Step 4: Bringing application "
            "to foreground"
        )

        driver.activate_app(APP_PACKAGE)

        time.sleep(5)

        print(
            "Application foregrounded successfully"
        )

        # ====================================================
        # 5. Terminate Application
        # ====================================================

        print("")
        print(
            "Step 5: Terminating application"
        )

        driver.terminate_app(APP_PACKAGE)

        time.sleep(3)

        print(
            "Application terminated successfully"
        )

        # ====================================================
        # 6. Relaunch Application
        # ====================================================

        print("")
        print(
            "Step 6: Relaunching application"
        )

        driver.activate_app(APP_PACKAGE)

        time.sleep(8)

        current_package = driver.current_package

        print(
            f"Package after relaunch: "
            f"{current_package}"
        )

        assert current_package == APP_PACKAGE, (
            "Application did not relaunch correctly"
        )

        print(
            "Application relaunch verified"
        )

        # ====================================================
        # Test Passed
        # ====================================================

        print("")
        print("------------------------------------------")
        print("APP LIFECYCLE TEST PASSED")
        print("------------------------------------------")

    finally:

        # ====================================================
        # Close Appium Session
        # ====================================================

        if driver is not None:

            print("")
            print(
                "Ending Appium session"
            )

            try:

                driver.quit()

                print(
                    "Appium session closed successfully"
                )

            except Exception as exc:

                print(
                    "Warning while closing "
                    f"Appium session: {exc}"
                )
