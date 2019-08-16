from collections import deque


class Buffer:
    def __init__(self):
        self._queue = deque()
        self._use = 0
        self._d = 0

    def __fill(self):
        while self._use <= 16:
            try:
                pop = self._queue.pop()
                self._d |= (pop << (24 - 8 - self._use))
                self._use += 8
            except IndexError:
                break
        return self._use > 0

    def decode(self, data):
        self._queue.extendleft(data)
        while self.__fill():
            if self._d & 0x800000:
                # uncompressed
                data = (self._d >> (24 - 9)) & 0xFF
                self._d = (self._d << 9) & 0xFFFFFF
                self._use -= 9
                yield False, data
            else:
                # compressed
                offset = (self._d >> (24 - 11)) & 0x3FF
                if offset == 0:
                    break
                offset -= 1  # offset is one based
                length = ((self._d >> (24 - 15)) & 0xF) + 2
                self._d = (self._d << 15) & 0xFFFFFF
                self._use -= 15
                yield True, (offset, length)


class Decompressor:
    def __init__(self):
        self.buf = Buffer()

        self.dictionary = bytearray(1024)
        self.dict_pos = 0

    @staticmethod
    def __window(x):
        return x & 0x3FF

    def increment_dict_pos(self, inc):
        self.dict_pos = self.__window(self.dict_pos + inc)

    def decompress(self, data):
        output = bytearray()

        for compressed, x in self.buf.decode(data):
            if compressed:
                offset, length = x
                for c in range(length):
                    temp = self.dictionary[self.__window(offset + c)]
                    self.dictionary[self.dict_pos] = temp
                    self.increment_dict_pos(1)
                    output.append(temp)
            else:
                # uncompressed
                self.dictionary[self.dict_pos] = x
                self.increment_dict_pos(1)
                output.append(x)

        return output
