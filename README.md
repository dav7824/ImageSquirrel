# ImageSquirrel
Practice Selenium scraper for fictitious media hosting site.

### Running environment:
- ChromeDriver ([Download](https://chromedriver.chromium.org/downloads))
- Python modules:
    - requests 2.28.0
    - Selenium 4.8.3
    - PIL image library

To set up driver, you can either:
1. Add driver path to system paths
    ```python
    from selenium import webdriver
    import os

    os.environ['PATH'] += path_to_driver
    driver = webdriver.Chrome()
    ```
1. Pass drvier path by `Options` class when creating webdriver object
    ```python
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.chrome_executable_path = path_to_driver
    driver = webdriver.Chrome(options=options)
    ```
