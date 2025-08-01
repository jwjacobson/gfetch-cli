# gfetch-cli - save gmail emails locally

The CLI version of [gfetch-web](https://github.com/jwjacobson/gfetch-web)!

This app helps you create local backups of your Gmail emails. It saves raw .eml files, cleaned .txt files, and attachments, each to their own directory.

 It is built using [Python](https://www.python.org/) and the [Gmail API](https://developers.google.com/workspace/gmail/api/reference/rest).

> [!NOTE]
> The following instructions assume you are using [uv](https://docs.astral.sh/uv/).

## Running Gfetch without installation 
```
uvx gfetch
```
> [!NOTE]
> You will not be able to download emails without a valid `credentials.json` file (see [Setting up Google Cloud](https://github.com/jwjacobson/gfetch-cli?tab=readme-ov-file#setting-up-google-cloud)).

> [!WARNING]
> Invoking gfetch in this way will create a directory called `gfetch` and its subdirectories in your current working directory!

## Installation for local development
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
> - You have to manually download `credentials.json` (see [Setting up Google Cloud](https://github.com/jwjacobson/gfetch-cli?tab=readme-ov-file#setting-up-google-cloud) below); `token.json` will be generated automatically when you authenticate with the app.

> [!WARNING]
> `credentials.json` contains sensitive data and should not be put in version control. It is already listed in `.gitignore` but might not be covered if you change the filename.

## Setting up Google Cloud
For now, Gfetch requires you to create your own credentials to use it.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/welcome/) and create an account if you don't have one.
2. Using the navigation menu in the top-left of the screen, go to ```APIs & Services```, then ```Enable APIs and Services```.
3. Search ```gmail``` in the box and find the Gmail API, then enable it.
4. In the ```APIs & Services``` menu, click ```Credentials```, then click ```Create Credentials```, then ```OAuth Client ID```.
5. For application type, select `Desktop App` and name it how you desire -- perhaps `gfetch`?
6. Follow the prompts to generate credentials.
7. Once you've created the credentials, you must download them immediately, as you won't be able to access them again once you've left the confirmation screen.  Download the credentials JSON and save it as `credentials.json` in `src/gfetch/` or your `gfetch` directory (if you're using uvx).

## Running gfetch after local installation
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

If you don't have a valid token (`token.json` in the `gfetch` folder), your default browser will open for you to authenticate with the account of your choice when you enter a correspondent's email.

To download emails, must grant access to your Gmail account to Gfetch. Gfetch only requires read-only access to Gmail account, and your emails are saved on processed on your hard drive. They are never stored elsewhere or used for any other purpose. For more details, see the [terms of service](https://github.com/jwjacobson/gfetch-cli/blob/main/terms_of_service.md) and [privacy policy](https://github.com/jwjacobson/gfetch-cli/blob/main/privacy_policy.md).

### License
Gfetch is [free software](https://www.fsf.org/about/what-is-free-software), released under version 3.0 of the GPL. Everyone has the right to use, modify, and distribute gfetch subject to the [stipulations](https://github.com/jwjacobson/gfetch-cli/blob/main/LICENSE) of that license.
