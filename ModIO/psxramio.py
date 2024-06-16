import psutil
from pymem import Pymem
from pymem.exception import ProcessNotFound

from ModIO.pymemio import PymemIO


class PsxRamIO(PymemIO):
    def __init__(self, base_address):
        super().__init__(None, base_address=base_address)

    def _inject(self, process_name=None):
        injected = False
        while not injected:
            program_name = [x for x in psutil.process_iter() if "duckstation" in x.name()][0].name()
            try:
                self.pm = Pymem(program_name)
                injected = True
            except ProcessNotFound:
                pass
        if not injected:
            raise ProcessNotFound
