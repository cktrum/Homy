# Homy

## CI Status
[![Build Status](https://travis-ci.org/cktrum/Homy.svg?branch=master)](https://travis-ci.org/cktrum/Homy)

## Setup
### Installation
* Make sure python is installed
* Install all packages by running `pip install -r requirements.txt`

### Creating inital song database
* Adjust paths in `bluetoothSrv/config.json` to correspond to your local setup
* To create and fill a database, run: `python bluetoothSrv/setupLibrary.py`

## Testing
To run all tests within a test file, run: `python -m unittest tests.SongsLibraryTest`
