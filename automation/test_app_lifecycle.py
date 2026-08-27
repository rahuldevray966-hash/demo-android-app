import subprocess
import time

PACKAGE_NAME = "com.epam.mobitru"


def run_adb(*args):
    result = subprocess.run(
        ["adb", *args],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"ADB command failed: {' '.join(args)}\n"
            f"{result.stderr}"
        )

    return result.stdout.strip()


def test_app_lifecycle():
    # 1. Check ADB device
    devices = run_adb("devices")

    assert "\tdevice" in devices, "No Android device connected"

    print("✓ ADB device connected")

    # 2. Launch application
    run_adb(
        "shell",
        "monkey",
        "-p",
        PACKAGE_NAME,
        "1"
    )

    print("✓ App launched")

    # 3. Wait
    time.sleep(3)

    # 4. Put application in background
    run_adb(
        "shell",
        "input",
        "keyevent",
        "HOME"
    )

    print("✓ App moved to background")

    time.sleep(2)

    # 5. Bring application to foreground
    run_adb(
        "shell",
        "monkey",
        "-p",
        PACKAGE_NAME,
        "1"
    )

    print("✓ App brought to foreground")

    time.sleep(2)

    # 6. Kill application
    run_adb(
        "shell",
        "am",
        "force-stop",
        PACKAGE_NAME
    )

    print("✓ App killed")

    time.sleep(2)

    # 7. Relaunch application
    run_adb(
        "shell",
        "monkey",
        "-p",
        PACKAGE_NAME,
        "1"
    )

    print("✓ App relaunched")

    time.sleep(3)

    print("✓ App lifecycle test completed successfully")
