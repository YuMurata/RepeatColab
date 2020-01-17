from config import ColabPath


class RuntimeMode:
    CPU = ''
    GPU = 'GPU'
    TPU = 'TPU'


class ColabFile:
    def __init__(self, file_path: str, mode: RuntimeMode):
        self.path = file_path
        self.mode = mode


train_file = ColabFile(ColabPath.train, RuntimeMode.GPU)
evacuate_file = ColabFile(ColabPath.evacuate, RuntimeMode.CPU)
