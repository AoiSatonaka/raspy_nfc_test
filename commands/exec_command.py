from typing import Tuple
from nfc.tag.tt4 import Type4Tag
from commands.status import Status, STATUS_TABLE


def exec_command(
    tag: Type4Tag, command: bytearray, indent=1
) -> Tuple[bytearray, Status]:
    indents = "\t"*indent
    try:
        # TODO: use Type4Tag.send_apdu()
        result: bytearray = tag.transceive(command)

        code1, code2 = (result[-2], result[-1])

        status = STATUS_TABLE[code1][code2]
        print(indents, status.message)

        return result, status

    except Exception as e:
        print(indents, "Error:get_retry_count [Reason]", e)
        return bytearray(), Status(False, e)
