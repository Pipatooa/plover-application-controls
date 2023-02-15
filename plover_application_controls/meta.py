from plover.formatting import _Context, _Action

from plover_application_controls.window_tracker import WindowTracker


def meta(ctx: _Context, cmdline: str) -> _Action:
    action = ctx.new_action()
    action.text = ":".join(map(get_property, cmdline.split(":")))
    return action


def get_property(prop: str) -> str:
    return WindowTracker.current_window_details.get_property(prop)
