from enum import Enum
from vbftool.output import writeline, newline


# Allowed identifiers:
# - vbf_version
# - header
# - description
# - sw_part_number
# - sw_part_number_DID
# - sw_part_type
# - VBF_package_release_number
# - data_format_identifier (optional)
# - network
# - ecu_address
# - frame_format
# - erase (optional)
# - omit (optional)
# - call (mandatory only for SBL, GBL, TEST)
# - file_checksum


class Option:
    def __init__(self, name, description, value, number_format='0x%x'):
        self._name = name
        self._desc = description
        self._value = value
        self._number_format = number_format

    def _format_value(self, value):
        if isinstance(value, Enum):
            value = value.value
        elif isinstance(value, int):
            value = self._number_format % value
        elif isinstance(value, str):
            value = '"%s"' % value
        elif isinstance(value, tuple):
            x = [self._format_value(s) for s in value]
            value = '{ %s }' % ', '.join(x)
        elif isinstance(value, list):
            x = [self._format_value(s) for s in value]
            value = '{ %s }' % ', '.join(x)
        return value

    def dump(self, fp):
        writeline(fp, '\t// %s' % self._desc)

        value = self._format_value(self._value)

        writeline(fp, '\t%s = %s;' % (self._name, value))
        newline(fp)


class Description(Option):
    def __init__(self, value):
        if not isinstance(value, list):
            value = [value]
        super().__init__('description', 'Description', value)


class SwPartNumber(Option):
    def __init__(self, value):
        super().__init__('sw_part_number', 'Software part number', value)


class SwPartNumberDID(Option):
    def __init__(self, value):
        super().__init__('sw_part_number_DID',
                         'DID to read software part number', value, number_format='0x%04X')


class SwPartType(Option):
    def __init__(self, value):
        super().__init__('sw_part_type', 'Software part type', value)


class DataFormatIdentifier(Option):
    def __init__(self, compression_method, encryption_method):
        super().__init__('data_format_identifier', 'Format identifier', compression_method << 4 | encryption_method,
                         number_format='0x%02x')


class Network(Option):
    def __init__(self, value):
        super().__init__('network', 'Network type or list', value)


class EcuAddress(Option):
    def __init__(self, value):
        super().__init__('ecu_address', 'ECU address or list', value)


class FrameFormat(Option):
    def __init__(self, value):
        super().__init__('frame_format', 'Format frame', value)


class Erase(Option):
    def __init__(self, value):
        super().__init__('erase', 'Erase block', value)


class Call(Option):
    def __init__(self, value):
        super().__init__('call', 'Call address', value)
