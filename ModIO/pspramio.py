import win32api
import win32gui
import pyautogui
from pymem import Pymem
from pymem.exception import ProcessNotFound

from ModIO.pymemio import PymemIO


class PspRamIO(PymemIO):
    def __init__(self):
        super().__init__(None)
        pywi = pyautogui.getWindowsWithTitle("PPSSPP")[0]
        wi = win32gui.FindWindow(None, pywi.title)
        retl = win32api.SendMessage(wi, 0x8000+0x3118, 0, 0)
        reth = win32api.SendMessage(wi, 0x8000+0x3118, 0, 1) << 32
        self.base_address = reth + retl
        self._inject()

    def _inject(self, process_name=None):
        injected = False
        while not injected:
            try:
                self.pm = Pymem("PPSSPPWindows64.exe")
                injected = True
            except ProcessNotFound:
                try:
                    self.pm = Pymem("PPSSPPWindows.exe")
                    injected = True
                except ProcessNotFound:
                    pass
        if not injected:
            raise ProcessNotFound
