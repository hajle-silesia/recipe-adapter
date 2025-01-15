class FileContentMonitor:
    _content_default = ""

    def __init__(self, producer):
        self._producer = producer

        self._content = self._content_default

    @property
    def content(self):
        return self._content

    def update(self, new_raw_content):
        self._update_data(new_raw_content)
        self._notify()

    def _update_data(self, new_raw_content):
        self._content = new_raw_content

    def _notify(self):
        self._producer.send(topic="file-content-monitor-topic",
                            value=self.content,
                            )
