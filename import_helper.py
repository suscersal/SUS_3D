import sys
import os



def install():
    os.system(f'{sys.executable} -m pip install -r requirements.txt')

try:
    from ursina import *
    import json
    import time
    import keyboard
    import termcolor
except ModuleNotFoundError:
   install()