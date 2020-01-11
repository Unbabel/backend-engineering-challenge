import json

from enki.StreamProcessor import StreamProcessor


class JsonDumper(StreamProcessor[dict, str]):
    def consume(self, data: str):
        """
        Dump data as a single line JSON.
        """
        self.emit(json.dumps(data))
