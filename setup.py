from setuptools import setup, find_packages
from setuptools.command.install import install
from os.path import exists
import subprocess
import sys
import platform

OS_TYPE = platform.system().lower()
class PostInstallCommand(install):
    """Run post_installer.py automatically after pip install."""
    def run(self):
        install.run(self)
        # If a requirements.txt exists, try to install it first using pip
        req_file = "requirements.txt"
        linux_req_file = "linux_requirements.txt"
        try:
            if OS_TYPE == "windows":
                if exists(req_file):
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", "-r", req_file],
                        check=True,
                    )
            if OS_TYPE == "linux":
                if exists(linux_req_file):
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", "-r", linux_req_file],
                        check=True,
                    )
        except Exception as e:
            # Do not fail the whole install if requirements installation fails here;
            # print a warning for the user to handle manually.
            print(f"Warning: failed to install requirements from {req_file}: {e}")

        # Run the project's post installer script (existing behavior)
        subprocess.run([sys.executable, "post_installer.py"], check=True)

setup(
    name="snortamv",
    version="1.0.0",
    author="Francis David",
    description="Automated Snort IDS Manager",
    python_requires=">=3.8",
    packages=find_packages(),
    py_modules=["main", "version", "activate", "activenv"],
    include_package_data=True,
    install_requires=[
        "certifi==2025.11.12",
        "charset-normalizer==3.4.4",
        "click",
        "idna==3.11",
        "markdown-it-py==4.0.0",
        "mdurl==0.1.2",
        "MouseInfo==0.1.3",
        "PyAutoGUI==0.9.54",
        "pyfiglet==1.0.4",
        "PyGetWindow==0.0.9",
        "Pygments==2.19.2",
        "PyMsgBox==2.0.1",
        "pyperclip==1.11.0",
        "PyRect==0.2.0",
        "PyScreeze==1.0.1",
        "pytweening==1.2.0",
        "requests==2.32.5",
        "rich==14.2.0",
        "urllib3==2.6.0",
    ],
    entry_points={
        "console_scripts": [
            "snortamv=main:main",
        ]
    },
    cmdclass={
        "install": PostInstallCommand,
    },
)
