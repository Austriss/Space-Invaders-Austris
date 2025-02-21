class Observer:
    def on_event(self, event):
        pass

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event=None): 

        for observer in self._observers:
            observer.on_event(event)