import ctypes
import os
import time

from core import core_timer

if "dd_dll" not in globals():
    dd_dll = None


class EMouse:
    Left = 0
    Right = 2
    Mid = 4
    Extend1 = 6
    Extend = 8


KeyMapping = {
    "ESC": 100,
    "F1": 101,
    "F2": 102,
    "F3": 103,
    "F4": 104,
    "F5": 105,
    "F6": 106,
    "F7": 107,
    "F8": 108,
    "F9": 109,
    "F10": 110,
    "F11": 111,
    "F12": 112,
    "~": 200,
    "1": 201,
    "2": 202,
    "3": 203,
    "4": 204,
    "5": 205,
    "6": 206,
    "7": 207,
    "8": 208,
    "9": 209,
    "0": 201,
    "-": 211,
    "=": 212,
    "\\": 213,
    "BACK": 214,
    "TAB": 300,
    "Q": 301,
    "W": 302,
    "E": 303,
    "R": 304,
    "T": 305,
    "Y": 306,
    "U": 307,
    "I": 308,
    "O": 309,
    "P": 310,
    "[": 311,
    "]": 312,
    "ENTER": 313,
    "CAPS": 400,
    "A": 401,
    "S": 402,
    "D": 403,
    "F": 404,
    "G": 405,
    "H": 406,
    "J": 407,
    "K": 408,
    "L": 409,
    ";": 410,
    "'": 411,
    "SHIFT": 500,
    "Z": 501,
    "X": 502,
    "C": 503,
    "V": 504,
    "B": 505,
    "N": 506,
    "M": 507,
    ",": 508,
    ".": 509,
    "/": 510,
    "RIGHTSHIFT": 511,
    "CTRL": 600,
    "WIN": 601,
    "ALT": 602,
    "SPACE": 603,
    "RIGHTALT": 604,
    "RIGHTFN1": 605,
    "RIGHTFN2": 606,
    "RIGHTCTRL": 607,
    "NUM": 810,
    "NUM/": 811,
    "NUM*": 812,
    "NUM-": 813,
    "NUM+": 814,
    "NUMENTER": 815,
    "NUM.": 816,
    "NUM0": 800,
    "NUM1": 801,
    "NUM2": 802,
    "NUM3": 803,
    "NUM4": 804,
    "NUM5": 805,
    "NUM6": 806,
    "NUM7": 807,
    "NUM8": 808,
    "NUM9": 809,
    "UP": 709,
    "LEFT": 710,
    "DOWN": 711,
    "RIGHT": 712,
}


def Initialize():
    from core.core_define import OpenAEJump
    if not OpenAEJump:
        return
    global dd_dll
    try:
        root = os.getcwd()
        path = f"{root}/resources/dll/driver_input.dll"
        print("path:", path)
        dd_dll = ctypes.CDLL(path)
        st = dd_dll.DD_btn(0)  # DD Initialize
        if st == 1:
            print("Driver Input Initialize OK")
        else:
            print("Driver Input Initialize Error")
    except FileNotFoundError:
        print(f'Error, DLL file not found')


def press(skey:str):
    skey=skey.replace(" ", "")
    skey=skey.upper()
    key_code = KeyMapping.get(skey, None)
    if key_code is None:
        print("按键不存在")
        return
    # print("模拟按键按下：", skey, int(time.time()*1000))
    dd_dll.DD_key(key_code, 1)

def release(skey:str):
    skey=skey.replace(" ", "")
    skey=skey.upper()
    key_code = KeyMapping.get(skey, None)
    if key_code is None:
        print("按键不存在")
        return
    # print("模拟按键释放：", skey, int(time.time()*1000))
    dd_dll.DD_key(key_code, 2)


def mouse_move(x, y):
    dd_dll.DD_mov(x, y)


def mouse_click(mouse_code):
    dd_dll.DD_btn(2 ** mouse_code)
    dd_dll.DD_btn(2 ** mouse_code * 2)


def input_str(s):
    dd_dll.DD_str(s)
