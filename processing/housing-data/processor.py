class Processor:
    def __init__(self):
        self.data = None
        self.input_path = None
        self.output_path = None

    def grab_data(self):
        pass

    def process(self):
        pass

    def create_data(self):
        self.grab_data()
        self.process()
        return self.data