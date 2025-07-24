# gfetch-cli - save gmail emails locally

The CLI version of [gfetch-web](https://github.com/jwjacobson/gfetch-web)!

This app helps you create local backups of your Gmail emails. It saves raw .eml files, cleaned .txt files, and attachments, each to their own directory.

 It is built using [Python](https://www.python.org/) and the [Gmail API](https://developers.google.com/workspace/gmail/api/reference/rest).

## Installation (using [uv](https://docs.astral.sh/uv/))
[Clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository):
```bash
git clone git@github.com:jwjacobson/gfetch-cli.git
```
Navigate to the `gfetch-cli` directory:
```bash
cd gfetch-cli
```
Install dependencies:
```bash
uv sync
```
Create a `.env` file from the provided template:
```bash
cp env-template .env
```
If you use the default values from env-template, the project layout will be as follows:
```
src
└── gfetch
    ├── cleaned_emails
    │   └── attachments
    ├── raw_emails
    ├── credentials.json
    └── token.json
    (.py files omitted for clarity)
```
> [!NOTE]
> - The `cleaned_emails`, `raw_emails`, and `attachments` directories are not part of the repo, but will be created when you run the app.
> - You have to manually download `credentials.json` (see "Setting up Google Cloud" below); `token.json` will be generated automatically when you authenticate with the app.

> [!WARNING]
> `credentials.json` contains sensitive data and should not be put in version control. It is already listed in `.gitignore` but might not be covered if you change the filename.

## Setting up Google Cloud
1. Go to the [Google Cloud Console](https://console.cloud.google.com/welcome/) and create an account if you don't have one
2. Using the navigation menu in the top-left of the screen, go to ```APIs & Services```, then ```Enable APIs and Services```
3. Search ```gmail``` in the box and find the Gmail API, then enable it
4. In the ```APIs & Services``` menu, click ```Credentials```, then click ```Create Credentials```, then ```OAuth Client ID```
5. For application type, select `Desktop App` and name it how you desire -- perhaps `gfetch`?
6. Follow the prompts to generate credentials
7. Once you've created the credentials, must download them immediately, as you won't be able to access them again once you've left the confirmation screen.  Download the credentials JSON and save it as `credentials.json` in `src/gfetch/`

## Running gfetch
```bash
uv run gfetch
```
Or, if you have [Just](https://github.com/casey/just) installed:
```bash
just run
```
Follow the onscreen instructions to back up your emails!

> [!NOTE]
> At present, Gfetch only allows you to download *all* correspondence with a given address.

If you don't have a valid token, your default browser will open for you to authenticate with the account of your choice when you enter a correspondent's email. You will also have to grant access to Gfetch in order to download your emails. I promise I'm not doing anything with them! (terms of service to be published soon)

### License
Gfetch is [free software](https://www.fsf.org/about/what-is-free-software), released under version 3.0 of the GPL. Everyone has the right to use, modify, and distribute gfetch subject to the [stipulations](https://github.com/jwjacobson/gfetch-cli/blob/main/LICENSE) of that license.
