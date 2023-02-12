import time
from threading import Thread
from typing import Callable, Tuple

try:
    from pywinctl import getActiveWindow, BaseWindow
except ImportError:
    import sys
    import plover_application_controls.fake_tk as tkinter
    sys.modules["tkinter"] = tkinter
    from pywinctl import getActiveWindow, BaseWindow


class WindowTracker:
    _t = None
    _run = 0

    CHECK_INTERVAL = 0.25

    current_window = None
    current_app = ""
    current_class = ""
    current_title = ""

    _callbacks = []

    @staticmethod
    def check_active_window() -> None:
        try:
            WindowTracker.current_window = getActiveWindow()
            WindowTracker.current_title = WindowTracker.current_window.title
        except:
            WindowTracker.current_window = None
            WindowTracker.current_title = ""

        try:
            WindowTracker.current_app = WindowTracker.current_window.getAppName()
        except:
            WindowTracker.current_app = ""

        try:
            WindowTracker.current_class = WindowTracker.current_window.getHandle().get_wm_class()[0]
        except:
            WindowTracker.current_class = ""

        callback_contents = (WindowTracker.current_app, WindowTracker.current_class, WindowTracker.current_title)
        for callback in WindowTracker._callbacks:
            callback(WindowTracker.current_window, callback_contents)

    @staticmethod
    def _thread_work(run) -> None:
        while WindowTracker._run == run:
            WindowTracker.check_active_window()
            time.sleep(WindowTracker.CHECK_INTERVAL)

    @staticmethod
    def start() -> None:
        if WindowTracker._t is not None:
            return
        WindowTracker._t = Thread(target=WindowTracker._thread_work, args=[WindowTracker._run])
        WindowTracker._t.start()

    @staticmethod
    def stop() -> None:
        WindowTracker._run += 1
        WindowTracker._t = None

    @staticmethod
    def restart() -> None:
        WindowTracker.stop()
        WindowTracker.start()

    @staticmethod
    def add_callback(callback: Callable[[BaseWindow, Tuple[str, str, str]], None]) -> None:
        WindowTracker._callbacks.append(callback)

    @staticmethod
    def remove_change_callback(callback: Callable[[BaseWindow, Tuple[str, str, str]], None]) -> None:
        WindowTracker._callbacks.remove(callback)
