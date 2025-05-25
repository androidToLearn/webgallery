class Message:
    def __init__(self, message: str, sendTo: str, sendFrom: str, id: int, filename: str, isFrom_get: bool, isTo_get: bool):
        self.message = message
        self.sendTo = sendTo
        self.sendFrom = sendFrom
        self.id = id
        self.filename = filename
        self.isFrom_get = isFrom_get
        self.isTo_get = isTo_get
