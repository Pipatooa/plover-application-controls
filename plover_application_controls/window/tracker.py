from __future__ import annotations

import sys
import time
from threading import Thread
from typing import Callable

from plover.log import info

from plover_application_controls.pywinctl import getActiveWindow, BaseWindow
from plover_application_controls.window.history import WindowHistory
from plover_application_controls.window.details import WindowDetails


SLOW_PLATFORMS = {"darwin"}


class WindowTracker:
    _t = None
    _run = 0

    if sys.platform in SLOW_PLATFORMS:
        CHECK_INTERVAL = 0.25
    else:
        CHECK_INTERVAL = 0.1

    UNKNOWN = "UNKNOWN"
    BLANK_DETAILS = WindowDetails(hash(None), None, UNKNOWN, UNKNOWN, UNKNOWN)

    current_window = None
    current_window_details = BLANK_DETAILS

    _callbacks = []

    @staticmethod
    def check_active_window() -> None:
        old_details = WindowTracker.current_window_details

        try:
            WindowTracker.current_window = getActiveWindow()
            WindowTracker._get_window_properties()
        except Exception as e:
            info(f"{e}")
            WindowTracker.current_window = None
            WindowTracker.current_window_details = WindowTracker.BLANK_DETAILS

        change = old_details != WindowTracker.current_window_details
        if change and WindowTracker.current_window is not None:
            WindowHistory.push(WindowTracker.current_window_details)
        WindowTracker._trigger_callbacks(change)

    @staticmethod
    def _get_window_properties() -> None:
        handle = WindowTracker.current_window.getHandle()

        try:
            app_name = WindowTracker.current_window.getAppName()
        except:
            app_name = WindowTracker.UNKNOWN

        try:
            class_name = handle.get_wm_class()[0]
        except:
            class_name = WindowTracker.UNKNOWN

        try:
            title = WindowTracker.current_window.title
        except:
            title = WindowTracker.UNKNOWN

        WindowTracker.current_window_details = WindowDetails(
            hash(handle), WindowTracker.current_window,
            app_name, class_name, title
        )

    @staticmethod
    def _trigger_callbacks(change: bool) -> None:
        for on_change, callback in WindowTracker._callbacks:
            if on_change and not change:
                continue
            callback(WindowTracker.current_window, WindowTracker.current_window_details)

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
    def add_callback(on_change: bool, callback: Callable[[BaseWindow | None, WindowDetails], None]) -> None:
        WindowTracker._callbacks.append((on_change, callback))

    @staticmethod
    def remove_callback(on_change: bool, callback: Callable[[BaseWindow | None, WindowDetails], None]) -> None:
        WindowTracker._callbacks.remove((on_change, callback))
