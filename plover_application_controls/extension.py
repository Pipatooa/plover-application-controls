from plover.engine import StenoEngine
from plover.formatting import _Action

from plover_application_controls.window.history import WindowHistory
from plover_application_controls.window.tracker import WindowTracker

THREAD_INTERVAL = 0.25


class ApplicationControlExtension:
    def __init__(self, engine: StenoEngine) -> None:
        self._on = False
        self._engine = engine
        self._engine.hook_connect("output_changed", self.on_output_changed)
        WindowHistory.sync_windows()

    def start(self) -> None:
        self._on = True
        self._engine.hook_connect("translated", self.on_translated)
        WindowTracker.start()

    def stop(self) -> None:
        self._on = False
        WindowTracker.stop()
        self._engine.hook_disconnect("translated", self.on_translated)

    def on_output_changed(self, enabled: bool) -> None:
        if self._on:
            if enabled:
                WindowTracker.start()
            else:
                WindowTracker.stop()

    def on_translated(self, old: [_Action], new: [_Action]) -> None:
        WindowHistory.on_translated(old, new)
