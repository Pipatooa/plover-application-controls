from plover.engine import StenoEngine

from plover_application_controls.window_tracker import WindowTracker


def command(engine: StenoEngine, arg: str) -> None:
    split_args = arg.split(":")
    if len(split_args) == 0:
        raise KeyError("No subcommand specified")
    subcommand, *args = split_args
    _COMMAND_MAP[subcommand](*args)


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
    "close": close,
    "minimize": minimize,
    "maximize": maximize,
    "restore": restore,
    "hide": hide,
    "show": show,
    "activate": activate,
    "resize": resize,
    "resizeTo": resize_to,
    "move": move,
    "move_to": move_to,
    "raise_window": raise_window,
    "lower_window": lower_window,
    "always_on_top": always_on_top,
    "always_on_bottom": always_on_bottom,
    "send_behind": send_behind,
    "acceptInput": accept_input
}
