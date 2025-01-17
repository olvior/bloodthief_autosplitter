
# Bloodthief autosplitter

This is an autosplitter that connects to [LivesplitOne](<https://one.livesplit.org/>) and takes screenshots to see when to split.

See `Installation` below


## The program:

- is an image based autosplitter;
- has a timer accurate to ~0.1s;
- can connect to livesplit via a websocket;
- can split on:
    - checkpoints,
    - secrets,
    - the first key in the tutorial level,
    - and pressing the reset key;
- starts and ends automatically;
- can follow a route to not split accidentaly.

It (probably) works on all platforms but was only tested on Linux

## Installation

You can use the program in two different ways, either the easy way by running an executable or the harder way by running a python file.

### With the executable

To run with the executable you must first download the respective zip file from the releases page.

Then extract it and run the file `main.exe` (simply `main` on Linux)`

It may take a second to startup, but it should launch a console and start printing out messages. 

However if this does not work you should try to install with python.


### With python

You must have [python](https://www.python.org/downloads/) installed

The autosplitter uses the following libraries:
- Pillow
- NumPy
- MSS
- AIOHTTP

To install the libraries, use:
```sh
python -m pip install Pillow numpy mss aiohttp pynput
```

Then simply download a zip of the code and extract it.

Then run `main.py` in the terminal.

To do this, open the command prompt/terminal.

Then enter `cd Downloads` to enter the downloads folder.

Then enter `cd ` with the name of the extracted code.

Then enter `python main.py` to run it.


## Usage

Once you have the program running, connect to livesplitone by entering `ws://localhost:8001` into the connect option.

<img width="267" alt="Screenshot 2024-07-11 at 17 13 09" src="https://github.com/olvior/bloodthief_autosplitter/assets/78297864/b8e93497-1f10-4104-95a4-6dc16c253e58">

<img width="526" alt="Screenshot 2024-07-11 at 17 13 29" src="https://github.com/olvior/bloodthief_autosplitter/assets/78297864/efc46cf7-540d-4242-8f4f-817e2fa38bdd">

<img width="267" alt="Screenshot 2024-07-11 at 17 13 56" src="https://github.com/olvior/bloodthief_autosplitter/assets/78297864/a72338b9-5e29-4d63-b057-f278a07c8e37">


There should be a confirmation message in both livesplitone and the terminal.

The timer should work immediatly afterwards, but see below to edit settings for more advanced usage.

However, the autosplitter will not work if you have a screen resolution other than 1080p

**If your screen is not 1920x1080, you _must_ take your own screenshots**

## Take your own screenshots:
To do this:
- run `configure.py`
- with the text area, take screenshots of the:
    - checkpoint text
    - found secret text
    - and the text that comes up after you get the first key in the tutorial level
- with the timer area, take a screenshot of the:
    - timer when it says 00:00, within the first second

Then replace the old images in `images/` with the ones you took


## Configuration

Edit the `config.json` file or use `configure.py` to change settings
- 'width' and 'height' are simply your screen's width and height
- 'wait_time' is the ammount of idle time between loops of the program, so if it is 0.1 the program will take screenshots 10 timer per seconds. Recommended values are between 0.1-0.02
- leave 'end_cost' as it is
- set 'use_routes' to 1 if you want to use a route, if not set it to 0
- 'routes' is a list with all the routes, a route is a dictionary with
    - a 'name' 
    - a list of 'splits'
    - the list of splits contains numbers where
    - -1 = end screen
    - 1 = checkpoint
    - 2 = secret
    - 3 = the first key in tutorial
- essentialy you can use routes to help the autosplitter not make mistakes and accidentaly split when it shouldn't


## Take your own screenshots:
To do this:
- run `configure.py`
- with the text area, take screenshots of the:
    - checkpoint text
    - found secret text
    - and the text that comes up after you get the first key in the tutorial level
- with the timer area, take a screenshot of the:
    - timer when it says 00:00, within the first second

Then replace the old images in `images/` with the ones you took

-- --

That should be it but feel free to ask for help if it doesn't work, my discord is `olvior`

