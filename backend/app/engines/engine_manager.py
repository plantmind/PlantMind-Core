class EngineManager:
    def __init__(self):
        self.engines = []

    def register(self, engine):
        self.engines.append(engine)

    def count(self):
        return len(self.engines)
