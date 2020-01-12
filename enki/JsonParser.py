import json

from enki.StreamProcessor import StreamProcessor


class JsonParser(StreamProcessor[str, dict]):
    def consume(self, data: str):
        """
        Data is single object of JSON.
        """
        self.emit(json.loads(data))
