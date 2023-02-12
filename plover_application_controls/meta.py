from plover.formatting import _Context, _Action

from plover_application_controls.window_tracker import WindowTracker


def meta(ctx: _Context, cmdline: str) -> _Action:
    action = ctx.new_action()
    action.text = ":".join(map(get_property, cmdline.split(":")))
    return action


def get_property(prop: str) -> str:
    if prop == "app":
        return _replace_unknown(WindowTracker.current_app)
    if prop == "class":
        return _replace_unknown(WindowTracker.current_class)
    if prop == "title":
        return _replace_unknown(WindowTracker.current_title)
    if prop == "":
        raise KeyError("No application name property specified")
    raise KeyError(f"Unknown window property {prop}")


def _replace_unknown(v: str) -> str:
    return v if v else "UNKNOWN"
