import csv
import os
import time
import customer_class

from robocorp import browser
from robocorp.tasks import task

# Load the environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path="secrets.env")

# Environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PAGE = os.getenv("PAGE")
LOGIN_PAGE = os.getenv("LOGIN_PAGE")
FILE_PATH = os.getenv("FILE_PATH") # Path to the file that is being used or stored with certain name

# Constants
BROWSER = browser.page()

@task
def solve_level_1():
    browser.configure(browser_engine="chromium",
                      headless=True,
                      screenshot="only-on-failure",)
    login_to_website()
    open_website()
    download_csv_and_start()
    customer_data = read_csv()
    start_button()
    fill_form(customer_data)
    time.sleep(5)

def open_website():
    """ Open the website. """
    BROWSER.goto(PAGE)

def login_to_website():
    """ Login to the website. """
    BROWSER.goto(LOGIN_PAGE)
    BROWSER.fill("input[name='email']", EMAIL)
    BROWSER.fill("input[name='password']", PASSWORD)
    BROWSER.get_by_role("button", name="Login").click()


def download_csv_and_start():
    """ Download the CSV file and start the process. """
    BROWSER.fill("input[name='tool_used']", "robocorp, python")

    # Start waiting for the download
    with BROWSER.expect_download() as download_info:
        # Perform the action that initiates download
        BROWSER.get_by_role("button", name="download").click()
    download = download_info.value
    # Wait for the download process to complete and save the downloaded file somewhere
    download.save_as(FILE_PATH)
    
def start_button():
    # Starts the challenge
    BROWSER.get_by_role("button", name="start").click()

def read_csv():
    """ Read the CSV file and return the data with mapped field names. """
    field_mapping = {
        'Product Name': 'Nome Prodotto',
        'Quantity': 'Quantita',
        'Price': 'Prezzo',
        'Customer Name': 'Nome Cliente',
        'Customer Address': 'Indirizzo Cliente',
        'Customer Email': 'Email Cliente',
        'Delivery Date': 'Data Consenga'
    }
    
    with open(FILE_PATH, "r", encoding="UTF-8") as file:
        reader = csv.DictReader(file)
        customer_data = []
        for row in reader:
            mapped_row = {field_mapping[key]: value for key, value in row.items()}
            customer_data.append(mapped_row)
    
    print(customer_data)
    return customer_data

def fill_form(customer_data):
    """ Fill the form with the data from the CSV file. """
    for data in customer_data:
        BROWSER.locator("xpath=//input[@id='Indirizzo_Cliente']").fill(data['Indirizzo Cliente'])
        BROWSER.locator("xpath=//input[@id='Nome_Cliente']").fill(data['Nome Cliente'])
        BROWSER.locator("xpath=//input[@id='email_cliente']").fill(data['Email Cliente'])
        BROWSER.locator("xpath=//input[@id='Nome_prodotto']").fill(data['Nome Prodotto'])
        BROWSER.locator("xpath=//input[@id='Quantita']").fill(data['Quantita'])
        BROWSER.locator("xpath=//input[@id='prezzo']").fill(data['Prezzo'])
        BROWSER.locator("xpath=//input[@id='Data_consenga']").fill(data['Data Consenga'])

        BROWSER.locator(".submit-btn").click() 