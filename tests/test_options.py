from io import BytesIO

import vbftool.options as opts
from vbftool import SwPartType, Network, FrameFormat


def assert_desc(desc, expected):
    with BytesIO() as fp:
        desc.dump(fp)
        fp.seek(0)
        assert fp.read() == expected


def test_description_single_line():
    desc = opts.Description('description')
    assert_desc(desc, b'\t// Description\r\n'
                      b'\tdescription = {"description"};\r\n'
                      b'\r\n')


def test_description_multi_line():
    desc = opts.Description(['description1', 'description2'])
    assert_desc(desc, b'\t// Description\r\n'
                      b'\tdescription = {"description1", "description2"};\r\n'
                      b'\r\n')


def test_sw_part_number_wers_or_eniva():
    desc = opts.SwPartNumber('WERS number')
    assert_desc(desc, b'\t// Software part number\r\n'
                      b'\tsw_part_number = "WERS number";\r\n'
                      b'\r\n')


def test_sw_part_number_wers_and_eniva():
    desc = opts.SwPartNumber(['WERS number', "ENOVIA number"])
    assert_desc(desc, b'\t// Software part number\r\n'
                      b'\tsw_part_number = {"WERS number", "ENOVIA number"};\r\n'
                      b'\r\n')


def test_sw_part_number_DID():
    desc = opts.SwPartNumberDID(0xF188)
    assert_desc(desc, b'\t// DID to read software part number\r\n'
                      b'\tsw_part_number_DID = 0xF188;\r\n'
                      b'\r\n')


def test_sw_part_type():
    desc = opts.SwPartType(SwPartType.EXE)
    assert_desc(desc, b'\t// Software part type\r\n'
                      b'\tsw_part_type = EXE;\r\n'
                      b'\r\n')


def test_data_format_identifier_none():
    desc = opts.DataFormatIdentifier(0, 0)
    assert_desc(desc, b'\t// Format identifier\r\n'
                      b'\tdata_format_identifier = 0x00;\r\n'
                      b'\r\n')


def test_data_format_identifier_compressed():
    desc = opts.DataFormatIdentifier(1, 0)
    assert_desc(desc, b'\t// Format identifier\r\n'
                      b'\tdata_format_identifier = 0x10;\r\n'
                      b'\r\n')


def test_network_single():
    desc = opts.Network(Network.CAN_HS)
    assert_desc(desc, b'\t// Network type or list\r\n'
                      b'\tnetwork = CAN_HS;\r\n'
                      b'\r\n')


def test_network_subnet():
    desc = opts.Network([Network.CAN_HS, Network.SUB_CAN1])
    assert_desc(desc, b'\t// Network type or list\r\n'
                      b'\tnetwork = {CAN_HS, SUB_CAN1};\r\n'
                      b'\r\n')


def test_ecu_address_single():
    desc = opts.EcuAddress(0x723)
    assert_desc(desc, b'\t// ECU address or list\r\n'
                      b'\tecu_address = 0x723;\r\n'
                      b'\r\n')


def test_ecu_address_subnet():
    desc = opts.EcuAddress([0x723, 0x740])
    assert_desc(desc, b'\t// ECU address or list\r\n'
                      b'\tecu_address = {0x723, 0x740};\r\n'
                      b'\r\n')


def test_frame_format():
    desc = opts.FrameFormat(FrameFormat.CAN_STANDARD)
    assert_desc(desc, b'\t// Format frame\r\n'
                      b'\tframe_format = CAN_STANDARD;\r\n'
                      b'\r\n')


def test_erase_single_block():
    desc = opts.Erase([(0x10000, 0x20000)])
    assert_desc(desc, b'\t// Erase block\r\n'
                      b'\terase = {{0x10000, 0x20000}};\r\n'
                      b'\r\n')


def test_erase_multi_block():
    desc = opts.Erase([(0x10000, 0x20000), (0x50000, 0x1000)])
    assert_desc(desc, b'\t// Erase block\r\n'
                      b'\terase = {{0x10000, 0x20000}, {0x50000, 0x1000}};\r\n'
                      b'\r\n')


def test_call():
    desc = opts.Call(0x10000)
    assert_desc(desc, b'\t// Call address\r\n'
                      b'\tcall = 0x10000;\r\n'
                      b'\r\n')
