import src.constance as const


class DrawGraphConfig:
    def __init__(self, radius: int = 15, width: float = const.SCREEN_WIDTH, height: float = const.SCREEN_HEIGHT):
        self.node_radius: int = radius
        self.width: float = width
        self.height: float = height
        self.current_x: float = 0
        self.current_y: float = 0
        self.y_margin: int = 60
        self.dragged_node_radius: int = 20
