import src.constance as const


class DrawGraphConfig:
    def __init__(self, node_width: int = 120, width: float = const.SCREEN_WIDTH, height: float = const.SCREEN_HEIGHT, node_height: int = 50):
        self.width: float = width
        self.height: float = height
        self.current_x: float = 0
        self.current_y: float = 0
        self.y_margin: int = 60
        self.node_width: int = node_width
        self.node_height: int = node_height
