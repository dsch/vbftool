import logging
import struct
from enum import Enum

from vbftool.checksum import crc16, crc32
from vbftool.options import Option
from vbftool.output import writeline, newline

log = logging.getLogger(__name__)


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


class _FileChecksum(Option):
    def __init__(self, value):
        super().__init__('file_checksum', 'file checksum', value, number_format='0x%08x')


class Vbf:
    def __init__(self, version):
        self.version = version
        self._options = []
        self._data = []

    def add_data(self, address, data):
        self._data.append((address, data))
    def dump(self, fp):
        content = bytes()
        crc = 0
        for address, data in self._data:
            block_content = self.create_data_block(address, data)
            crc = crc32(block_content, crc)
            content += block_content
        file_checksum = _FileChecksum(crc)

        writeline(fp, 'vbf_version = %s;' % self.version.value)
        newline(fp)
        writeline(fp, 'header {')
        newline(fp)

        for option in self._options:
            option.dump(fp)

        file_checksum.dump(fp)

        fp.write(b'}')

        fp.write(content)

    @staticmethod
    def create_data_block(start_addr, data):
        data_checksum = crc16(data)  # data checksum is always calculated from uncompressed data
        if 0:  # compression enabled
            data = lzss.encode(bytes(data), 10, 4)
        data_length = len(data)
        log.info("block start address: 0x%08x", start_addr)
        log.info("block length: 0x%08x", data_length)
        log.info("block checksum: 0x%04x", data_checksum)
        content = struct.pack('>II', start_addr, data_length)
        content += data
        content += struct.pack('>H', data_checksum)
        return content

    def add_option(self, option):
        self._options.append(option)
