# get working directory and store it in a variable
import os
driver_path = os.getcwd() + '/driver/chromedriver'

from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os


# create directory if not exists 'downloaded_pdfs/transport_govt/file1-8217.pdf'

os.makedirs('transport_data/transport_govt', exist_ok=True)


transport_url = 'https://www.transport.govt.nz/about-us/what-we-do/search-official-information-act/SearchForm?Keyword=&TopicID=&DocumentTypeID=28&action_results=Search'

# Path to the ChromeDriver executable
#driver_path =  '/Users/felipenavarro/Documents/Auckland/nzta/dissertation/chromedriver' # Update this with the correct path

# Create a ChromeDriver service
chrome_service = Service(driver_path)

# Initialize the WebDriver with the service
driver = webdriver.Chrome(service=chrome_service)
driver.get(transport_url)

# ok here is the plan
downloaded_files = []
# load the page with the driver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException


# Initialize variables
downloaded_files = set()
file_index = 1
base_url = 'https://www.transport.govt.nz'
download_folder = 'transport_data/transport_govt'

def process_current_page():
    global file_index
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href and '/download/' in href)
    
    for link in pdf_links:
        href = link.get('href')
        if href not in downloaded_files:
            # Print messages at start and every 100 files
            if file_index == 0:
                print("Starting download...")
            elif file_index % 100 == 0:
                print(f"{file_index} files downloaded.")

            print(f'Downloading: {href}')
            try:
                response = requests.get(base_url + href)
                response.raise_for_status()
                file_name = os.path.basename(href)
                file_path = os.path.join(download_folder, f"file{file_index}-{file_name}.pdf")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                file_index += 1
                downloaded_files.add(href)
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {href}: {e}")

# Ensure the download directory exists
os.makedirs(download_folder, exist_ok=True)

# Main loop
while True:
    process_current_page()
    try:
        see_more_button = driver.find_element(By.CLASS_NAME, 'pagination-more')
        see_more_button.click()
        time.sleep(1)  # Wait for the next page to load
    except NoSuchElementException:
        print('Reached the last page.')
        break



# create directory if not exists 'downloaded_pdfs/transport_govt_2 
os.makedirs('transport_data/transport_govt_2', exist_ok=True)

transport_url = 'https://www.transport.govt.nz/about-us/what-we-do/proactive-releases/SearchForm'
# Path to the ChromeDriver executable

# Initialize variables
file_index = 1
downloaded_files = set()
base_url = 'https://www.transport.govt.nz'
download_folder = 'transport_data/transport_govt_2'

# Ensure the download directory exists
os.makedirs(download_folder, exist_ok=True)

def process_current_page():
    global file_index
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href and '/download/' in href)
    
    for link in pdf_links:
        href = link.get('href')
        if href not in downloaded_files:
            # Print messages at start and every 100 files
            if file_index == 1:
                print("Starting download...")
            elif (file_index - 1) % 100 == 0:
                print(f"{file_index - 1} files downloaded.")

            print(f'Downloading: {href}')
            try:
                response = requests.get(base_url + href)
                response.raise_for_status()
                file_name = os.path.basename(href)
                file_path = os.path.join(download_folder, f"file{file_index}-{file_name}.pdf")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                file_index += 1
                downloaded_files.add(href)
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {href}: {e}")

# Main loop
while True:
    process_current_page()
    try:
        see_more_button = driver.find_element(By.CLASS_NAME, 'pagination-more')
        see_more_button.click()
        time.sleep(1)  # Adjust sleep time as needed
    except NoSuchElementException:
        print('Reached the last page.')
        break