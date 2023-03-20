from copy import copy


class State:
    def __init__(self, initial_state):
        self._state = initial_state
        self._prev_state = initial_state
        self._subscribers = set()

    def get(self):
        return self._state

    def set(self, new_state):
        self._prev_state = copy(self._state)
        self._state = new_state
        self.notify_subscribers()

    def subscribe(self, subscriber):
        self._subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)

    def notify_subscribers(self):
        for subscriber in self._subscribers:
            subscriber(self._state, self._prev_state)
