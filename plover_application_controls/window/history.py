from plover.formatting import _Action
from plover.log import error

from plover_application_controls.pywinctl import getAllWindows
from plover_application_controls.window.details import WindowDetails


class WindowHistory:
    _sync_t = None
    _sync_run = 0

    _history = []
    _windows = {}
    _tab_index = 0
    _tabbed = False

    _ignore_push = None

    @staticmethod
    def push(window: WindowDetails) -> None:
        if window.handle_hash == WindowHistory._ignore_push:
            return
        if WindowHistory._tabbed:
            WindowHistory.stop_cycle()
        try:
            WindowHistory._history.remove(window.handle_hash)
        except ValueError:
            pass
        WindowHistory._history.append(window.handle_hash)
        WindowHistory._windows[window.handle_hash] = window.window

    @staticmethod
    def sync_windows() -> None:
        try:
            windows = getAllWindows()
        except Exception as e:
            error(e)
            return
        handle_hashes = [hash(w.getHandle()) for w in windows]
        old_history = WindowHistory._history
        old_window_map = WindowHistory._windows
        WindowHistory._windows = dict(zip(handle_hashes, windows))
        WindowHistory._history = [h for h in handle_hashes if h not in old_window_map]
        WindowHistory._history.extend(h for h in old_history if h in WindowHistory._windows)

    @staticmethod
    def _filter_alive(handle: int) -> bool:
        try:
            return WindowHistory._windows[handle].isAlive
        except:
            return False

    @staticmethod
    def filter_alive() -> None:
        WindowHistory._history = list(filter(WindowHistory._filter_alive, WindowHistory._history))

    @staticmethod
    def cycle_by(n: int, initial_sync: bool) -> None:
        if initial_sync and not WindowHistory._tabbed:
            WindowHistory.sync_windows()
        else:
            WindowHistory.filter_alive()
        WindowHistory._tabbed = True
        WindowHistory._tab_index += n
        if len(WindowHistory._history) == 0:
            return
        index = (-1 - WindowHistory._tab_index) % len(WindowHistory._history)
        handle_hash = WindowHistory._history[index]
        window = WindowHistory._windows[handle_hash]
        window.activate()
        WindowHistory._ignore_push = handle_hash

    @staticmethod
    def stop_cycle() -> None:
        if not WindowHistory._tabbed:
            return
        WindowHistory._tabbed = False
        WindowHistory._ignore_push = None
        index = (-1 - WindowHistory._tab_index) % len(WindowHistory._history)
        handle_hash = WindowHistory._history[index]
        try:
            WindowHistory._history.remove(handle_hash)
        except ValueError:
            pass
        WindowHistory._history.append(handle_hash)
        WindowHistory._tab_index = 0

    @staticmethod
    def on_translated(old: [_Action], new: [_Action]) -> None:
        for action in new:
            if action.command is not None:
                if action.command.startswith("application:tab"):
                    return
                if action.command.startswith("application:cycle"):
                    return
        WindowHistory.stop_cycle()
