from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

class PostInstallCommand(install):
    """Run post_installer.py automatically after pip install."""
    def run(self):
        install.run(self)
        subprocess.run([sys.executable, "post_installer.py"])

setup(
    name="snortamv",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click"
    ],
    entry_points={
        "console_scripts": [
            "snortamv = main:main",  # <-- points to your main.py
        ]
    },
    cmdclass={
        'install': PostInstallCommand,
    }
)
