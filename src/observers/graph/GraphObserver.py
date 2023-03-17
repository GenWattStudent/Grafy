from typing import Callable
from src.observers.Observer import Observer
from src.graph.GraphMatrix import GraphMatrix


class GraphObserver(Observer):
    def __init__(self, callback: Callable[[GraphMatrix], None]):
        super().__init__()
        self.callback = callback

    def update(self, value: GraphMatrix):
        self.callback(value)
