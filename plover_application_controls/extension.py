from plover.engine import StenoEngine

from plover_application_controls.window_tracker import WindowTracker

THREAD_INTERVAL = 0.25


class ApplicationControlExtension:
    def __init__(self, engine: StenoEngine) -> None:
        self._on = False
        self._engine = engine
        self._engine.hook_connect("output_changed", self.on_output_changed)

    def start(self) -> None:
        self._on = True
        WindowTracker.start()

    def stop(self) -> None:
        self._on = False
        WindowTracker.stop()

    def on_output_changed(self, enabled: bool) -> None:
        if self._on:
            if enabled:
                WindowTracker.start()
            else:
                WindowTracker.stop()
