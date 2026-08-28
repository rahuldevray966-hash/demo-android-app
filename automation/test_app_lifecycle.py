import os
import time
import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options


APP_PACKAGE = os.getenv("APP_PACKAGE", "com.epam.mobitru")
DEVICE_NAME = os.getenv("PCLOUDY_DEVICE", "")

PCLOUDY_EMAIL = os.environ["PCLOUDY_EMAIL"]
PCLOUDY_ACCESS_KEY = os.environ["PCLOUDY_ACCESS_KEY"]

PCLOUDY_APPIUM_URL = "https://device.pcloudy.com/appiumcloud/wd/hub"


def create_driver():
    options = UiAutomator2Options()

    # -----------------------------
    # pCloudy credentials
    # -----------------------------
    options.set_capability(
        "pCloudy_Username",
        PCLOUDY_EMAIL
    )

    options.set_capability(
        "pCloudy_ApiKey",
        PCLOUDY_ACCESS_KEY
    )

    # -----------------------------
    # APK already uploaded to pCloudy
    # -----------------------------
    options.set_capability(
        "pCloudy_ApplicationName",
        "firebase-app.apk"
    )

    # -----------------------------
    # Device
    # -----------------------------
    options.set_capability(
        "pCloudy_DeviceFullName",
        DEVICE_NAME
    )

    options.set_capability(
        "pCloudy_DurationInMinutes",
        15
    )

    # Android
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
        120
    )

    print(f"Starting Appium session on: {DEVICE_NAME}")

    return webdriver.Remote(
        command_executor=PCLOUDY_APPIUM_URL,
        options=options
    )


@pytest.mark.lifecycle
def test_app_lifecycle():

    driver = None

    try:
        driver = create_driver()

        print("Appium session created successfully")

        # ---------------------------------
        # 1. Application Launch
        # ---------------------------------

        print("Step 1: Application launched")

        time.sleep(10)

        # Verify package
        current_package = driver.current_package

        print(
            f"Current package: {current_package}"
        )

        assert current_package == APP_PACKAGE, (
            f"Expected {APP_PACKAGE}, "
            f"but found {current_package}"
        )

        print("Application launch verified")

        # ---------------------------------
        # 2. Wait
        # ---------------------------------

        print("Step 2: Waiting for application")

        time.sleep(5)

        # ---------------------------------
        # 3. Background
        # ---------------------------------

        print("Step 3: Sending application to background")

        driver.background_app(5)

        print("Application backgrounded successfully")

        # ---------------------------------
        # 4. Foreground
        # ---------------------------------

        print("Step 4: Bringing application to foreground")

        driver.activate_app(APP_PACKAGE)

        time.sleep(5)

        print("Application foregrounded successfully")

        # ---------------------------------
        # 5. Kill
        # ---------------------------------

        print("Step 5: Terminating application")

        driver.terminate_app(APP_PACKAGE)

        time.sleep(3)

        print("Application terminated successfully")

        # ---------------------------------
        # 6. Relaunch
        # ---------------------------------

        print("Step 6: Relaunching application")

        driver.activate_app(APP_PACKAGE)

        time.sleep(8)

        current_package = driver.current_package

        print(
            f"Package after relaunch: {current_package}"
        )

        assert current_package == APP_PACKAGE, (
            "Application did not relaunch correctly"
        )

        print("Application relaunch verified")

        print("--------------------------------")
        print("APP LIFECYCLE TEST PASSED")
        print("--------------------------------")

    finally:

        if driver:
            print("Ending Appium session")
            driver.quit()
