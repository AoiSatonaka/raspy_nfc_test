import nfc
from commands.exec_command import exec_command

# constant
MF_EF01_SELECT_COMMAND = bytearray(
    [0x00, 0xA4, 0x02, 0x0C, 0x02, 0x2F, 0x01]
)


def select_mf_ef01(tag: nfc.tag.Tag):
    (_, status) = exec_command(tag, MF_EF01_SELECT_COMMAND)

    return status.is_success
