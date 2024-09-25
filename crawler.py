import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re
import pickle
from tqdm import tqdm




def nzta_oia_crawler_preparation(soup):
 
    # Parse the HTML content
    # Define the regular expression pattern to match the desired link format
    # The pattern will now match any URL that starts with 'oia-####-response' and ends with '.pdf'
    pattern = re.compile(r'oia-\d+-response.*\.pdf', re.IGNORECASE)

    # List to store the results with links and their preceding <p>, <h3>, <i>, and <h4> (year) elements
    results_2024_2023 = []

    # Find all links that match the pattern and capture their preceding <p>, <h3>, <i> (month), and <h4> (year)
    for link in soup.find_all('a', href=True):
        if pattern.search(link['href']):
            # Initialize variables to store the preceding <p>, <h3>, month, and year elements
            preceding_p = None
            preceding_h3 = None
            month = None
            year = None
            
            # Traverse backward in the document from the link's position
            prev_element = link.find_previous(['p', 'h3', 'i', 'h4'])
            while prev_element:
                if prev_element.name == 'p' and not preceding_p:
                    preceding_p = prev_element.get_text(strip=True)
                elif prev_element.name == 'h3' and not preceding_h3:
                    preceding_h3 = prev_element.get_text(strip=True)
                elif prev_element.name == 'i' and 'i-caret-down' in prev_element.get('class', []) and not month:
                    # Find the associated month from the parent <a> tag
                    month = prev_element.find_parent('a').get_text(strip=True)
                elif prev_element.name == 'h4' and not year:
                    # Find the year from the <h4> tag
                    year = prev_element.get_text(strip=True)
                # Break the loop if all elements are found
                if preceding_p and preceding_h3 and month and year:
                    break
                prev_element = prev_element.find_previous(['p', 'h3', 'i', 'h4'])
            
            # Store the result with the link and its associated <p>, <h3>, month, and year
            results_2024_2023.append({
                'url': link['href'],
                'response_letter': link.get_text(strip=True),
                'preceding_p': preceding_p,
                'preceding_h3': preceding_h3,
                'month': month,
                'year': year
            })

    return results_2024_2023


# Function to find related attachments based on the response file name
def find_related_attachments_2024_2023(response_filename):
    # Extract the ID number from the response filename (assuming the pattern is oia-####-response*.pdf)
    request_id_match = re.search(r'oia-(\d+)-response.*\.pdf', response_filename, re.IGNORECASE)

    if not request_id_match:
        print(f"No valid ID found in the filename: {response_filename}")
        return []  # No valid ID found, return an empty list

    request_id = request_id_match.group(1)

    # Create a pattern to identify attachment URLs with the same ID
    # The pattern allows for any characters between "attachment" and any file extension
    attachment_pattern = re.compile(r'oia-' + request_id + r'(-\d+)?-attachment.*\..+', re.IGNORECASE)




    # List to store found attachments
    attachments = []

    # Find all <a> tags that match the attachment pattern
    for link in soup.find_all('a', href=True):
        if attachment_pattern.search(link['href']):
            attachment_info = link['href']  # Store only the URL
            attachments.append(attachment_info)

    return attachments





def nzta_oia_non_media_crawler_preparation(soup):
    response_pattern = re.compile(r'^(?!.*attachment).*\.pdf', re.IGNORECASE)

    # List to store the results with links and their preceding <p>, <h3>, <i>, and <h4> (year) elements
    results_non_media = []

    # Find all links that match the pattern and exclude 'attachment'
    for link in soup.find_all('a', href=True):
        if response_pattern.search(link['href']):
            # Initialize variables to store the preceding <p>, <h3>, month, and year elements
            preceding_p = None
            preceding_h3 = None
            year = None
            
            # Traverse backward in the document from the link's position
            prev_element = link.find_previous(['p', 'h2', 'i'])
            while prev_element:
                if prev_element.name == 'p' and not preceding_p:
                    preceding_p = prev_element.get_text(strip=True)
                elif prev_element.name == 'h2' and not preceding_h3:
                    preceding_h3 = prev_element.get_text(strip=True)
                elif prev_element.name == 'i' and 'i-caret-down' in prev_element.get('class', []) and not year:
                    # Find the associated year from the parent <a> tag
                    year = prev_element.find_parent('a').get_text(strip=True)
            
                # Break the loop if all elements are found
                if preceding_p and preceding_h3 and year:
                    break
                prev_element = prev_element.find_previous(['p', 'h2', 'i'])
            
            # Store the result with the link and its associated <p>, <h3>, month, and year
            results_non_media.append({
                'url': link['href'],
                'response_letter': link.get_text(strip=True),
                'preceding_p': preceding_p,
                'preceding_h3': preceding_h3,
                'year': year
            })
    return results_non_media

def find_related_attachments_non_media(response_filename):
    # Extract the ID number from the response filename (assuming the pattern is oia-####-response*.pdf)
    request_id_match = re.search(r'oia-(\d+)-.*\.pdf', response_filename, re.IGNORECASE)

    
    if not request_id_match:
        return []  # No valid ID found, return an empty list

    request_id = request_id_match.group(1)

    # Create a pattern to identify attachment URLs with the same ID
    # The pattern allows for any characters between "attachment" and any file extension
    attachment_pattern = re.compile(r'oia-' + request_id + r'(-\d+)?-attachment.*\..+', re.IGNORECASE)


    # List to store found attachments
    attachments = []

    # Find all <a> tags that match the attachment pattern
    for link in soup.find_all('a', href=True):
        if attachment_pattern.search(link['href']):
            attachment_info = link['href']  # Store only the URL
            attachments.append(attachment_info)

    return attachments


def nzta_oia_media_crawler_preparation(soup):
    # Modify the initial pattern to exclude 'attachment' URLs
    response_pattern = re.compile(r'^(?!.*attachment).*\.pdf', re.IGNORECASE)

    # List to store the results with links and their preceding <p>, <h3>, <i>, and <h4> (year) elements
    results_media = []

    # Find all links that match the pattern and exclude 'attachment'
    for link in soup.find_all('a', href=True):
        if response_pattern.search(link['href']):
            # Initialize variables to store the preceding <p>, <h3>, month, and year elements
            preceding_p = None
            preceding_h3 = None
            year = None
            
            # Traverse backward in the document from the link's position
            prev_element = link.find_previous(['p', 'h2', 'i'])
            while prev_element:
                if prev_element.name == 'p' and not preceding_p:
                    preceding_p = prev_element.get_text(strip=True)
                elif prev_element.name == 'h2' and not preceding_h3:
                    preceding_h3 = prev_element.get_text(strip=True)
                elif prev_element.name == 'i' and 'i-caret-down' in prev_element.get('class', []) and not year:
                    # Find the associated year from the parent <a> tag
                    year = prev_element.find_parent('a').get_text(strip=True)
            
                # Break the loop if all elements are found
                if preceding_p and preceding_h3 and year:
                    break
                prev_element = prev_element.find_previous(['p', 'h2', 'i'])
            
            # Store the result with the link and its associated <p>, <h3>, month, and year
            results_media.append({
                'url': link['href'],
                'response_letter': link.get_text(strip=True),
                'preceding_p': preceding_p,
                'preceding_h3': preceding_h3,
                'year': year
            })
    return results_media


# Function to find related attachments based on the response file name
def find_related_attachments_media(response_filename):
    # Extract the ID number from the response filename (assuming the pattern is oia-####-response*.pdf)
    request_id_match = re.search(r'oia-(\d+)-.*\.pdf', response_filename)
    
    if not request_id_match:
        return []  # No valid ID found, return an empty list

    request_id = request_id_match.group(1)

    # Create a pattern to identify attachment URLs with the same ID
    # The pattern allows for any characters between "attachment" and any file extension
    attachment_pattern = re.compile(r'oia-' + request_id + r'(-\d+)?-attachment.*\..+', re.IGNORECASE)



    # List to store found attachments
    attachments = []

    # Find all <a> tags that match the attachment pattern
    for link in soup.find_all('a', href=True):
        if attachment_pattern.search(link['href']):
            attachment_info = link['href']  # Store only the URL
            attachments.append(attachment_info)

    return attachments




print("Crawling 2024 - 2023 Data")

response = requests.get('https://www.nzta.govt.nz/about-us/official-information-act/official-information-act-responses/')
soup = BeautifulSoup(response.content, 'html.parser')

results_2024_2023 = nzta_oia_crawler_preparation(soup)


# Loop over each response in the results list to find and attach related attachments
for result in results_2024_2023:
    response_filename = result['url']
    related_attachments = find_related_attachments_2024_2023(response_filename)
    result['attachments'] = related_attachments

# Output the results with attached attachments
print("Sample Results:")
for result in results_2024_2023[0:3]:
    print(f"URL: {result['url']}")
    print(f"Response Letter: {result['response_letter']}")
    print(f"Preceding <p>: {result['preceding_p']}")
    print(f"Preceding <h3>: {result['preceding_h3']}")
    print(f"Month: {result['month']}")
    print(f"Year: {result['year']}")
    print("Attachments:")
    for attachment in result['attachments']:
        print(f"  - {attachment}")
    print("=" * 40)





# Loop over each response in the results list to find and attach related attachments

print("Crawling Non-Media Data")

response = requests.get('https://www.nzta.govt.nz/about-us/official-information-act/official-information-act-responses/non-media-official-information-act-oia-responses/')
soup = BeautifulSoup(response.content, 'html.parser')

results_non_media = nzta_oia_non_media_crawler_preparation(soup)
for result in results_non_media:
    response_filename = result['url']
    related_attachments = find_related_attachments_non_media(response_filename)
    result['attachments'] = related_attachments

# Output the results with attached attachments
print("Sample Results:")
for result in results_non_media[0:3]:
    print(f"URL: {result['url']}")
    print(f"Response Letter: {result['response_letter']}")
    print(f"Preceding <p>: {result['preceding_p']}")
    print(f"Preceding <h3>: {result['preceding_h3']}")
    print(f"Year: {result['year']}")
    print("Attachments:")
    for attachment in result['attachments']:
        print(f"  - {attachment}")
    print("=" * 40)


print("Crawling Media Data")
response = requests.get('https://www.nzta.govt.nz/about-us/official-information-act/official-information-act-responses/media-official-information-act-oia-responses/')
# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

results_media = nzta_oia_media_crawler_preparation(soup)



# Loop over each response in the results list to find and attach related attachments
for result in results_media:
    response_filename = result['url']
    related_attachments = find_related_attachments_media(response_filename)
    result['attachments'] = related_attachments

# Output the results with attached attachments
print("Sample Results:")
for result in results_media[0:3]:
    print(f"URL: {result['url']}")
    print(f"Response Letter: {result['response_letter']}")
    print(f"Preceding <p>: {result['preceding_p']}")
    print(f"Preceding <h3>: {result['preceding_h3']}")
    print(f"Year: {result['year']}")
    print("Attachments:")
    for attachment in result['attachments']:
        print(f"  - {attachment}")
    print("=" * 40)

all_results = results_2024_2023 + results_non_media + results_media

# Save to a file
with open('nzta_file_metadata.pkl', 'wb') as file:
    pickle.dump(all_results, file)


# List of month names for extraction
MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

def extract_month(text):
    """
    Extracts the first occurrence of a month name from the given text.

    Parameters:
        text (str): The text to search for a month.

    Returns:
        str: The found month name or 'Unknown' if no month is found.
    """
    for month in MONTHS:
        if month.lower() in text.lower():
            return month
    return 'Unknown'

def download_file(url, save_path):
    """
    Downloads a file from the given URL and saves it to the specified path.

    Parameters:
        url (str): The URL of the file to download.
        save_path (str): The local file path to save the downloaded file.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")

def main(all_results):
    """
    Processes the results to download files organized by year and month.

    Parameters:
        all_results (list): A list of result dictionaries containing file information.
    """
    base_url = 'https://www.nzta.govt.nz'
    base_dir = "transport_data/nzta"
    printed_years = set()

    for result in tqdm(all_results, desc="Processing Results", unit="file"):
        # Extract and validate the year
        year_str = result.get('year', '').strip()
        try:
            year = int(year_str)
        except ValueError:
            print(f"Invalid year '{year_str}' in result. Skipping entry.")
            continue

        # Determine the month based on the year
        if year <= 2022:
            preceding_p = result.get('preceding_p', '')
            month = extract_month(preceding_p)
        else:
            month = result.get('month', 'Unknown')

        # Print the year being downloaded only once
        if year not in printed_years:
            print(f"📂 Downloading files for year {year}")
            printed_years.add(year)

        # Define the directory path
        dir_path = os.path.join(base_dir, str(year), month)
        os.makedirs(dir_path, exist_ok=True)

        # Download the main response letter PDF
        response_relative_url = result.get('url', '')
        if not response_relative_url:
            print("No URL found for response letter. Skipping.")
            continue
        response_url = base_url + response_relative_url
        response_filename = os.path.basename(response_relative_url)
        response_save_path = os.path.join(dir_path, response_filename)
        download_file(response_url, response_save_path)

        # Download all attachments
        attachments = result.get('attachments', [])
        for attachment_relative_url in attachments:
            attachment_url = base_url + attachment_relative_url
            attachment_filename = os.path.basename(attachment_relative_url)
            attachment_save_path = os.path.join(dir_path, attachment_filename)
            download_file(attachment_url, attachment_save_path)


    # Example usage:
    # Replace the following list with your actual `all_results` data
print("Downloading Files")
main(all_results)




print("Downloading Sample Simple Files")
# Download simple files
simple_files = pd.read_csv('reference_tables/simple_files.csv')

# loop over the rows in simple files and select the Link column
# find the ntry in all_results that matches the link and download that link and the attatchments if any into testing_data/simple_files


for index, row in simple_files.iterrows():
    link = row['Link']
    #print(link)
    for result in all_results:
        if 'https://www.nzta.govt.nz' + result['url'] == link:
            
            # Make the directory if it doesn't exist
            os.makedirs('transport_data/sample_files/nzta/simple_files/', exist_ok=True)
            print(f'transport_data/sample_files/nzta/simple_files/{link.split("/")[-1]}')
            response = requests.get(link)
            with open(f'transport_data/sample_files/nzta/simple_files/{link.split("/")[-1]}', 'wb') as f:
                f.write(response.content)
            for attachment in result['attachments']:
                response = requests.get(attachment)
                with open(f'testing_data/simple_files/{attachment.split("/")[-1]}', 'wb') as f:
                    f.write(response.content)


print("Downloading Sample Annexed Files")

# Download annexed files
annexed_files = pd.read_csv('reference_tables/annexed_files.csv')
# select only half of the annexed files rows
# loop over the rows in annexed files and select the Link column
# find the ntry in all_results that matches the link and download that link and the attatchments if any into testing_data/annexed_files
for index, row in annexed_files.iterrows():
    link = row['Link']
    #print(link)
    for result in all_results:
        if 'https://www.nzta.govt.nz' + result['url'] == link:
            
            print(f"file found")
            response = requests.get(link)
            # make dir transport_data/sample_files/nzta/annexed_files

            os.makedirs('transport_data/sample_files/nzta/annexed_files', exist_ok=True)
            with open(f'transport_data/sample_files/nzta/annexed_files/{link.split("/")[-1]}', 'wb') as f:
                f.write(response.content)
            for attachment in result['attachments']:
                print(f"found attachment")
                response = requests.get('https://www.nzta.govt.nz' + attachment)
                with open(f'transport_data/sample_files/nzta/annexed_files/{attachment.split("/")[-1]}', 'wb') as f:
                    f.write(response.content)