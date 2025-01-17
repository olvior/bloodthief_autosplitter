from PIL import ImageGrab, Image
import numpy as np
import time
import json
import mss

import asyncio

with open("config.json", 'r') as f:
    config_dict = json.load(f)


current_split = 0

use_routes = bool(config_dict["use_routes"])

routes = config_dict["routes"]
current_route = config_dict["current_route"]
current_splits = routes[current_route]["splits"]

if use_routes:
    print(f"Loaded splits for: {routes[current_route]['name']}")
else:
    print("Not loading splits")

width = int(config_dict["width"])
height = int(config_dict["height"])

end_screen_cost = int(config_dict["end_cost"])

wait_time = config_dict["wait_time"]

sct = mss.mss() # mss screenshot object

reset_key = config_dict["reset_key"]

hotkey_queue = asyncio.Queue()

async def queue_handler():
    while True:
        value = await hotkey_queue.get()
        split(4)

def r_press():
    global restarts
    restarts += 1
    hotkey_queue.put_nowait('')
    hotkey_queue._loop._write_to_self()
    print(f"restart no. {restarts}")

from pynput import keyboard

h = keyboard.GlobalHotKeys({reset_key: r_press}).start()

class ScreenShotArea():
    def __init__(self, bbox_ratio):
        bbox_pixels = (int(height * bbox_ratio[0]), int(width * bbox_ratio[1]), int(width * bbox_ratio[2]), int(height * bbox_ratio[3]))
        self.monitor = {"top": int(height*bbox_ratio[1]),
                        "left": int(width*bbox_ratio[0]), 
                        "width": int(width*bbox_ratio[2]) - int(width*bbox_ratio[0]),
                        "height": int(height*bbox_ratio[3]) - int(height*bbox_ratio[1])}

    def take_screen_shot(self):
        self.current_image = sct.grab(self.monitor)
        self.image_array = np.array(self.current_image).sum(axis=-1) // 3

class MonitorVariable():
    def __init__(self, screen_shot_area, comparison_image_path, activation_cost, on_activate_function, white_filter_on, split_type=None):
        self.screen_shot_area = screen_shot_area
        self.comparison_image = np.asarray(Image.open(comparison_image_path).convert('L'))
        self.activation_cost = activation_cost
        self.on_activate_function = on_activate_function
        self.white_filter_on = white_filter_on
        self.split_type = split_type

        self.activated = False
        self.current_cost = None

    def get_current_cost(self):
        current_image = self.screen_shot_area.image_array
        
        d = self.comparison_image - current_image
        if self.white_filter_on:
            d *= (self.comparison_image==255)

        self.current_cost = d.sum()

        return self.current_cost

    def every_frame(self):
        current_cost = self.get_current_cost()

        if current_cost == self.activation_cost:
            if not self.activated:
                self.activated = True
                
                if self.split_type:
                    self.on_activate(self.split_type)
                else:
                    self.on_activate()
        else:
            self.activated = False

    def on_activate(self, split_type=False):
        if split_type:
            self.on_activate_function(split_type)
        else:
            self.on_activate_function()

def split(split_type):
    global current_split
    
    do_split = False
    if not use_routes:
        do_split = True

    elif current_splits[current_split] == split_type:
        do_split = True

    if do_split:
        current_split += 1
        print(f"Split {current_split} at: {time.time() - run_start_time - restarts * restart_time}")
        asyncio.get_event_loop().create_task(wsock.split()) 


def reset_timer():
    global run_start_time, current_split, restarts, is_in_run
    run_start_time = time.time() - 0.05 # we first we the timer at about 0.1s 
    current_split = 0
    restarts = 0
    is_in_run = True
    print("Reset timer")
    asyncio.get_event_loop().create_task(wsock.start())

def on_end_timer():
    global potential_run_end
    potential_run_end = time.time() # it was consistantly 0.3s off, maybe the fade to black takes that long?
    print(f"run end maybe {potential_run_end - run_start_time}")

text_area = ScreenShotArea([0.44, 0.61, 0.55, 0.64]) #left, top, right, bottom, 844, 658, 1056, 691
#text_area = ScreenShotArea([0.61, 0.44, 0.11, 0.03]) #top, left, width, height,  658, 844, 1056, 691
timer_area = ScreenShotArea([0.503, 0.546, 0.536, 0.576]) #
#timer_area = ScreenShotArea([0.546, 0.503, 0.033, 0.033]) #

screen_shot_areas = [text_area, timer_area]

checkpoint_monitor = MonitorVariable(text_area, "images/reached_checkpoint.png", 0, split, True, 1)
key_message_monitor = MonitorVariable(text_area, "images/thatonekeyintut.png", 0, split, True, 3)
secret_message_monitor = MonitorVariable(text_area, "images/secret.png", 0, split, True, 2)

start_timer_monitor = MonitorVariable(timer_area, "images/timerzero.png", 0, reset_timer, True)
end_monitor = MonitorVariable(timer_area, "images/timerzero.png", end_screen_cost, on_end_timer, True)
# -1 = end, 1 = checkpoint, 2 = secret, 3 = thatonekey, 4 = reset

variable_monitors = [start_timer_monitor, checkpoint_monitor, key_message_monitor, end_monitor, secret_message_monitor]

potential_run_end = 0
run_start_time = 0

restarts = 0
restart_time = 0.15

is_in_run = False

async def main(app):
    global is_in_run

    start_message_said = False
    while True:
        time_start = time.time()
        
        for screenshot_area in screen_shot_areas:
            screenshot_area.take_screen_shot()
        
        for m in variable_monitors:
            m.every_frame()

        if time.time() > potential_run_end + 1 and end_monitor.activated and is_in_run:
            print(f"Run finished at {potential_run_end - run_start_time - restarts * restart_time}")
            is_in_run = False
            await wsock.set_game_time(potential_run_end - run_start_time - restarts * restart_time)
            split(-1)

        
        time_end = time.time()
        
        if is_in_run:
            await wsock.set_game_time(time.time() - run_start_time - restarts * restart_time)
        await asyncio.sleep(max(wait_time - (time_end - time_start), 0))

        if not start_message_said:
            print("Please connect livesplit to ws://localhost:8001")
            print("Connect before you play")
            start_message_said = True

from wsock import app, web
import wsock

async def start_background_tasks(app):
    asyncio.get_event_loop().create_task(queue_handler())

app.on_startup.append(start_background_tasks)

web.run_app(app, port=8001)

