class Throbber:

    STYLES = ['spin', 'periods', 'pulse']

    def __init__(self, style: str):
        assert style in self.STYLES
        if style == 'spin':
            self.chars = ['|', '/', '-', '\\']

        if style == 'pulse':
            self.chars = ['*', ' ']

        if style == 'periods':
            self.chars = ['.', '..', '...', '....', '.....', '......']

        self.iteration = 0
        self.length = len(self.chars)

    def throb(self):
        print(f'\r{self.chars[self.iteration % self.length]}', end='')
        self.iteration += 1

    def reset(self):
        self.iteration = 0


if __name__ == '__main__':
    from time import sleep
    for style in Throbber.STYLES:
        t = Throbber(style)
        for i in range(50):
            t.throb()
            sleep(0.25)
