# Homy

## Setup
### Installation
* Make sure python is installed
* Install eyed3: `pip install eyed3`
* Install python-magic: `pip install python-magic-bin==0.4.14`
* Install sqlalchemy: `pip install sqlalchemy`

### Creating inital song database
* Adjust paths in `bluetoothSrv/config.json` to correspond to your local setup
* To create and fill a database, run: `python bluetoothSrv/setupLibrary.py`

## Testing
To run all tests within a test file, run: `python -m tests.SongsLibraryTest`
