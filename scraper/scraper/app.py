

class App():  
    def __init__(self):
        self.config = Config()

    def run(self, runner):
        runner(self.config)


class Config(dict):
    def from_object(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

