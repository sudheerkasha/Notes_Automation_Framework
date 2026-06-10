import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.logger import get_logger
from utils.config_reader import get_browser_config

logger = get_logger(__name__)


def create_driver(browser_name: str = None, headless: bool = None):

    config = get_browser_config()

    browser = (browser_name or config.get("name", "chrome")).lower()

    is_headless = (
        headless
        if headless is not None
        else config.get("headless", False)
    )

    window_size = config.get("window_size", "1920,1080")
    implicit_wait = config.get("implicit_wait", 20)
    page_load_timeout = config.get("page_load_timeout", 60)

    # Local or remote execution configuration
    execution_mode = config.get("execution", "local").lower()
    grid_url = config.get("grid_url", "http://localhost:4444")

    logger.info(
        f"Creating {browser} driver "
        f"(headless={is_headless}, execution={execution_mode})"
    )

    if browser == "chrome":

        options = webdriver.ChromeOptions()

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")

        if is_headless:
            options.add_argument("--headless=new")

        options.add_argument(f"--window-size={window_size}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")

        options.add_experimental_option(
            "excludeSwitches",
            ["enable-logging"],
        )

        # Selenium Grid remote execution
        if execution_mode == "remote":

            logger.info(
                f"Connecting Chrome to Selenium Grid: {grid_url}"
            )

            driver = webdriver.Remote(
                command_executor=grid_url,
                options=options,
            )

        # Normal local execution
        elif execution_mode == "local":

            driver_path = ChromeDriverManager().install()

            if not driver_path.lower().endswith("chromedriver.exe"):

                candidate = os.path.join(
                    os.path.dirname(driver_path),
                    "chromedriver.exe",
                )

                if os.path.exists(candidate):
                    driver_path = candidate

            driver = webdriver.Chrome(
                service=ChromeService(driver_path),
                options=options,
            )

        else:
            raise ValueError(
                f"Unsupported execution mode: {execution_mode}. "
                f"Use 'local' or 'remote'."
            )

    elif browser == "edge":

        options = webdriver.EdgeOptions()

        if is_headless:
            options.add_argument("--headless=new")

        options.add_argument(f"--window-size={window_size}")

        # Selenium Grid remote execution
        if execution_mode == "remote":

            logger.info(
                f"Connecting Edge to Selenium Grid: {grid_url}"
            )

            driver = webdriver.Remote(
                command_executor=grid_url,
                options=options,
            )

        # Normal local execution
        elif execution_mode == "local":

            driver = webdriver.Edge(
                service=EdgeService(
                    EdgeChromiumDriverManager().install()
                ),
                options=options,
            )

        else:
            raise ValueError(
                f"Unsupported execution mode: {execution_mode}. "
                f"Use 'local' or 'remote'."
            )

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    driver.maximize_window()

    logger.info(
        f"{browser.capitalize()} driver created successfully "
        f"using {execution_mode} execution"
    )

    return driver
