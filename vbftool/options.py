from enum import Enum
from vbftool.vbf import writeline, newline


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
    def __init__(self, name, description, value):
        self._name = name
        self._desc = description
        self._value = value

    def format_value(self, value):
        if isinstance(value, Enum):
            value = value.value
        elif isinstance(value, int):
            value = '0x%x' % value
        elif isinstance(value, str):
            value = '"%s"' % value
        elif isinstance(value, tuple):
            x = [self.format_value(s) for s in value]
            value = '{ %s }' % ', '.join(x)
        elif isinstance(value, list):
            x = [self.format_value(s) for s in value]
            value = '{ %s }' % ', '.join(x)
        return value

    def dump(self, fp):
        writeline(fp, '\t//%s' % self._desc)

        value = self.format_value(self._value)

        writeline(fp, '\t%s = %s;' % (self._name, value))
        newline(fp)


class Description(Option):
    def __init__(self, value):
        super().__init__('description', 'Description', value)


class SwPartNumber(Option):
    def __init__(self, value):
        super().__init__('sw_part_number', 'Software part number', value)


class SwPartNumberDID(Option):
    def __init__(self, value):
        super().__init__('sw_part_number_DID',
                         'DID to read software part number', value)


class SwPartType(Option):
    def __init__(self, value):
        super().__init__('sw_part_type', 'Software part type', value)


class DataFormatIdentifier(Option):
    def __init__(self, value):
        super().__init__('data_format_identifier', 'Format identifier', value)


class Network(Option):
    def __init__(self, value):
        super().__init__('network', 'Network type or list', value)


class EcuAddress(Option):
    def __init__(self, value):
        super().__init__('ecu_address', 'ecu_address or list', value)


class FrameFormat(Option):
    def __init__(self, value):
        super().__init__('frame_format', 'Format frame', value)


class Erase(Option):
    def __init__(self, value):
        super().__init__('erase', 'erase block', value)


class Call(Option):
    def __init__(self, value):
        super().__init__('call', 'call address', value)
