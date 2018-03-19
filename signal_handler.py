import signal
import time


class SignalHandler():
    def __init__(self):
        self.exit = False

    def signal_handler(self, signal, frame):
        if signal == 2:
            print("Caught SIGINT")
            self.exit = True

        if signal == 15:
            print("Caught SIGTERM")
            self.exit = True

    def set_handler(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)


handler = SignalHandler()
handler.set_handler()

while True:
    print("hi")
    time.sleep(1)
    if handler.exit:
        break

