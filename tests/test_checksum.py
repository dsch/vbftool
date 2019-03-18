from vbftool.checksum import crc16, crc32
from struct import pack
from pytest import mark


@mark.parametrize("data,expected", [
    ('00 00 00 00', 0x84C0),
    ('F2 01 83', 0xD374),
    ('0F AA 00 55', 0x2023),
    ('00 FF 55 11', 0xB8F9),
    ('33 22 55 AA BB CC DD EE FF', 0xF53F),
    ('92 6B 55', 0x0745),
    ('FF FF FF FF', 0x1D0F),
    ('31 32 33 34 35 36 37 38 39', 0x29B1),  # check
    ('31 32 33 34 35 36 37 38 39 29 b1', 0x0000),  # magic
])
def test_crc16(data, expected):
    assert crc16(bytes.fromhex(data)) == expected


@mark.parametrize("data,expected", [
    (bytes.fromhex('00 00 00 00'), 0x2144DF1C),
    (bytes.fromhex('F2 01 83'), 0x24AB9D77),
    (bytes.fromhex('0F AA 00 55'), 0xB6C9B287),
    (bytes.fromhex('00 FF 55 11'), 0x32A06212),
    (bytes.fromhex('33 22 55 AA BB CC DD EE FF'), 0xB0AE863D),
    (bytes.fromhex('92 6B 55'), 0x9CDEA29B),
    (bytes.fromhex('FF FF FF FF'), 0xffffffff),
    (b'123456789', 0xCBF43926),  # check
    (b'123456789' + pack('<I', 0xCBF43926), 0xDEBB20E3 ^ 0xFFFFFFFF),  # magic
])
def test_crc32(data, expected):
    assert crc32(data) == expected
