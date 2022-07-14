from source.Clocks.ChessClock import ChessClock
import time


class NoIncrement(ChessClock):
    """
    Clock with initial time of 10 minutes (600 seconds) and no increment.
    """

    def set_start_clock(self) -> [int, int]:
        initial_time = 600
        return initial_time, initial_time

    def set_clock_increment(self):
        time_increment = 0
        return time_increment


if __name__ == "__main__":
    clock = NoIncrement()
    clock.start()
    print(clock)
    time.sleep(2)
    print(clock)
    clock.switch()
    time.sleep(4)
    print(clock)
    clock.stop()

