try:
    from pywinctl import getActiveWindow, getAllWindows, BaseWindow
except ImportError:
    import sys
    import plover_application_controls.pywinctl.fake_tk as tkinter
    sys.modules["tkinter"] = tkinter
    from pywinctl import getActiveWindow, getAllWindows, BaseWindow
