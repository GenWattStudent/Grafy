import customtkinter as ctk

variable_theme = {
    "dark": {
        "node_color": "red",
        "edge_color": "white",
        "node_dragged_color": "green",
        "edge_dragged_color": "yellow",
        "node_selected_color": "blue",
        "edge_path_color": "red",
        "canvas_bg_color": "#2b2b2b",
        "text_color": "#dbdbdb",
        "intersection_color": "yellow",
        "secondary_color": "#3b8ed0"
    },
    "light": {
        "node_color": "grey",
        "edge_color": "black",
        "node_dragged_color": "green",
        "edge_dragged_color": "yellow",
        "node_selected_color": "blue",
        "edge_path_color": "red",
        "intersection_color": "yellow",
        "canvas_bg_color": "#dbdbdb",
        "text_color": "#2b2b2b",
        "secondary_color": "#3b8ed0"
    }
}


class Theme:
    @staticmethod
    def get(prop_name: str, theme_name: str = ctk.get_appearance_mode()) -> str:
        return variable_theme[theme_name.lower()][prop_name]
