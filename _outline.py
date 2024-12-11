import pyautogui
import psutil
import subprocess
import os
import pygetwindow as gw
from pywinauto import Application
import time

import ctypes
import win32gui
import win32con
import win32process
from ctypes.wintypes import HWND


def get_outline_pid():
    all_pids = list()
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Outline.exe':
            print(proc)
            all_pids.append(proc.pid)
    print(all_pids)
    return all_pids[2]


def open_outline_window():
    outline_path = r"C:\Program Files (x86)\Outline\Outline.exe"
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Outline.exe':
            process = subprocess.Popen(outline_path)
            return proc.pid
    process = subprocess.Popen(outline_path)
    return process.pid


def close_outline_window(app):
    app.window().minimize()


def find_and_open_outline():
    outline_path = r"C:\Program Files (x86)\Outline\Outline.exe"
    app = Application(backend="uia").start(outline_path)
    return app


def click_on_button(path: str):
    button_location = pyautogui.locateCenterOnScreen(path)
    if button_location:
        pyautogui.click(button_location)
    else:
        print("Кнопка не найдена.")


def terminate_outline():
    all_pids = list()
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Outline.exe':
            proc.terminate()


def start_outline():
    # os.system(r"script.vbs")
    # os.system(r"script.vbs")
    terminate_outline()
    outline_path = r"C:\Program Files (x86)\Outline\Outline.exe"
    process = subprocess.Popen(outline_path)
    return process


def stop_outline(outline):
    outline.terminate()


def show_and_disconnect(hwnd):
    show_window(hwnd)
    time.sleep(0.2)
    click_on_button("active_button_image.png")


def hide_window(hwnd):
    ctypes.windll.user32.ShowWindow(hwnd, 0)


def show_window(hwnd):
    ctypes.windll.user32.ShowWindow(hwnd, 5)


def get_windows_by_pid(pid):
    windows = []

    def enum_windows_callback(hwnd, lParam):
        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
        if window_pid == pid:
            windows.append(hwnd)

    win32gui.EnumWindows(enum_windows_callback, None)
    return windows


def connect_and_hide(outline):
    pid = outline.pid
    click_on_button("button_image.png")
    windows = get_windows_by_pid(pid)
    hide_window(windows[0])
    return windows[0]


def main():
    outline = start_outline()
    time.sleep(1)
    hwnd = connect_and_hide(outline)
    time.sleep(7)
    print("off")
    show_and_disconnect(hwnd)
    time.sleep(0.5)
    stop_outline(outline)


if __name__ == "__main__":
    main()
