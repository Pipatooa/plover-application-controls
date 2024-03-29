from plover.engine import StenoEngine
from plover.misc import boolean

from plover_application_controls.window.history import WindowHistory
from plover_application_controls.window.tracker import WindowTracker


def command(engine: StenoEngine, arg: str) -> None:
    subcommand, *args = arg.split(":")
    if not subcommand:
        raise KeyError("No subcommand specified")
    _COMMAND_MAP[subcommand](*args)


def tab(n: str, initial_sync: str = "false") -> None:
    cycle(n, initial_sync)
    WindowHistory.stop_cycle()


def cycle(n: str, initial_sync: str = "false") -> None:
    n = int(n)
    initial_sync = boolean(initial_sync)
    WindowHistory.cycle_by(n, initial_sync)


def stop_cycle() -> None:
    WindowHistory.stop_cycle()


def sync_history() -> None:
    WindowHistory.sync_windows()


def close() -> None:
    WindowTracker.current_window.close()


def minimize() -> None:
    WindowTracker.current_window.minimize()


def maximize() -> None:
    WindowTracker.current_window.maximize()


def restore() -> None:
    WindowTracker.current_window.hide()


def hide() -> None:
    WindowTracker.current_window.hide()


def show() -> None:
    WindowTracker.current_window.show()


def activate() -> None:
    WindowTracker.current_window.activate()


def resize(x: str, y: str) -> None:
    x, y = int(x), int(y)
    WindowTracker.current_window.resize(x, y)


def resize_to(x: str, y: str) -> None:
    x, y = int(x), int(y)
    WindowTracker.current_window.resizeTo(x, y)


def move(x: str, y: str) -> None:
    x, y = int(x), int(y)
    WindowTracker.current_window.move(x, y)


def move_to(x: str, y: str) -> None:
    x, y = int(x), int(y)
    WindowTracker.current_window.moveTo(x, y)


def raise_window() -> None:
    WindowTracker.current_window.raiseWindow()


def lower_window() -> None:
    WindowTracker.current_window.lowerWindow()


def always_on_top(value: bool = None) -> None:
    WindowTracker.current_window.alwaysOnTop(value)


def always_on_bottom(value: bool = None) -> None:
    WindowTracker.current_window.alwaysOnBottom(value)


def send_behind() -> None:
    WindowTracker.current_window.sendBehind()


def accept_input(value: bool = None) -> None:
    WindowTracker.current_window.acceptInput(value)


_COMMAND_MAP = {
    "tab": tab,
    "cycle": cycle,
    "stop_cycle": stop_cycle,
    "sync_history": sync_history,
    "close": close,
    "minimize": minimize,
    "maximize": maximize,
    "restore": restore,
    "hide": hide,
    "show": show,
    "activate": activate,
    "resize": resize,
    "resize_to": resize_to,
    "move": move,
    "move_to": move_to,
    "raise_window": raise_window,
    "lower_window": lower_window,
    "always_on_top": always_on_top,
    "always_on_bottom": always_on_bottom,
    "send_behind": send_behind,
    "accept_input": accept_input
}
