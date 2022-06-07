import nfc
from commands.exec_command import exec_command

# constant
_RETRY_COUNT_VERIFY_COMMAND = bytearray(
    [0x00, 0x20, 0x00, 0x81]
)
_RETRY_COUNT_VERIFY_MASK = ~0xC0


def get_retry_count(tag: nfc.tag.Tag):
    (result, status) = exec_command(tag, _RETRY_COUNT_VERIFY_COMMAND)

    if(not status.is_success):
        return 0

    retry_count: int = result[1] & _RETRY_COUNT_VERIFY_MASK
    return retry_count
