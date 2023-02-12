from __future__ import annotations

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


SLOW_PLATFORMS = {"darwin"}


class WindowTracker:
    _t = None
    _run = 0

    if sys.platform in SLOW_PLATFORMS:
        CHECK_INTERVAL = 0.25
    else:
        CHECK_INTERVAL = 0.1

    current_window = None
    current_handle_hash = None
    current_app = ""
    current_class = ""
    current_title = ""

    _callbacks = []

    @staticmethod
    def check_active_window() -> None:
        old_handle_hash = WindowTracker.current_handle_hash
        old_title = WindowTracker.current_title

        try:
            WindowTracker.current_window = getActiveWindow()
            WindowTracker._get_window_properties()
        except:
            WindowTracker._unset_window()

        change = old_handle_hash != WindowTracker.current_handle_hash or old_title != WindowTracker.current_title
        WindowTracker._trigger_callbacks(change)

    @staticmethod
    def _get_window_properties() -> None:
        handle = WindowTracker.current_window.getHandle()
        WindowTracker.current_handle_hash = hash(handle)

        try:
            WindowTracker.current_app = WindowTracker.current_window.getAppName()
        except:
            WindowTracker.current_app = ""

        try:
            WindowTracker.current_class = handle.get_wm_class()[0]
        except:
            WindowTracker.current_class = ""

        try:
            WindowTracker.current_title = WindowTracker.current_window.title
        except:
            WindowTracker.current_title = ""

    @staticmethod
    def _unset_window() -> None:
        WindowTracker.current_window = None
        WindowTracker.current_handle_hash = hash(None)
        WindowTracker.current_app = ""
        WindowTracker.current_class = ""
        WindowTracker.current_title = ""

    @staticmethod
    def _trigger_callbacks(change: bool) -> None:
        details = (WindowTracker.current_app, WindowTracker.current_class, WindowTracker.current_title)
        for on_change, callback in WindowTracker._callbacks:
            if on_change and not change:
                continue
            callback(WindowTracker.current_window, WindowTracker.current_handle_hash, details)

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
    def add_callback(on_change: bool, callback: Callable[[BaseWindow | None, int, Tuple[str, str, str]], None]) -> None:
        WindowTracker._callbacks.append((on_change, callback))

    @staticmethod
    def remove_callback(on_change: bool, callback: Callable[[BaseWindow | None, int, Tuple[str, str, str]], None]) -> None:
        WindowTracker._callbacks.remove((on_change, callback))
