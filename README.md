# QQZone.downloader

[Chinese version](./README_zh.md)
Tool for downloading images, posts from qq zone

## Usage

- Create python virtual environments

    `python -m venv venv`
- Activate virtual environments

    `source venv/bin/activate`

- Install dependencies

    `pip install -r requirements.txt`

- Login in qq client, make sure web browser can detect login state automaticaly

- Running the following script

    `python run.py --account <qq_account> --save <save_directory>`


## Todo lists

- [x] Fix bugs when album is hidden by advertisment or un-clickable
- [x] Optimize runing efficiency, change forcive waiting to explicit waiting
- [x] Add new features, such as downloading image with upload time, comments and downloading posts
- [x] Add function for leaving message and diary
- [x] Build gui
- [x] Build exe


## Acknowledgement

I am a man who has heart-broken experiences using Tencent products!

## Welcome pull requests

If this do help you, please star~star~star

