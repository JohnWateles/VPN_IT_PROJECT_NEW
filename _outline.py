import pyautogui
import psutil
import subprocess
import time
import ctypes
import win32gui
import win32con
import win32process


def resize_window(hwnd, x, y, width=None, height=None):
    if (width is None) or (height is None):
        _, _, width, height = get_window_info(hwnd)
    # Используем SetWindowPos для изменения размера и положения окна
    win32gui.SetWindowPos(hwnd, 0, x, y, width, height, win32con.SWP_NOZORDER)


def get_window_info(hwnd):
    # Получаем прямоугольник окна относительно экрана
    rect = win32gui.GetWindowRect(hwnd)
    x, y, right, bottom = rect
    width = right - x
    height = bottom - y
    return x, y, width, height


def terminate_outline():
    all_pids = list()
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Outline.exe':
            proc.terminate()


def start_outline():
    terminate_outline()
    outline_path = r"C:\Program Files (x86)\Outline\Outline.exe"
    process = subprocess.Popen(outline_path)
    return process


def stop_outline(outline):
    outline.terminate()


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
    time.sleep(0.4)
    windows = get_windows_by_pid(outline.pid)
    hwnd = windows[0]
    resize_window(hwnd, 10, 10, 10, 10)
    time.sleep(0.2)
    for i in range(4):
        pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(0.05)
    hide_window(windows[0])
    return windows[0]


def show_and_disconnect(hwnd):
    show_window(hwnd)
    pyautogui.press("enter")


def test_new():
    outline = start_outline()
    hwnd = connect_and_hide(outline)

    time.sleep(5)

    show_and_disconnect(hwnd)
    stop_outline(outline)


if __name__ == "__main__":
    test_new()
