from dataclasses import dataclass


@dataclass
class WindowDetails:
    handle_hash: int
    app_name: str
    class_name: str
    title: str

    def get_property(self, prop: str) -> str:
        if prop == "app":
            return self.app_name
        if prop == "class":
            return self.class_name
        if prop == "title":
            return self.title
        if prop == "":
            raise KeyError("No window property specified")
        raise KeyError(f"Unknown window property {prop!r}")
