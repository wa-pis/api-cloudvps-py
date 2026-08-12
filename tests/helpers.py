class FakeResponse:
    def __init__(self, status_code=200, payload=None, *, text="", content=None):
        self.status_code = status_code
        self.payload = {"ok": True} if payload is None else payload
        self.text = text
        self.content = content if content is not None else b"{}"

    def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


class FakeSession:
    def __init__(self, responses=None):
        self.calls = []
        self.responses = list(responses or [])
        self.closed = 0

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.responses.pop(0) if self.responses else FakeResponse()

    def close(self):
        self.closed += 1
