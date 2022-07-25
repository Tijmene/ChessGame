import abc
import time, threading


class ChessClock:
    """
    The abstract Clock class which defines common functionality to all Chess clocks.
    """
    __metaclass__ = abc.ABCMeta
    start_time: float
    remaining_time_player_1: float
    remaining_time_player_2: float
    time_increment: int

    active_clock = 1  # Player 1 always starts (player 1 should be assigned to white)
    clock_resolution = 0.01
    running = True

    def __init__(self):
        self.clock_thread = threading.Thread(target=self.decrease_active_clock)
        self.remaining_time_player_1, self.remaining_time_player_2 = self.set_start_clock()
        self.time_increment = self.set_clock_increment()

    @abc.abstractmethod
    def set_start_clock(self) -> [int, int]:
        """
        Sets the initial time on the clock for both players in seconds.
        :return: initial time for player1, initial time for player 2
        """
        pass

    @abc.abstractmethod
    def set_clock_increment(self) -> int:
        """
        Sets the clock increment in seconds which is added to the clock of the player who has just made the last move.
        :return: the clock increment in seconds
        """
        pass

    def start(self) -> None:
        """
        Starts the clock
        """
        self.remaining_time_player_1 = float(self.remaining_time_player_1)
        self.remaining_time_player_2 = float(self.remaining_time_player_2)
        self.start_time = time.time()
        self.clock_thread.start()

    def decrease_active_clock(self) -> None:
        """
        Function that is called repeatedly in its own thread and decreases the time on the clock of the active
        player.
        """
        while self.running:
            time.sleep(self.clock_resolution)
            if self.active_clock == 1:
                self.remaining_time_player_1 -= self.clock_resolution

            elif self.active_clock == 2:
                self.remaining_time_player_2 -= self.clock_resolution

    def switch(self) -> None:
        """
        Switch the active and inactive player.
        :return:
        """
        if self.active_clock == 1:
            self.remaining_time_player_1 += self.time_increment
            self.active_clock = 2

        elif self.active_clock == 2:
            self.remaining_time_player_2 += self.time_increment
            self.active_clock = 1

    def get_remaining_clock_time(self, player_number: int) -> str:
        """
        Retrieves the current clock time with 2 decimal point precision
        :return: the remaining time in decimals
        """
        if player_number == 1:
            return "%.2f" % self.remaining_time_player_1
        elif player_number == 2:
            return "%.2f" % self.remaining_time_player_2
        else:
            raise Exception("Player number should be 1 or 2")

    def __str__(self) -> str:
        """
        Get the current clock standing as a string representation
        :return: string representation of the clock
        """
        return f"Remaining Time player 1: {self.remaining_time_player_1:.2f} \n" \
               f"Remaining Time player 2: {self.remaining_time_player_2:.2f}"

    def stop(self) -> None:
        """
        Stop the clock
        """
        self.running = False





