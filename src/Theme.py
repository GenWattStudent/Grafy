
class Theme:
    def __init__(self):
        self.theme: dict[str, str] = {}

    def get(self, prop_name: str) -> str:
        if prop_name in self.theme:
            return self.theme[prop_name]
        raise Exception(f"Theme property {prop_name} not found")
    
    def set(self, prop_name: str, value: str):
        self.theme[prop_name] = value

theme = Theme()