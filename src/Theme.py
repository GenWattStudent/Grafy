import customtkinter as ctk


secondary_color_light = "#3b8ed0"
secondary_color_dark = "#3b8ed0"
text_color_light = "#2b2b2b"
text_color_dark = "#dbdbdb"
bg_color_light = "#dbdbdb"
bg_color_dark = "#2b2b2b"
distinction_color = "#144870"


variable_theme = {
    "dark": {
        "node_color": secondary_color_dark,
        "edge_color": "white",
        "node_dragged_color": "green",
        "edge_dragged_color": "yellow",
        "node_selected_color": distinction_color,
        "edge_path_color": "red",
        "canvas_bg_color": bg_color_dark,
        "edge_selected_color": distinction_color,
        "text_color": text_color_dark,
        "intersection_color": "yellow",
        "secondary_color": secondary_color_dark
    },
    "light": {
        "node_color": secondary_color_light,
        "edge_color": "black",
        "node_dragged_color": "green",
        "edge_dragged_color": "yellow",
        "node_selected_color": distinction_color,
        "edge_path_color": "red",
        "edge_selected_color": distinction_color,
        "intersection_color": "yellow",
        "canvas_bg_color": bg_color_light,
        "text_color": text_color_light,
        "secondary_color": secondary_color_light
    }
}


class Theme:
    @staticmethod
    def get(prop_name: str, theme_name: str = ctk.get_appearance_mode()) -> str:
        return variable_theme[theme_name.lower()][prop_name]
