import struct
from enum import Enum

from vbftool.checksum import crc16, crc32


def writeline(fp, s):
    fp.write(b'%s\r\n' % s.encode('utf-8'))


def newline(fp):
    fp.write(b'\r\n')


class VbfVersion(Enum):
    VERSION_2_2 = '2.2'
    VERSION_2_3 = '2.3'
    VERSION_2_4 = '2.4'
    VERSION_2_5 = '2.5'
    VERSION_3_0 = '3.0'
    VERSION_JLR3_0 = 'JLR3.0'


class Network(Enum):
    CAN_HS = 'CAN_HS'  # main network @ 500 kbit/s
    CAN_MS = 'CAN_MS'  # main network @ 125 kbit/s
    FLEXRAY = 'FLEXRAY'  # Main network
    DOIP = 'DOIP'  # Main network
    SUB_MOST = 'SUB_MOST'  # MOST sub network connected to a gateway
    SUB_CAN1 = 'SUB_CAN1'  # CAN sub network connected to a gateway
    SUB_CAN2 = 'SUB_CAN2'  # CAN sub network connected to a gateway
    SUB_LIN1 = 'SUB_LIN1'  # LIN sub network connected to a gateway
    SUB_LIN2 = 'SUB_LIN2'  # LIN sub network connected to a gateway
    SUB_OTHER = 'SUB_OTHER'  # Other sub network connected to a gateway


class FrameFormat(Enum):
    # standard frame format, 11-bit CAN identifiers
    CAN_STANDARD = 'CAN_STANDARD'
    # extended frame format, 29-bit CAN identifiers
    CAN_EXTENDED = 'CAN_EXTENDED'
    # 16 bit DoIP logical address or 16 bit FlexRay logical address
    LOGICAL_ADDRESS = '16BIT_STANDARD'


class SwPartType(Enum):
    CARCFG = 'CARCFG'  # Car configuration
    CUSTOM = 'CUSTOM'  # Customer parameters
    DATA = 'DATA'  # Data or parameters (i.e., calibrations)
    EXE = 'EXE'  # Executable (i.e., strategy)
    GBL = 'GBL'  # Gateway Bootloader
    SBL = 'SBL'  # Secondary Bootloader
    SIGCFG = 'SIGCFG'  # Signal configuration
    TEST = 'TEST'  # Test program, (i.e. production test, diagnostics)


class Vbf:
    def __init__(self, version, start_addr, memory_size, data):
        self.version = version
        self.start_addr = start_addr
        self.length = memory_size
        self.data = data
        self._options = []

    def dump(self, fp):
        data_checksum = crc16(self.data)
        content = struct.pack('>II', self.start_addr, len(self.data))
        content += self.data
        content += struct.pack('>H', data_checksum)
        file_checksum = crc32(content)

        writeline(fp, 'vbf_version = %s;' % self.version.value)
        newline(fp)
        writeline(fp, 'header {')
        newline(fp)

        for option in self._options:
            option.dump(fp)

        writeline(fp, '\t//file checksum')
        writeline(fp, '\t%s = 0x%08x;' % ('file_checksum', file_checksum))
        newline(fp)

        fp.write(b'}')

        fp.write(content)

    def add_option(self, option):
        self._options.append(option)
