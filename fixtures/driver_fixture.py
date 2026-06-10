import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.logger import get_logger
from utils.config_reader import get_browser_config

logger = get_logger(**name**)

def create_driver(browser_name: str = None, headless: bool = None):

```
config = get_browser_config()

browser = (
    browser_name
    or config.get("name", "chrome")
).lower()

is_headless = (
    headless
    if headless is not None
    else config.get("headless", False)
)

window_size = config.get("window_size", "1920,1080")
implicit_wait = config.get("implicit_wait", 20)
page_load_timeout = config.get("page_load_timeout", 60)

execution_mode = config.get(
    "execution",
    "local"
).lower()

grid_url = config.get(
    "grid_url",
    "http://localhost:4444"
)

logger.info(
    f"Creating {browser} driver "
    f"(headless={is_headless}, execution={execution_mode})"
)

# ====================================================
# CHROME
# ====================================================

if browser == "chrome":

    options = webdriver.ChromeOptions()

    if is_headless:
        options.add_argument("--headless=new")

    options.add_argument(f"--window-size={window_size}")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")

    options.add_argument(
        "--remote-allow-origins=*"
    )

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-logging"]
    )

    if execution_mode == "remote":

        logger.info(
            f"Connecting Chrome to Selenium Grid: {grid_url}"
        )

        driver = webdriver.Remote(
            command_executor=grid_url,
            options=options
        )

    elif execution_mode == "local":

        logger.info(
            "Starting Chrome using Selenium Manager"
        )

        driver = webdriver.Chrome(
            options=options
        )

    else:
        raise ValueError(
            f"Unsupported execution mode: {execution_mode}. "
            f"Use 'local' or 'remote'."
        )

# ====================================================
# EDGE
# ====================================================

elif browser == "edge":

    options = webdriver.EdgeOptions()

    if is_headless:
        options.add_argument("--headless=new")

    options.add_argument(
        f"--window-size={window_size}"
    )

    if execution_mode == "remote":

        logger.info(
            f"Connecting Edge to Selenium Grid: {grid_url}"
        )

        driver = webdriver.Remote(
            command_executor=grid_url,
            options=options
        )

    elif execution_mode == "local":

        driver = webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()
            ),
            options=options
        )

    else:
        raise ValueError(
            f"Unsupported execution mode: {execution_mode}. "
            f"Use 'local' or 'remote'."
        )

else:
    raise ValueError(
        f"Unsupported browser: {browser}"
    )

driver.implicitly_wait(implicit_wait)
driver.set_page_load_timeout(page_load_timeout)

if not is_headless:
    try:
        driver.maximize_window()
    except Exception:
        pass

logger.info(
    f"{browser.capitalize()} driver created successfully "
    f"using {execution_mode} execution"
)

return driver
```
