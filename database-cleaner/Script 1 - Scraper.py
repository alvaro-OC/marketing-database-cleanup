# -*- coding: utf-8 -*-
import csv
import os
import webbrowser
import pyautogui
import time
from bs4 import BeautifulSoup
from googlesearch import search

################################################################################
## STAGE 1: Opening the database, searching in Google, and saving HTML files. ##
################################################################################

database = 'sample_all_100.csv'  # Columns: email, status, first_name, last_name, company
file = open(database, encoding='utf-8')
reader = csv.DictReader(file)
temp_output = open("temp_output.csv", "wt", encoding='utf-8', newline='')
temp_headers = ['email', 'name', 'surname', 'status', 'country', 'company', 'duplicate', 'filename', 'muckrack.url']
writer = csv.DictWriter(temp_output, fieldnames=temp_headers, dialect='excel')
writer.writeheader()

# 1. Create a folder to save the websites (if doesn't exist).
if not os.path.exists('./muckrack'):
    os.mkdir('./muckrack')
    
# 2. Display prompt so that the download directory can be set correctly. Terminate if Cancelled.
download_folder_prompt = pyautogui.confirm(text='A Muckrack folder was created within the directory with the script. Please open your default browser and save anything to it, to make it the download location for the HTML files.', title='User attention required', buttons=['OK', 'Cancel'])
if download_folder_prompt == 'Cancel':
    raise ValueError('Cancelled. Terminarting the script.')
    
#3. PC-specific macros set-up.
# 3.1. Tab time - time required to open a tab.
while True:
    tab_time = pyautogui.prompt('Please choose the time needed to open and load a tab in the browser in seconds. Value must exceed 3.')
    if tab_time == 'Cancel':
        raise ValueError('Cancelled. Terminarting the script.')
    try:
        tab_time = int(tab_time)
        if tab_time >= 3:
            break
    except:
        pyautogui.alert(text='Make sure that the time is given as an integer greater or equal to 3.', title='Incorrect input', button='OK')
# 3.2. Download time - time required to dowload the HTML file.
while True:
    download_time = pyautogui.prompt('Please choose the time needed to download a ~42 bytes large HTML file in seconds. Value must exceed 3.')
    if download_time == 'Cancel':
        raise ValueError('Cancelled. Terminarting the script.')
    try:
        download_time = int(download_time)
        if download_time >= 3:
            break
    except:
        pyautogui.alert(text='Make sure that the time is given as an integer greater or equal to 3.', title='Incorrect input', button='OK')
# 3.3. Calculate the mouse position based on the resolution.   
width, height = pyautogui.size() # Returns screen resolution in the format (width, height).
mouse_x = width * 0.6
mouse_y = height * 0.7

# 4. Go through the database and extract the data to perform the Google search.
starting_prompt = pyautogui.confirm(text='Search is being started. Please do not move your mouse or use keyboard until being prompted to do so.', title='Starting search', buttons=['OK', 'Cancel'])
if starting_prompt == 'Cancel':
    raise ValueError('Cancelled. Terminarting the script.')

for r in reader:
    sites = []                  # List of links found for a given result
    name = r['first_name']      
    surname = r['last_name']
    company = r['company']
    status = r['status']
    email = r['email']
    country = r['country']
    company = r['company']
    slug_1 = (name + '-' + surname).lower() # Encountered slug variant 1
    slug_2 = (name + surname).lower() # Encountered slug variant 2
    expected_url_1 = 'https://muckrack.com/{0!s}'.format(slug_1)
    expected_url_2 = 'https://muckrack.com/{0!s}'.format(slug_2)
    query = name + ' ' + surname + ' ' + company + ' muckrack' # Google search
# 4. If the journalist is empty, ":) :)", or similar save what is in the database. Not excluding empty surnames as these sometimes yield results.
    if name == ':)' or name == 'Hello' or surname == ':)':
        writer.writerow({'email': email, 'name': name, 'surname': surname, 'status': status, 'country': country, 'company': company, 'duplicate': 'No'})
        continue
    if name == '' and surname == '':
        writer.writerow({'email': email, 'name': name, 'surname': surname, 'status': status, 'country': country, 'company': company, 'duplicate': 'No'})
        continue
    
# 5. Perform Google search.
    for j in search(query, tld="co.in", num=8, stop=8, pause=2):  # Returns first 8 results from Google.
# 5.1. Keep only urls that are from muckrack and include expected slugs.
        if j.find(expected_url_1) != -1 or j.find(expected_url_2) != -1:
            if j.find('articles') == -1 and j.find('bio') == -1 and j.find('#!') == -1 and j.find('media-outlet') == -1 and j.find('overview') == -1: 
                sites.append(j)
# 5.2. More general condition if e.g., there is a slug that doesn't match the pattern and returns an empty list:
        if not sites and j.find('https://muckrack.com') != -1:
            if j.find('articles') == -1 and j.find('bio') == -1 and j.find('#!') == -1 and j.find('media-outlet') == -1 and j.find('overview') == -1:
                sites.append(j)
# 5.3  If search failed, just save whatever is in the database               
    if not sites:
        writer.writerow({'email': email, 'name': name, 'surname': surname, 'status': status, 'country': country, 'company': company, 'duplicate': 'No'})
        continue
#    print(sites)   # For testing purposes
# 6. Open websites saved in the list and save them using macros.
    for index, site in enumerate(sites):
        webbrowser.open(site, autoraise=True) # Opens a window in the default browser.
        time.sleep(tab_time)
        pyautogui.moveTo(x=mouse_x, y=mouse_y) # Move cursor to the middle to ensure we're saving the web. Resolution dependent. Set for 1920 x 1200 for me
        pyautogui.hotkey('ctrl', 's') # Press CTRL+s to save the website.
        time.sleep(2)
# 6.1. File naming conventions in case of longer lists or empty ones.
        if len(sites) == 1:
            filename = slug_1 + '.html'
            duplicate = 'No'
        else:
            index = str(index)
            filename = slug_1 + '-' + index + '.html'
            duplicate = 'Yes'
        pyautogui.write(filename, interval=0.1) # Interval gives the time between typing each letter.
        pyautogui.press('enter')
        time.sleep(download_time) 
        pyautogui.hotkey('ctrl', 'w') # Closes the tab
        time.sleep(3)
        writer.writerow({'email': email, 'name': name, 'surname': surname, 'status': status, 'country': country, 'company': company, 'duplicate': duplicate, 'filename': filename, 'muckrack.url': site})
        
temp_output.close()   
file.close()
pyautogui.alert(text='Search has finished. You can use the mouse and keyboard now.', title='Search finished', button='OK')
