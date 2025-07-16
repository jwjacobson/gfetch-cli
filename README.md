# gfetch-cli - save gmail emails locally

CLI version of [gfetch-web](https://github.com/jwjacobson/gfetch-web)

This app helps you create local backups of your Gmail emails and attachments.

## Installation (Using [uv](https://docs.astral.sh/uv/))
1. [Clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
2. Navigate to the 'gfetch-cli' directory
3. Install dependencies:
```bash
uv sync
```
4. Create a `.env` file from the provided template:
```bash
cp env-tempate .env
```

## Setting up Google Cloud
1. Go the the [Google Cloud Console](https://console.cloud.google.com/welcome/) and create an account if you don't have one
2. Using the navigation menu in the top-left of the screen, go to ```APIs & Services```, then ```Enable APIs and Services```
3. Search ```gmail``` in the box and find the Gmail API, then enable it
4. In the ```APIs & Services``` menu, click ```Credentials```, then click ```Create Credentials```, then ```OAuth Client ID```
5. Follow the prompts to generate credentials
6. Once you've created the credentials, you should see them on the main credentials page. Download the credentials JSON and save it to the value of CREDENTIALS in your `.env`

## Using the program
1. Run the program:
```bash
uv run src/gfetch/app.py
```
2. Follow the menu prompts to download or delete saved emails!

### License
Gfetch is [free software](https://www.fsf.org/about/what-is-free-software), released under version 3.0 of the GPL. Everyone has the right to use, modify, and distribute gfetch subject to the [stipulations](https://github.com/jwjacobson/gfetch-cli/blob/main/LICENSE) of that license.
