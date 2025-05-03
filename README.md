# GalaxyGeeksBot, a modular Telegram bot, written in Python

## How to use it
- Clone `https://github.com/el0xren/GalaxyGeeksBot`
- Execute `pip3 install .` to install all the dependencies
- Rename `example_config.env` to `config.env`
- Put a bot token in `config.env`
- Edit additional variables in `config.env`
- Launch the bot by typing

```bash
python3 -m tg_bot
```
## Variables
The following env variables are supported:
- `OWNER_ID`: Your Telegram ID.
- `BOT_API_TOKEN`: Your Bot token. Get one from @botfather.
- `BOT_ADMIN_USER_IDS`: Allowed users ID's.
- `SUPPORT_CHAT_ID`: Your support Chat ID.
- `CI_APPROVED_USER_IDS`: Allowed users ID's to use CI functions.
- `CI_MAIN_DIR`: This folder needs to contain every project sources with proper folder naming (e.g. if you want to use LineageOS-17.1 script, a folder called "LineageOS-17.1" with the sources synced must be present in the specified main CI folder, so when you launch the command it will cd into Lineage-17.1 folder and start building). DON'T add a slash at the end of the path (eg. /home/foo).
- `CI_CHANNEL_ID`: This variable contains the chat ID, the channel username or the channel ID that you want to use to post updates and build logs.
- `CI_UPLOAD_ARTIFACTS`: Set it to true to upload CI artifacts.
- `CI_ARTIFACTS_UPLOAD_METHOD`: Define what file hosting solution you want to use to upload artifacts, the supported methods are: `localcopy` (Copy artifacts to a local folder), `ftp` (FTP server uploading) and `sftp` (SFTP server uploading).
- `CI_UPLOAD_BASE_DIR`: The directory that must be cd'ed into before copying files.
- `CI_UPLOAD_HOST`: Host name of the server (if needed by the upload method).
- `CI_UPLOAD_PORT`: Server port (the default port depends on the upload method, e.g. forr FTP it's 21, for SFTP it's 22).
- `CI_UPLOAD_USERNAME`: Username for login to server (if needed).
- `CI_UPLOAD_PASSWORD`: Password for login to server (if needed)
- `CI_GITHUB_USERNAME`: Your GitHub username.
- `CI_GITHUB_TOKEN`: GitHub token with access to defined organization with create_repo and push permissions.
- `CI_TWRPDTGEN_GITHUB_ORG`: Name of GitHub organization used to store device trees.
- `CI_TWRPDTGEN_CHANNEL_ID`: Channel ID where to post new releases.
- `WEATHER_API_KEY`: Weather api get one from `https://openweathermap.org/api`.
- `WEATHER_TEMP_UNIT`: Supported values: Fahrenheit `imperial`, Celsius `metric`, Kelvin `empty`

## Features

- Module-based, so you can add and remove modules as you like
- Easy to understand
- It uses python-telegram-bot, one of the most used Telegram bot API library

## Modules included

- weather | Get weather updates of a city
- speedtest | Test bot's Internet connection speed
- ci | Automated CI system, you can trigger AOSP custom ROMs and custom recoveries building, with progress updating
- cowsay
- And more...

## Wiki

Want to see how this bot works or you want to create a module for this bot?

Head over to [the wiki](https://github.com/SebaUbuntu/tg_bot/wiki) for more informations

## Credits
[4PERTURE](https://github.com/4PERTURE)
