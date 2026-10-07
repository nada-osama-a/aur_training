from time import time
from rich.console import Console

console = Console()

def send_Msg(msg):
    try:
        if isinstance(msg, BaseMsg):
            console.print(msg, style=msg.style)
        else:
            print(msg)
    except Exception as e:
        print( e)


class BaseMsg:
    def __init__(self, data: str):
        self._data = data

    @property
    def style(self) -> str:
        return ''  

    @property
    def data(self):
        return self._data

    def __str__(self):
        return self._data 

    def __len__(self):
        try:
            return len(str(self))
        except Exception as e:
            print(e)
            return 0

    def __eq__(self, other):
        try:
            if not isinstance(other, BaseMsg):
                return False
            return str(self) == str(other)
        except Exception as e:
            print(e)
            return False

    def __add__(self, other):
        try:
            if isinstance(other, BaseMsg):
                new_data = self.data + other.data
            elif isinstance(other, str):
                new_data = self.data + other
            else:
                raise TypeError("Unsupported addition type")

            return self.__class__(new_data)
        except Exception as e:
            print(e)
            return self  


class LogMsg(BaseMsg):
    def __init__(self, data):
        super().__init__(data)
        try:
            self._timestamp: int = int(time())
        except Exception:
            self._timestamp = 0  

    @property
    def style(self) -> str:
        return "black on yellow"

    def __str__(self):
        try:
            return f"[{self._timestamp}] {self._data}"
        except Exception as e:
            print( e)
            return self._data


class WarnMsg(LogMsg):
    @property
    def style(self) -> str:
        return "white on red"

    def __str__(self):
        try:
            return f"[!WARN][{self._timestamp}] {self._data}"
        except Exception as e:
            print(e)
            return self._data


if __name__ == '__main__':
        m1 = BaseMsg('Normal message')
        m2 = LogMsg('Log')
        m3 = WarnMsg('Warning')

        send_Msg(m1)
        send_Msg(m2)
        send_Msg(m3)
    