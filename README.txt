Software requirements:
- Python 3.9 with libraries:
	- BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
	- Google: https://pypi.org/project/google/
	- pyautogui: https://pyautogui.readthedocs.io/en/latest/
	- Should come pre-installed (at least in the Anaconda distribution): os, time, csv, webbrowser

IMPORTANT: COMPATIBILITY. Databases must be encoded in UTF-8. Practically, exports from Google Sheets are fine. Databases created from scratch in Excel are NOT. 
Excel does not like UTF-8 and changes non-English symbols to combinations that make the script crash.

How to use:
1. Put both scripts in the same folder as the database that is meant to be cleaned.
	Advice: Split database in smaller parts. In case of an error/manual stop, the script WILL save everything until that point, but the user would have to go through the entire database to find the spot where it stopped exactly and then split it.
2. Open Script 1. Change the variable "database" to the name of the database file. Do not remove '' signs.
	Advice: Check the names of columns in the CSV file and in the code. These can be found in lines 66-72, e.g. name = r['column_name']. If the corresponding columns have different names than in the code, please update the code accordingly.
3. Run Script 1. It will guide you through the next steps via displayed prompts.
	Advice: The average Muckrack HTML file is 42 bytes. This can help you estimate the download time needed. It is recommended to add an extra second to prevent cancelled downloads in case the network slows down or so.
4. After finishing work with Script 1, run Script 2. Similarly, it will communicate via prompts and should not require any additional modifications.
5. All extracted data will be in "muckrack_out.csv".
	Advice: If working with multiple databases, muckrack_out.csv will be overwritten each time the scripts are running. To keep all data, make sure to move it somewhere else, rename or change the name of the output CSV file in the "output = open('NAME.CSV'" part of line 16 in Script 2.
 
