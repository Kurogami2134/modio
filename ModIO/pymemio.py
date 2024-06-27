from pymem import Pymem
from pymem.exception import ProcessNotFound
import os
from io import IOBase


class NoEOFError(Exception):
    def __init__(self):
        super().__init__("Process memory has no end of file.")


class CantTruncate(Exception):
    def __init__(self):
        super().__init__("Can't truncate process memory.")


class PymemIO(IOBase):
    def __init__(self, process_name: str | None, base_address: int = 0):
        self.offset = 0
        self.base_address = base_address
        self.pm: Pymem
        if process_name is not None:
            self._inject(process_name)

    def _inject(self, process_name: str):
        injected = False
        attempts = 0
        while not injected and attempts <= 3:
            try:
                self.pm = Pymem(process_name)
                injected = True
            except ProcessNotFound:
                attempts += 1
        if not injected:
            raise ProcessNotFound

    def close(self):
        self.pm.close_process()
        return super().close()

    def seekable(self):
        return not self.closed

    def readable(self):
        return not self.closed

    def writable(self):
        return not self.closed

    def seek(self, offset, whence=os.SEEK_SET):
        match whence:
            case os.SEEK_SET:
                self.offset = offset
            case os.SEEK_CUR:
                self.offset += offset
            case os.SEEK_END:
                raise NoEOFError
        return self.offset

    def truncate(self, size=None):
        raise CantTruncate

    def read(self, size):
        res = self.pm.read_bytes(self.base_address + self.offset, size)
        self.seek(size, os.SEEK_CUR)
        return res

    def write(self, data):
        res = self.pm.write_bytes(self.base_address + self.offset, data, len(data))
        self.seek(len(data), os.SEEK_CUR)
        return len(data)
