import io

from vbftool.lzss import Decompressor, Compressor, LookAheadBuffer, Dictionary

COMPRESSED_DATA = b'\xa6[\xeeV[l\x82\xd3p\xb9\xdd@(Y-\xf6\xc0\x04\x12\x0b\x9d\xa6\xe9 \xb0\xdbl\xb7Id\x82\xc7o\xb7\\\xec\xb6;\xa0\x19\x0b\xa8\x11\x0b\r\x90\x03\x85\xa6\xe7c\xb4\xdb\xac\xf2\x0b-\xb0\n\x04\xbaAS\xb2\xd9$\x16\xcb\r\x8e\xebs\x90[\xac\xb7\x1b\xad\x94\r\x85\xca\xebt\t`\x02\xc2\xcbg\x03! \xba\xdb\x02hZAxYB\x10]\x81\xb0XB@\xdd\xac!h\x02\x08\xdc\xad\x00x\x02\x01YnV\xfb\x988\n\x85\xc82\x00 \x0bp\x15\x11\x06\x16P\x18\x17[HI\x0b\x80\x02\x0b\xa5\xd01\x00\x10\x1b\x08\x84[M\x90G\x000\x01>\x17!\x16\x00\x14-\xa2h\x04\xa0\x07Q\xb9\x83q\x0f\xa1o\x06\x00\x04\x80\x1d\x88j\x00\x12\x01\x08F0ZA\xc0UD\xd8\\\xc0p\x03P\x05\xe0\t@\x15\x00\xbf\x0b0\xc5\x00b\x16\x91\xac\x16\x11\\\x16\x91\x80b\xbd\x03\xd8Q\x83`X\xc5\x00]\x84\x10\x10\x10\x16\x00,\xc4Y\x00r\x01D\x17Q\x066`h706\x03\xa4.\x00\xf8EH\t\xa1\x1b\xa0\x05\xc0\x89\x81\x1f\x01\xcc\x030E\xa0\xddG\xc0RF\xf8\x10 \xb1\x90\x90\x12"\x04\x04&\x00\x9c\x0b\x90s\x01\x1e\x00\x0c\x04\xa0\n\xc1\xb8\x03@\xb6\x08!\x16\xc0\x11\x84\x9b\x856\xc2\t\x80\x99\x08\xa2\x01\\7;\x99\x1b\x00\xc2r\x00\x8c\x04\xa0@\xe9\x97\xb1"BK\x18|\x05\x10F\x01j\x11N\xc0tI0\x01\x80+\x80U\x04e\x85\x8a\xd0\x0e\x04}\x81W\x03J%\xc4\x07\xf1[\x01\xea\x94q\x1e@Y\xce\xc2E\x80\xbd\x99\xcf\x00D\x05\x10\x03\xdd\x1c\xc7\x01\xe2\x01\x00\xc9\x85\x0c\xe2\x81q\x02\x92\x17\x038\x04DK\xb8\r\x91\x1d\x83oA\xc0\x1e@\xec\x00(\x13\xee\x02T\x8b\x98"\x11,\x02\x82D\xdc\x00\x98\x03\x007[\x11\'\x01\x94\x08\\\x02\xc8XDp\xa3\x01!ce@\xc0\x1eBAh4\xe4\x1f\xc0<\x8c*\x86y\x80d\x82)\x03\xea%\xbc,\xe9P\nI\x8b\x90\xa8\xa6\x11\x08\xc2IA\x02\x81\xb0\x01\x90(\x9c\x12\xa0\x0008\x02\x94\x016\x81\x1e\x00p\x87,Q\xc0(\xc1>\xa4\x08D\xe4\x01\x93\n*\x10\x02P#\xb8\x83\xb9\x0c\x01?\x83P+\x12\x19\xd80\x81\x00\x0b\x92#\x13^D\xd0VJ\x961D@\x8d\xc0\x9a\ns\x0bm\xbcx\x05\xc2\xd0\xa1\x05\x1f\n\xee\x0b\xc1\x19\x12|\x02@\x00H+0\x14\x00\xac\xd13\x02 \x02\x0cH\xec-\xcb\x9c)\xca\xb0\xed\xa9\x0c\x98\xe8\xa1\xe1\xb10\xf1H\xc2\xa0\x15]\x8a\xf8\x05p\x03X\x13\xf0\xafw \x11p\n\xe0]AA\x8bA\xa0\xa4(\xf4\x12\xe8\xb1@O`\x94\xc0Z\x90f\x00\xae\x81xI\\\x15\xa0f\xc0\x03\xc2\xc4PE\x8d\x11=\x02\xc6\xec\x1d\x8b\xd9\x9c\x12\xb5\x1b`\x12\xc0\xe7\xa0\xc0; \x17\x10\x03\xa0W\xf0\x1cT\x02l|\x00\x12\x08_\x10\xd2\x88\xcc_\xe0\ra\x0b\xea\x14Q\xfb\x1aY\n\x0bW\x11\x0c\n\x01\x9c\xd90@Samo\x80/\xc1\xd7\x82h\x17\xce&h\x11\xc0\xd9\xc9\x1060O \x7fE.\x12\xde\x10\x07\x02,S|6\x06;\x83gX\xe4\x03\x90\xd7\x81~\x05\xde\xd6\x83r\'\xe8\x06(=\xc1,\xa0\xa8\x81\xac\x88`\x1bJg\x03x"\x18_k\xa3PI\x00Z\xc9\xf4\x85\xc9\xdb\x02\xe6\x15$C\x86\x01\x8b\xdan\x03\x0c\x0e\xd8\xb70\xb3Y\x94X1p:\x00\xc8\x10\xb6\x15\xbd\xcd\x83\xc7\x06\xfe\x0c\xc1D\xd4\xb3\x15 @\x1e\x80i\x82A\x17j\xaaXFd\x17S$\x00\x81\xc1\x94\x02~\x11z6A\xf4\x07\x84\xd5\xf5\'\x96)\x06k\x84U\x82A\x06ZEq\x96\xc9\x85\x88U\xe2\x13\x82\x88\x98H\xf7\x0b\xbc6\xec&\xcc*\xc3\xf0\x8b\x007\x00\x1cb\x9b\x05l\x19 \x87P+@\nH)`\xb8\x1e\xe1#\xe3v|\x00PA\xbc\x01>\x07!.\xc0F!\x1a)}\xaeT\x00X\n\xb87\xbe\x02\xe8D\x8b\xb5YZ*\xf7Y\xc8\xb0\xc6Ap\x08\xb4\x8e\xb84\x829\xc2{!\x96\x92\xd91\xec\x05\xb8\x01\xfb\x07\x80T`Y\xc4\x1b\x82E\x00\x9c\x14\x10\xbc\x06`\xc3\x10\xa73\'\x823\x81\x19\x80b\x05\x0e\x01P\x90 \x93f.\x8c\xc1\xc1\xe7\x82\xd7\x0bk\x15\x00\xe8\x06\x80*\xa2\xd8N\x08\xb0\xf35 \x9b\xc1$\x93M\x94\x00G\x00U\x10\x8e\xa0\x1d\xa0\x95\x80\x0c2{P&ve,\x03@\x0c\xa8\xab u\xe4\xea\xc4\x13\x05\x89B\x01>T4\x01\xac\x96\xb1\xaa \x1a\xc0\tYp\x83\xbe\x13\xcc!\x04\x1b\xf0!a\'\x04\x8a|\xc7\xa2\x0e\x876J\xf0\x94d\x03\xf5hl\xda\x08\x1d\x18\x89U\xbe\x0b\\\t\xf8\x151\\\xa2\xd9\r\xea\x83\x95\x01\xd2\x06\xc8J\x10\xac\x02G(\xab\x10\xe8Ad@\xaa.\xf0\xd8S\x05\x81@\x80f\x05\x01\x05\xca\xd0\xf8\xc0`\x01\x11\x16\xee\x05\x84laD\x85\x99K\x80\x00'
DATA = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lacus neque, rutrum eget ultricies vitae, varius rhoncus eros. Praesent ante dui, porttitor at ante id, interdum mattis est. Proin sed risus nisi. Ut sollicitudin fringilla mi sed mattis. Fusce venenatis tincidunt felis, a placerat diam facilisis eu. In nec tortor ut arcu pretium pellentesque. Mauris id massa vitae quam consequat facilisis. Duis interdum condimentum nibh. Suspendisse vel lacus ut mauris aliquam auctor. Praesent at mauris lorem. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.\nCras quis magna arcu. Quisque dapibus ornare vehicula. Sed ut iaculis lectus. Etiam sed eros sem. Pellentesque varius viverra nibh eu varius. Morbi euismod pharetra ex, ac posuere eros sagittis non. Nam semper non libero in ornare. Phasellus pharetra venenatis pulvinar. Phasellus egestas sapien est, ultrices facilisis leo lobortis nec. Mauris posuere quam vel justo lobortis consequat. Nulla a lacus sit amet metus varius convallis vitae eget metus.\nAenean ornare leo accumsan urna lacinia gravida. Cras eu convallis dui. Quisque pulvinar augue vitae enim euismod hendrerit. Maecenas dignissim sit amet nunc id cursus. Sed fringilla accumsan ipsum a efficitur. Nam id molestie libero. Maecenas libero ligula, posuere ut fringilla vitae, tempus id dolor. Pellentesque dapibus dolor nisi, non dapibus nibh convallis sed. Duis at quam est. Vestibulum arcu nibh, posuere nec volutpat a, vulputate facilisis risus. Vestibulum sit amet elit sem. Nunc hendrerit venenatis viverra. Nulla facilisi. Sed nulla tellus, vestibulum non nibh id, lacinia auctor ante. Aliquam dui ante, tincidunt eu sem vitae, dapibus porta magna. Ut nec eros luctus, pharetra velit nec, dictum metus.\nAliquam eget feugiat mauris. Morbi tempus neque velit, ac ornare diam suscipit vitae. Nulla facilisi. Duis hendrerit leo nec tincidunt lacinia. Nulla nec urna euismod, elementum leo non, finibus eros. Sed porta vulputate dolor eu porta. Morbi consequat rhoncus lacus cras amet.'


def test_dict():
    d = Dictionary()
    d.append(50)
    assert d[0] == 50


def test_dict_full():
    dct = Dictionary()
    for d in DATA[:1024]:
        dct.append(d)

    for i in range(1024):
        assert dct[i] == DATA[i]


def test_dict_wrap():
    dct = Dictionary()
    for d in DATA[:1025]:
        dct.append(d)

    assert dct[0] == DATA[1024]  # wrapped
    for i in range(1023):
        assert dct[i + 1] == DATA[i + 1]


def test_dict_pos():
    dct = Dictionary()
    for i, d in enumerate(DATA):
        dct.append(d)
        assert dct[i % 1024] == d


def test_dict_data():
    dct = Dictionary()
    for i, d in enumerate(DATA):
        dct.append(d)
        assert dct.data == DATA[max(0, i - 1023):i + 1]


def test_decompress():
    decompressor = Decompressor()
    assert decompressor.decompress(COMPRESSED_DATA) == DATA


def test_decompress_chunked():
    decompressor = Decompressor()

    stream = io.BytesIO(COMPRESSED_DATA)
    out = b''
    for chunk in iter(lambda: stream.read(64), b''):
        out += decompressor.decompress(chunk)

    assert (out == DATA)


def test_lookahead_init_buffer():
    lab = LookAheadBuffer(DATA)
    assert lab.lookahead == DATA[0:17]


def test_lookahead_iter_data():
    lab = LookAheadBuffer(DATA)
    it = lab.iter()
    for x in DATA:
        assert next(it) == x


def test_lookahead_iter_lookaheaed():
    lab = LookAheadBuffer(DATA)
    it = lab.iter()
    for i in range(len(DATA)):
        next(it)
        assert lab.lookahead == DATA[i:i + 17]


def test_lookahead_dict_init():
    lab = LookAheadBuffer(DATA)
    assert lab.dictionary.data == b''

# def test_compress():
#     compressor = Compressor()
#
#     compressed = compressor.compress(DATA)
#
#     l = 15
#     for i, (d, c) in enumerate(zip(compressed[0:l], COMPRESSED_DATA[0:l])):
#         print(i, hex(d), hex(c))
#         assert d == c
#
#     # assert compressed == COMPRESSED_DATA
#
#     decompressor = Decompressor()
#     assert decompressor.decompress(compressed) == DATA
