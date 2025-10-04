def time_string(seconds):
    out_string = ""
    if seconds > 3600:
        temp = int(seconds / 3600)
        seconds -= temp * 3600
        out_string += f"{temp} hrs "
    if seconds > 60:
        temp = int(seconds / 60)
        seconds -= temp * 60
        out_string += f"{temp} min "
    return out_string + f"{round(seconds, 1)} sec"


class IterationBar:
    from time import time

    def __init__(self, bar_length: int, tracking_object: str):
        self.step_counter = None
        self.full_char = '\u2588'
        self.empty_char = "\033[90m\u2588\033[0m"
        self.bar_length = bar_length
        self.title_str = tracking_object

        self.block_string = None
        self.space_string = None
        self.step = None
        self.start_time = None
        self.current_iter = None

    def start(self, total_iter: int):
        self.start_time = self.time()
        self.block_string = ""
        self.space_string = self.empty_char * self.bar_length
        self.step = total_iter / self.bar_length
        self.step_counter = 0
        self.current_iter = 0
        print(f"\n{self.title_str} progress:")

    def iterate(self):
        self.current_iter += 1
        if self.current_iter >= self.step * self.step_counter:
            self.step_counter += 1
            self.block_string = self.full_char * self.step_counter
            self.space_string = self.empty_char * (self.bar_length - self.step_counter)
        if self.current_iter % 2 == 0:
            print(f"\r{{{self.block_string}{self.space_string}| "
                  f"time elapsed: {time_string(self.time() - self.start_time)} }}", end='')

    def end(self):
        temp_s = self.full_char * self.bar_length
        print(f"\r{{{temp_s}| time elapsed: {time_string(self.time() - self.start_time)} }}")
        self.block_string = None
        self.space_string = None
        self.step = None
        self.start_time = None
        self.current_iter = None
        self.step_counter = None


class TimeBar:
    from time import time

    def __init__(self, bar_length: int, tracking_object: str):
        self.full_char = '\u2588'
        self.empty_char = "\033[90m\u2588\033[0m"
        self.title_str = tracking_object
        self.bar_length = bar_length

        self.total_seconds = None
        self.block_string = None
        self.space_string = None
        self.step = None
        self.step_counter = None
        self.start_time = None

    def start(self, total_seconds: float):
        self.start_time = self.time()
        self.total_seconds = total_seconds
        self.block_string = ""
        self.space_string = self.empty_char * self.bar_length
        self.step = total_seconds / self.bar_length
        self.step_counter = 0
        print(f"\n{self.title_str} progress:")

    def iterate(self):
        elapsed_time = self.time() - self.start_time
        if elapsed_time > self.step * self.step_counter:
            self.step_counter = round(elapsed_time / self.step)
            self.block_string = self.full_char * self.step_counter
            self.space_string = self.empty_char * (self.bar_length - self.step_counter)
            print(f"\r{{{self.block_string}{self.space_string}| total time: {time_string(self.total_seconds)} }}",
                  end='')

    def end(self):
        temp_s = self.full_char * self.bar_length
        print(f"\r{{{temp_s}| total time: {time_string(self.total_seconds)} }}")
        self.total_seconds = None
        self.block_string = None
        self.space_string = None
        self.step = None
        self.step_counter = None
        self.start_time = None


if __name__ == '__main__':
    from time import sleep
    from time import time

    inp = input("1. Iteration Bar\n2. Time Bar\nEnter choice: ")
    if inp == "1":
        iterations = 100
        iBar = IterationBar(50, "[tracking_object]")
        iBar.start(iterations)
        for i in range(iterations):
            iBar.iterate()
            sleep(.05)
        iBar.end()

        iterations = 50

        iBar.start(iterations)
        for i in range(iterations):
            iBar.iterate()
            sleep(.05)
        iBar.end()

    elif inp == "2":
        total_time = 5
        start_t = time()
        tBar = TimeBar(50, "[tracking_object]")

        tBar.start(total_time)
        while time() - start_t < total_time:
            tBar.iterate()
            sleep(.01)

        tBar.end()

        total_time = 10
        start_t = time()

        tBar.start(total_time)
        while time() - start_t < total_time:
            tBar.iterate()
            sleep(.01)

        tBar.end()
