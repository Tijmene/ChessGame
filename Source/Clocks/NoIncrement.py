from Source.Clocks.ChessClock import ChessClock
import time


class NoIncrement(ChessClock):

    def set_clock(self):
        self.remaining_time_player_1 = 600.0
        self.remaining_time_player_2 = 600.0
        return

    def set_clock_increment(self):
        self.time_increment = 0
        return


if __name__ == "__main__":
    clock = NoIncrement()
    clock.start()
    clock.print()
    time.sleep(2)
    clock.print()
    clock.switch()
    time.sleep(4)
    clock.print()
    clock.stop()

