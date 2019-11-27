from collections import deque


class Buffer:
    def __init__(self):
        self._queue = deque()
        self._use = 0
        self._d = 0
        self._eof = False
        self._needs_input = True

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
        self._needs_input = False

        while self.__fill():
            if self._d & 0x800000:
                # uncompressed
                if self._use >= 9:
                    data = (self._d >> (24 - 9)) & 0xFF
                    self._d = (self._d << 9) & 0xFFFFFF
                    self._use -= 9
                    yield False, data
                else:
                    self._needs_input = True
                    break
            else:
                # compressed
                if self._use >= 11:
                    offset = (self._d >> (24 - 11)) & 0x3FF
                    if offset == 0:
                        self._eof = True
                        break
                if self._use >= 15:
                    offset -= 1  # offset is one based
                    length = ((self._d >> (24 - 15)) & 0xF) + 2
                    self._d = (self._d << 15) & 0xFFFFFF
                    self._use -= 15
                    yield True, (offset, length)
                else:
                    self._needs_input = True
                    break

    def _flush_encoded(self):
        output = bytearray()
        while self._use > 7:
            output.append((self._d >> 16) & 0xFF)
            self._d = (self._d << 8) & 0xFFFFFF
            self._use -= 8
        return output

    def encode_uncompressed(self, x):
        self._d |= 0x1 << (24 - 1 - self._use)  # uncompressed
        self._d |= (x & 0xFF) << (24 - 9 - self._use)
        self._use += 9
        return self._flush_encoded()

    def encode_compressed(self, offset, length):
        self._d |= 0x0 << (24 - 1 - self._use)  # compressed
        self._d |= ((offset + 1) & 0x3FF) << (24 - 11 - self._use)  # 10 bits offset
        self._d |= ((length - 2) & 0xF) << (24 - 15 - self._use)  # 4 bits length
        self._use += 15
        return self._flush_encoded()


class Dictionary:
    def __init__(self):
        self.dictionary = bytearray(1024)
        self.__dict_pos = 0
        self.__cnt = 0

    @staticmethod
    def __window(x: int) -> int:
        return x & 0x3FF

    def increment_dict_pos(self, inc: int):
        self.__dict_pos = self.__window(self.__dict_pos + inc)

    def append(self, x):
        self.dictionary[self.__dict_pos] = x
        self.increment_dict_pos(1)
        self.__cnt += 1

    def __getitem__(self, item: int) -> int:
        return self.dictionary[self.__window(item)]

    @property
    def data(self):
        first = bytearray()
        if self.__cnt > 1024:
            first = self.dictionary[self.__dict_pos:]

        if self.__cnt == 1024:
            return self.dictionary

        return first + self.dictionary[0:self.__dict_pos]


class Decompressor:
    def __init__(self):
        self.buf = Buffer()
        self.dictionary = Dictionary()

    def decompress(self, data) -> bytearray:
        output = bytearray()
        with open('decompress.log', 'w') as f:
            for compressed, x in self.buf.decode(data):
                f.write('%s %s\n' % (compressed, x))
                if compressed:
                    offset, length = x
                    for c in range(length):
                        temp = self.dictionary[offset + c]
                        self.dictionary.append(temp)
                        output.append(temp)
                else:
                    # uncompressed
                    self.dictionary.append(x)
                    output.append(x)
        return output


class LookAheadBuffer:
    def __init__(self, data, size=17):
        self.__data = data
        self.__size = size
        self.lookahead = data[0:size]
        self.dictionary = Dictionary()

    def iter(self):
        for nxt in self.__data[self.__size:]:
            current = self.lookahead[0]
            yield current
            self.dictionary.append(current)
            self.lookahead = self.lookahead[1:] + bytes([nxt])

        for current in self.lookahead:
            yield current
            self.dictionary.append(current)
            self.lookahead = self.lookahead[1:]


class Compressor:
    def __init__(self):
        self.buf = Buffer()
        self.dictionary = bytearray()
        self.lookahead = bytearray()

    def xx(self, data):
        # pre-fill lookahead buffer
        self.lookahead = data[0:17]

        for l in data[17:]:
            yield l
            self.dictionary.append(self.lookahead[0])
            self.lookahead = self.lookahead[1:] + bytes([l])

    def compress(self, data: bytearray) -> bytearray:
        output = bytearray()

        with open('compress.log', 'w') as f:

            gen = self.xx(data)
            for l in gen:
                for i in range(17, 1, -1):
                    index = self.dictionary.rfind(self.lookahead[:i])
                    if index >= 0:
                        length = i
                        f.write('%s %s\n' % (True, (index, length)))
                        output += self.buf.encode_compressed(index, length)
                        for _ in range(length - 1):
                            next(gen)
                        break

                if index < 0:
                    f.write('%s %s\n' % (False, self.lookahead[0]))
                    output += self.buf.encode_uncompressed(self.lookahead[0])

        return output
