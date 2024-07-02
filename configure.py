from PIL import ImageGrab, Image
import numpy as np
import time
import json

with open("config.json", 'r') as f:
    config_dict = json.load(f)

get_size_screenshot = ImageGrab.grab()
width, height = get_size_screenshot.size

config_dict["width"] = width
config_dict["height"] = height

def take_sceenshots():
    done = False
    while not done:
        print("\n\n\n\n\n")
        time.sleep(1)
        print("Do you want to take a screenshot of:")
        print("\nText area (for checkpoints, secrets, and the first tutorial key) [0]")
        print("Or the timer area (for the timer to start and end) [1]")
        choice = int(input("Type the number you want and hit enter: "))

        if choice == 0:
            bbox_ratio = [0.44, 0.61, 0.55, 0.64]
        
        elif choice == 1:
            bbox_ratio = [0.503, 0.546, 0.536, 0.576]

        else:
            print("Bad number")
            return

        bbox_pixels = (int(width * bbox_ratio[0]), int(height * bbox_ratio[1]), int(width * bbox_ratio[2]), int(height * bbox_ratio[3]))

        input("Once you press enter, after 3 seconds, it will take the screenshot")
        time.sleep(3)
        print(bbox_pixels)
        screenshot = ImageGrab.grab(bbox = bbox_pixels).convert("L")
        screenshot.save(f"image_at_{time.time()}.png", "PNG")
        screenshot.show()
        print("Rename the image taken now and replace the image you want to use with this one")
        input("Press enter when done")

        choice = input("Was this screenshot of the timer 00:00? y/[N]").lower()
        if choice == 'y':
            np_image = np.asarray(screenshot)
            cost = (np_image*(np_image==255)).sum()
            config_dict["end_cost"] = int(cost)
            print(cost)

        print("\n\n\n")
        a = input("Take another screenshot? [Y]/n").lower()
        if a == 'n':
            done = True

    

def change_settings():
    done = False

    while not done:
        print("\n\n\n\n")
        print("Select setting to change:")

        for idx, i in enumerate(config_dict.keys()):
            print(f"{i}, current value: {config_dict[i]} [{idx}]")
        

        choice = int(input())
        choice_key = list(config_dict.keys())[choice]
        print(choice_key)

        choice_type = type(config_dict[choice_key])
        new_value = choice_type(input(f"Enter the new value for {choice_key}: "))
        
        config_dict[choice_key] = new_value
        
        print("\n\n\n")
        a = input("Change another setting? [Y]/n ").lower()
        if a == 'n':
            done = True



done = False
while not done:
    print("Take screenshots [0]")
    print("Change settings  [1]")
    choice = int(input("Type the number you want and hit enter: "))

    if choice == 0:
        take_sceenshots()
    if choice == 1:
        change_settings()


    choice = input("Do you want to continue? y/[N] ").lower()
    
    if not choice == "y":
        done = True


with open("config.json", 'w') as f:
    json.dump(config_dict, f, indent=4)

