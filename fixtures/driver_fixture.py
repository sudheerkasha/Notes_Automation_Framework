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
    else config.get("headless", True)
)

window_size = config.get(
    "window_size",
    "1920,1080"
)

implicit_wait = config.get(
    "implicit_wait",
    20
)

page_load_timeout = config.get(
    "page_load_timeout",
    60
)

logger.info(
    f"Creating {browser} driver (headless={is_headless})"
)

if browser == "chrome":

    options = webdriver.ChromeOptions()

    if is_headless:
        options.add_argument("--headless=new")

    options.add_argument(f"--window-size={window_size}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-allow-origins=*")

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-logging"]
    )

    driver = webdriver.Chrome(
        options=options
    )

elif browser == "edge":

    options = webdriver.EdgeOptions()

    if is_headless:
        options.add_argument("--headless=new")

    options.add_argument(
        f"--window-size={window_size}"
    )

    driver = webdriver.Edge(
        service=EdgeService(
            EdgeChromiumDriverManager().install()
        ),
        options=options
    )

else:
    raise ValueError(
        f"Unsupported browser: {browser}"
    )

driver.implicitly_wait(
    implicit_wait
)

driver.set_page_load_timeout(
    page_load_timeout
)

try:
    driver.maximize_window()
except Exception:
    logger.info(
        "Headless mode detected. Skipping maximize_window()."
    )

logger.info(
    f"{browser.capitalize()} driver created successfully"
)

return driver
```
