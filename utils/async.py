import asyncio


class Loop:
    _loop = {
        'current': asyncio.get_event_loop,
        'new': asyncio.new_event_loop,
        'running': asyncio.get_running_loop
    }
    def __init__(self, kind: str, collapse: bool=False):
        assert kind in self._loop, f"Invalid kind: {kind!r} (available {'|'.join(self._loop)})"

        self.loop = self._loop[kind]
        self.collapse = collapse
        asyncio.set_event_loop(self.loop)

    def __enter__(self):
        return self.loop

    def __exit__(self, type, value, tb):
        if self.collapse:
            self.loop.close()
