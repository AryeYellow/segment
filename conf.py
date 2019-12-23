"""
https://blog.csdn.net/Yellow_python/article/details/80723272
"""
from time import time, strftime
END = '\033[0m'


class Color:

    @staticmethod
    def _wrap_colour(colour, args, prints, sep):
        if prints:
            for a in args:print(colour + '{}'.format(a) + END)
        return colour + sep.join('{}'.format(a) for a in args) + END

    @classmethod
    def background(cls, *args, prints=True, sep=' '):
        return cls._wrap_colour('\033[0;7m', args, prints, sep)

    @classmethod
    def background_yellow(cls, *args, prints=False, sep=' '):
        return cls._wrap_colour('\033[033;7m', args, prints, sep)

    @classmethod
    def blue(cls, *args, prints=True, sep=' '):
        return cls._wrap_colour('\033[94m', args, prints, sep)

    @classmethod
    def cyan(cls, *args, prints=True, sep=' '):
        return cls._wrap_colour('\033[96m', args, prints, sep)

    @classmethod
    def dark_blue(cls, *args, prints=False, sep=' '):
        return cls._wrap_colour('\033[34m', args, prints, sep)

    @classmethod
    def dark_cyan(cls, *args, prints=False, sep=' '):
        return cls._wrap_colour('\033[36m', args, prints, sep)

    @classmethod
    def dark_red(cls, *args, prints=False, sep=' '):
        return cls._wrap_colour('\033[031m', args, prints, sep)

    @classmethod
    def pink(cls, *args, prints=True, sep=' '):
        return cls._wrap_colour('\033[95m', args, prints, sep)

    @classmethod
    def red(cls, *args, prints=True, sep=' '):
        return cls._wrap_colour('\033[91m', args, prints, sep)

    @classmethod
    def yellow(cls, *args, prints=True, sep=' '):
        return cls._wrap_colour('\033[93m', args, prints, sep)

    @classmethod
    def highlight(cls, text, word):
        highlight_word = cls.background_yellow(word)
        len_w = len(word)
        len_t = len(text)
        for i in range(len_t - len_w, -1, -1):
            if text[i: i + len_w] == word:
                text = text[:i] + highlight_word + text[i + len_w:]
        print(text)

    @classmethod
    def hot(cls, value, half=.5):
        return cls.dark_blue(value) if value < half else cls.dark_red(value)

    @classmethod
    def bar(cls, value, maximum=1, label=''):
        length = int(value / maximum * 100)
        if label:
            print('\033[0;7m'+label.ljust(length, ' ')+END+cls.hot(value, maximum/2))
        return '#' * length


class Timer(Color):
    def __init__(self):
        self.t = time()

    def __del__(self):
        if self.__str__():
            self.background('耗时：%s' % self)

    def __str__(self):
        t = self.second
        if t < .2:
            return ''
        elif t < 60:
            return '%.2f秒' % t
        elif t < 3600:
            return '%.2f分钟' % (t / 60)
        else:
            return '%.2f小时' % (t / 3600)

    @property
    def second(self):
        return time() - self.t

    @classmethod
    def time(cls, fm='%Y-%m-%d %H:%M:%S'):
        return strftime(fm)


if __name__ == '__main__':
    t = Timer()
    Timer.blue('blue')
    Timer.cyan('cyan')
    print(t.dark_blue('dark', 'blue'))
    print(t.dark_cyan('dark', 'cyan'))
    print(t.dark_red('dark', 'red'))
    Color.pink('pink')
    Color.red('r', 'e', 'd')
    t.yellow('yellow')
    t.background('background', prints=False)
    print(Timer.time())
    print(t.highlight('一片一片又一片', '一片'))
    t.bar(30, 100, 'boy');t.bar(.7, 1, 'girl')
    print(t.bar(50, 100), 50);print(t.bar(.5, 1), .5)
    print(t);[i**2 for i in range(666666)];print(t)
