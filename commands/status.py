from enum import Enum, auto
from typing import Dict


class __ProcessStatus(Enum):
    COMPLETE = auto()
    ABORT = auto()


__PROCESS_FORMAT = "PROCESS {}"
__PROCESS_STATUS_TABLE: Dict[__ProcessStatus, str] = {
    __ProcessStatus.COMPLETE: __PROCESS_FORMAT.format("Complete"),
    __ProcessStatus.ABORT: __PROCESS_FORMAT.format("Abort"),
}


class __StatusType(Enum):
    SUCCESS = auto()
    WARNING = auto()
    EXECUTE_ERR = auto()
    INSPECT_ERR = auto()


__STATUS_TYPE_FORMAT = "TYPE {}"
__STATUS_TYPE_TABLE: Dict[__StatusType, str] = {
    __StatusType.SUCCESS: __STATUS_TYPE_FORMAT.format("SUCCESS"),
    __StatusType.WARNING: __STATUS_TYPE_FORMAT.format("WARNING"),
    __StatusType.EXECUTE_ERR: __STATUS_TYPE_FORMAT.format("EXECUTION_ERROR"),
    __StatusType.INSPECT_ERR: __STATUS_TYPE_FORMAT.format("INSPECTION_ERROR")
}

__STATUS_FORMAT = "{} > {} > {}"


class Status():
    is_success = False
    message = ""

    def __init__(self, is_success: bool, message: str) -> None:
        self.is_success = is_success
        self.message = message


def __MAKE_STATUS(process: __ProcessStatus):
    def func(status: __StatusType, is_success: bool):
        def func(msg: str) -> Status:
            return Status(is_success, __STATUS_FORMAT.format(
                __PROCESS_STATUS_TABLE[process],
                __STATUS_TYPE_TABLE[status],
                msg
            ))
        return func
    return func


__MAKE_COMPLETE_STATUS = __MAKE_STATUS(__ProcessStatus.COMPLETE)
__MAKE_ABORT_STATUS = __MAKE_STATUS(__ProcessStatus.ABORT)

__MAKE_SUCCESS_STATUS = __MAKE_COMPLETE_STATUS(__StatusType.SUCCESS, True)
__MAKE_WARNING_STATUS = __MAKE_COMPLETE_STATUS(__StatusType.WARNING, False)
__MAKE_EXECUTE_ERR_STATUS = __MAKE_ABORT_STATUS(
    __StatusType.EXECUTE_ERR, False
)
__MAKE_INSPECT_ERR_STATUS = __MAKE_ABORT_STATUS(
    __StatusType.INSPECT_ERR, False
)


STATUS_TABLE: Dict[int, Dict[int, Status]] = {
    0x90: {
        0x00:  __MAKE_SUCCESS_STATUS("Success")
    },
    0x62: {
        0X83:  __MAKE_WARNING_STATUS("Access blocked to DF.")
    },
    0x63: {
        0x00: __MAKE_WARNING_STATUS("Failed Verification"),
        0xC0: __MAKE_WARNING_STATUS(
            "Success getting verification retry count [0]"
        ),
        0xC1: __MAKE_SUCCESS_STATUS(
            "Success getting vefification retry count [1]"
        ),
        0xC2: __MAKE_SUCCESS_STATUS(
            "Success getting verification retry count [2]"
        ),
        0xC3: __MAKE_SUCCESS_STATUS(
            "Success getting verification retry count [3]"
        ),
    },
    0x64: {
        0x00: __MAKE_EXECUTE_ERR_STATUS("Incorrect file control information.")
    },
    0x65: {
        0x81: __MAKE_EXECUTE_ERR_STATUS("Failed writing memory.")
    },
    0x67: {
        0x00: __MAKE_INSPECT_ERR_STATUS("Incorrect Lc/Le.")
    },
    0x68: {
        0x81: __MAKE_INSPECT_ERR_STATUS(
            "Not provide access by number of target logical channel."
        ),
        0x82: __MAKE_INSPECT_ERR_STATUS("Not provide secure messeging.")
    },
    0x69: {
        0x81: __MAKE_INSPECT_ERR_STATUS(
            "Command contradictionaly with file structure."
        ),
        0x82: __MAKE_INSPECT_ERR_STATUS("Security status not fulfilled."),
        0x84: __MAKE_INSPECT_ERR_STATUS("Access blocked to referenced IEF."),
        0x86: __MAKE_INSPECT_ERR_STATUS("Current EF not found."),
    },
    0x6A: {
        0x81: __MAKE_INSPECT_ERR_STATUS("Not provide function."),
        0x82: __MAKE_INSPECT_ERR_STATUS("Access target file not found."),
        0x86: __MAKE_INSPECT_ERR_STATUS("Incorrect value of P1,P2."),
        0x87: __MAKE_INSPECT_ERR_STATUS("Incorrect referenced key setting.")
    },
    0x6B: {
        0x00: __MAKE_INSPECT_ERR_STATUS("Specify offset out of EF range.")
    },
    0x6D: {
        0x00: __MAKE_INSPECT_ERR_STATUS("Not provided INS.")
    },
    0x6E: {
        0x00: __MAKE_INSPECT_ERR_STATUS("Not provided class.")
    },
}
