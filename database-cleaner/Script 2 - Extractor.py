# -*- coding: utf-8 -*-
import csv
import os
import shutil
import pyautogui
import re
from bs4 import BeautifulSoup

###################################################
## STAGE 2: Extracting data from the HTML files. ##
###################################################

# 1. Open the temporary output file from the first script and create a CSV file for the extracted data.
file = open('temp_output.csv')
reader = csv.DictReader(file)
output = open('muckrack_out.csv', 'wt', encoding='utf-8', newline='')
output_header = ['email','name', 'surname', 'status', 'tags', 'location', 'journals', 'duplicate', 'muckrack.url', 'twitter', 'linkedin']
writer = csv.DictWriter(output, fieldnames=output_header, dialect='excel')
writer.writeheader()

# 2. Set the path to the directory with the HTML files. Assumes that it is a subfolder within the directory with the script.
parent_dir = os.path.dirname(__file__) # Read the path to current directory
sub_dir = os.path.join(parent_dir, 'muckrack')

# 3. Set user preferences regarding data handling (prompts).
delete_HTML_prompt = pyautogui.confirm(text='Do you want to delete the folder with the HTML files after the data is extracted?', title='User attention required', buttons=['Yes - Delete folder', 'No - Keep folder'])
empty_fields_keep_prompt = pyautogui.confirm(text='Some journalists do not have topic tags associated with them. Do you want to keep these entries? ', title='User attention required', buttons=['Yes - Keep entries', 'No - Exclude entries'])
empty_fields_fill_prompt = pyautogui.prompt(text='Please enter the expression/symbol that will be inserted into empty fields. Press Cancel to leave the fields blank.', title='User attention required' , default='')
if empty_fields_fill_prompt == 'Cancel':
    empty_fields_fill_prompt == ''

# 3.1. Define a function to determine row value, i.e., keep original if not empty or fill with the chosen expression.
def field_filler(row_value):
    if row_value == '':
        row_value = empty_fields_fill_prompt
    else:
        row_value = row_value
    return row_value

# 4. Iterate through the database again and extract HTML data for every entry.
for r in reader:
# 4.1. Extract data from the temporary CSV and fill accordingly.
    email = field_filler(r.get('email'))
    name = field_filler(r['name'])
    surname = field_filler(r['surname'])
    status = field_filler(r['status'])
    reported_country = field_filler(r['country'])
    reported_company = field_filler(r['company'])
    filename = field_filler(r['filename'])
    duplicate = field_filler(r['duplicate'])
    muckrack_url = field_filler(r['muckrack.url'])
    twitter = ''
    linkedin = ''
    try:
        file_path = os.path.join(sub_dir, filename)
        with open(file_path, encoding='utf-8') as html_file:
            html = html_file.read()
    except: # If there is no HTML file saved for any reason, fill the row with the known data.
        writer.writerow({'email': email, 'name': name, 'surname': surname, 'status': status, 'tags': empty_fields_fill_prompt, 'location': reported_country, 'journals': reported_company, 'duplicate': duplicate, 'muckrack.url': muckrack_url, 'twitter': empty_fields_fill_prompt, 'linkedin': empty_fields_fill_prompt})
        continue
# 4.2. Extract data from the HTML.    
    soup = BeautifulSoup(html, features="lxml")
    personal_details = soup.find('div', {'class': 'profile-details'})
    if personal_details:
        full_name = personal_details.find('h1').text.strip() # journalist's name
        beats = soup.find('div', {'class': 'person-details-item person-details-beats'})
        if beats:
            tags = [x.text.strip() for x in beats.find_all('a')] # tags/topics
            tags = ', '.join(tags)
        else:
            if empty_fields_keep_prompt == 'No - Exclude entries':
                continue
            else:    
                tags = empty_fields_fill_prompt
        companies = soup.find('div', {'class': 'profile-details-item'})
        if companies:
            journals = [x.text.strip() for x in companies.find_all('a')] # journals they've written for
            if 'more' in journals:  # Removes "more" that is sometimes present (and doesn't seem to be depending on the number of journals overall)
                journals.remove('more')
            journals = ', '.join(journals)
        else:
            journals = reported_company
        location = soup.find('div', {'class': 'person-details-item person-details-location'})
        if location:
            city = location.find('div').text.strip()
        else:  # If no location on Muckrack, fills it with the country reported in the database where available
                city = reported_country
    social_media = soup.find('div', {'class': 'profile-section-social'})
    if social_media:
        sm_links = [link.get('href') for link in social_media.find_all('a')]
        if sm_links:
            for link in sm_links:
                if link.find('twitter') != -1:
                    twitter = link
                if link.find('linkedin') != -1:
                    linkedin = link
            if not twitter:
                twitter = empty_fields_fill_prompt
            if not linkedin:
                linkedin = empty_fields_fill_prompt
# 4.3. Write the data in the CSV file.                    
    writer.writerow({'email': email, 'name': name, 'surname': surname, 'status': status, 'tags': tags, 'location': city, 'journals': journals, 'duplicate': duplicate, 'muckrack.url': muckrack_url, 'twitter': twitter, 'linkedin': linkedin })

# 5. Optional clean: Remove the temporary output file and the directory with the saved HTML files if the user chose to do so.
file.close()
output.close()
if delete_HTML_prompt == 'Yes - Delete folder':
    os.remove('temp_output.csv')
    shutil.rmtree(sub_dir)
pyautogui.alert(text='Data extaction has finished.', title='Data extraction finished', button='OK')
