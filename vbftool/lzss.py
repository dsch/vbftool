class Buffer:
    def __init__(self, stream):
        self._stream = stream
        self._use = 0
        self._d = 0

    def fill(self):
        while self._use <= 16:
            nxt = self._stream.read(1)
            if nxt:
                self._d |= (nxt[0] << (24 - 8 - self._use))
                self._use += 8
            else:
                break
        return self._use > 0

    def decode(self):
        self._stream.seek(0)  # rewind the stream
        self._use = 0
        self._d = 0

        while self.fill():
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
                length = ((self._d >> (24 - 15)) & 0xF) + 2
                self._d = (self._d << 15) & 0xFFFFFF
                self._use -= 15
                yield True, (offset, length)


class Decompressor:
    @staticmethod
    def __window(x):
        return x & 0x3FF

    def decompress(self, input, output):
        buf = Buffer(input)

        dictionary = bytearray(2 ** 10)
        dict_pos = 0
        for compressed, x in buf.decode():
            if compressed:
                offset, length = x
                offset -= 1  # offset 0 indicates end of stream
                finding = bytearray(length)
                for c in range(length):
                    dictionary[dict_pos] = dictionary[self.__window(offset + c)]
                    finding[c] = dictionary[dict_pos]
                    dict_pos = self.__window(dict_pos + 1)
            else:
                # uncompressed
                dictionary[dict_pos] = x
                dict_pos = self.__window(dict_pos + 1)
                finding = bytes([x])
            # print(x, finding, '0x%06X' % buf._d, buf._use)
            output.write(finding)