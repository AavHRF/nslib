import json
from models import Dispatch

class DispatchBuilder:

    def __init__(self, filename: str):
        self.file = filename
        self.dispatch = Dispatch()
