
# Bloodthief autosplitter


### The program:

- is an image based autosplitter;
- has a timer accurate to ~0.1s;
- can connect to livesplit via a websocket;
- can split on:
    - checkpoints,
    - secrets,
    - and the first key in the tutorial level;
- starts and ends automatically
- can follow a route to not split accidentaly

It (probably) works on all platforms but was only tested on Linux

It used to be able to split when pressing 'r' but that no longer works

### Installation

You must have python installed

The autosplitter uses the following libraries:
- Pillow
- NumPy
- MSS
- AIOHTTP

To install the libraries, use:
```sh
pip install Pillow numpy mss aiohttp
```
Or:
```sh
python -m pip install Pillow numpy mss aiohttp
```

Then simply download a zip of the code, extract it, and run `main.py`

### Usage

When after you run `main.py` you should connect livesplitone and it should work.

To do this, go to settings, then go to the bottom and click 'connect', then enter enter the url, by default `ws://localhost:8001`

There should be a confirmation message in both livesplitone and the terminal.

The timer should work immediatly afterwards, but see below to edit settings for more advanced usage.

However, the autosplitter will not work if you have a screen resolution other than 1080p

**If your screen is not 1920x1080, you will have to take your own screenshots**

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


### Take your own screenshots:
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

