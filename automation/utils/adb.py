import os
import subprocess


def run_adb(*args):
    """
    Execute an ADB command.

    ADB_SERIAL can be provided by the pCloudy device setup.
    If it is not provided, ADB uses the default connected device.
    """

    serial = os.getenv("ADB_SERIAL")

    command = ["adb"]

    if serial:
        command.extend(["-s", serial])

    command.extend(args)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"ADB command failed: {' '.join(command)}\n"
            f"{result.stderr}"
        )

    return result.stdout.strip()


def get_devices():
    return run_adb("devices")


def launch_app(package_name):
    return run_adb(
        "shell",
        "monkey",
        "-p",
        package_name,
        "1"
    )


def background_app():
    return run_adb(
        "shell",
        "input",
        "keyevent",
        "HOME"
    )


def stop_app(package_name):
    return run_adb(
        "shell",
        "am",
        "force-stop",
        package_name
    )


def is_device_connected():
    output = get_devices()
    return "\tdevice" in output
