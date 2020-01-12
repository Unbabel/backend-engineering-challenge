from typing import List, Callable

from enki.StreamProcessor import StreamProcessor


class ProcessorChain(StreamProcessor[str, str]):
    """
    Caller must ensure that:
        * First child accepts string,
        * Last child produces string
        * Children emit a type that can be consumed by the following child.
    """

    processors: [StreamProcessor]

    def __init__(self, sink: Callable[[str], None], children: List[Callable[[Callable], StreamProcessor]]):
        super().__init__(sink)

        self.processors = []
        current_sink = sink
        for fac in reversed(children):
            processor = fac(current_sink)
            self.processors.append(processor)
            current_sink = processor.consume

        self.processors.reverse()

    def consume(self, data: str):
        self.processors[0].consume(data)

    def end(self):
        for p in self.processors:
            p.end()
