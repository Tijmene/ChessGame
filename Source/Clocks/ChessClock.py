import abc
import time, threading


class ChessClock:
    """ The metaclass Clock which defines common functionality to all clocks."""
    __metaclass__ = abc.ABCMeta
    start_time: float
    remaining_time_player_1: float
    remaining_time_player_2: float
    time_increment: int

    active_clock = 1  # Player 1 always starts (player 1 should be assigned to white)
    clock_checking_interval = 0.01
    running = True

    def __init__(self):
        self.clock_thread = threading.Thread(target=self.decrease_active_clock)
        self.set_clock()
        self.set_clock_increment()

    @abc.abstractmethod
    def set_clock(self):
        return

    @abc.abstractmethod
    def set_clock_increment(self):
        return

    def start(self):
        self.start_time = time.time()
        self.clock_thread.start()

    def decrease_active_clock(self):
        while self.running:
            time.sleep(self.clock_checking_interval)
            if self.active_clock == 1:
                self.remaining_time_player_1 -= self.clock_checking_interval

            elif self.active_clock == 2:
                self.remaining_time_player_2 -= self.clock_checking_interval

    def switch(self):
        if self.active_clock == 1:
            self.remaining_time_player_1 += self.time_increment
            self.active_clock = 2

        elif self.active_clock == 2:
            self.remaining_time_player_2 += self.time_increment
            self.active_clock = 1

        print(self.active_clock)

    def get_remaining_clock_time(self, player_number: int) -> float:
        """ Retrieves the current clock time with 2 decimal point precision """
        if player_number == 1:
            return "%.2f" % self.remaining_time_player_1
        elif player_number == 2:
            return "%.2f" % self.remaining_time_player_2
        else:
            raise Exception("Player number should be 1 or 2")

    def print(self):
        print("Remaining Time player 1: {remaining_time_1:.2f} \n"
              "Remaining Time player 2: {remaining_time_2:.2f}".format(remaining_time_1=self.remaining_time_player_1,
                                                                       remaining_time_2=self.remaining_time_player_2))

    def stop(self):
        self.running = False





