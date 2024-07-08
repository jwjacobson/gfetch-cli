# gmailfetcher - save gmail emails locally

This is a little project inspired by a personal need. It downloads all emails to or from an address in your gmail account. 

## Installation
1. Clone this repository
2, Navigate to the 'gmailfetcher' directory
3. Create a virtual environment ```python -m venv venv''' (Windows/Linux) or ```python3 -m venv venv``` (Mac).
4. Activate the virtual environment ```.\venv\Scripts\activate``` (Windows) or ```source venv/bin/activate```(Mac/Linux)
5. Install the necessary packages: ```pip install -r requirements.txt``` (Note: you can also install pip-tools then run ```pip-compile``` to generate a new requirements.txt)

## Setting up Google Cloud
1. Go the the [Google Cloud Console](https://console.cloud.google.com/welcome/) and create an account if you don't have one.
2. Using the navigation menu in the top-left of the screen, go to ```APIs & Services```, then ```Enable APIs and Services```.
3. Search ```gmail``` in the box and find the Gmail API, then enable it.
4. In the ```APIs & Services``` menu, click ```Credentials```, then click ```Create Credentials```, then ```OAuth Client ID```.
5. Follow the prompts to generate credentials.
6. Once you've created the credentials, you should see them on the main credentials page. Download the credentials JSON and save it to the gmailfetcher folder.
7. The first time you run the program you will need to authorize the app via your browser.

## Using the program
1. Set the EMAIL_ADDRESS variable in retrieve_emails.py to the address whose emails you want to get.
2. Run the program: ```python retrieve_emails.py```
3. If everything was set up correctly, the raw emails will be saved to the raw_emails directory, and the cleaned emails will be saved to the cleaned_mails directory!