# 　　　　　　　　　　　　　鯰鯰　　　　　　鯰鯰鯰
# 　　　　　　　　　　　　鯰鯰　　　　　鯰鯰鯰　鯰鯰
# 　　　　　　　　　　　　鯰鯰　　　　鯰鯰　鯰　鯰鯰鯰
# 　　　　　鯰鯰鯰　　　鯰鯰鯰鯰鯰　　鯰鯰鯰　鯰　鯰鯰
# 　　　　鯰鯰鯰　　　　　　鯰鯰　　鯰　　鯰鯰鯰鯰　鯰鯰
# 　　　　鯰鯰　　　　　　　鯰鯰　鯰鯰鯰　　　　　鯰鯰鯰鯰鯰
# 　　　鯰鯰鯰鯰　　　　　鯰鯰　　　　鯰鯰鯰鯰鯰　鯰　　　　鯰
# 　　　　　鯰鯰　　　　　　　　　　　　　　　　鯰鯰鯰　　　　鯰鯰
# 　　　　　鯰　　　　　　　　　　　　　　　　　　　　鯰　　　　鯰鯰
# 　　　　鯰鯰　　　鯰鯰鯰鯰鯰鯰鯰鯰鯰　　　　　　　　　鯰　　　　鯰鯰
# 　　鯰　　　　鯰鯰鯰　　　　　　　鯰鯰鯰　　　　　　　鯰　　　　　鯰
# 　鯰鯰　　鯰鯰鯰　　　　　　　　　　　鯰鯰　　　　　鯰鯰　　　　　鯰鯰
# 　鯰　　　鯰　　　　　　　　　　　　　　鯰鯰　　鯰鯰鯰　　　　　　　鯰
# 　鯰鯰鯰鯰鯰　鯰鯰鯰鯰鯰　　　　鯰鯰鯰鯰鯰鯰鯰鯰鯰　　　　　　　　　鯰鯰
# 　　　鯰鯰　　鯰　鯰　　鯰　　鯰　　鯰　鯰　　　　　　　　　　　　　　鯰
# 　　鯰鯰鯰　　鯰　鯰鯰　鯰　　鯰鯰鯰鯰　鯰　　　　　　　　　　　　　　鯰
# 　　鯰　鯰　　　鯰鯰鯰鯰　　　　鯰鯰鯰鯰　　　　　　　　　　鯰　　　　鯰
# 　鯰　　鯰鯰　　　　　　　　　　　　　　　　　　　　　　　鯰　　　　鯰鯰
# 　鯰　　　鯰鯰鯰鯰　　　　　　　　　鯰鯰鯰鯰鯰　　　　　鯰鯰　　　　鯰
# 　鯰　　　　　　　　　鯰鯰鯰鯰鯰　　鯰　　　鯰鯰　　　　鯰　　　　鯰鯰
# 　鯰　　　　　　　　鯰　　　　　鯰　　　　　　　鯰鯰鯰鯰　　　鯰鯰鯰
# 　鯰　　　　　　　鯰　　鯰鯰鯰鯰　鯰　　　　　　　　　　　　鯰鯰
# 　　鯰鯰　　　　　鯰鯰鯰　　　鯰　鯰　　　　　　　　　　　鯰鯰
# 　　　鯰鯰鯰　　　　鯰鯰鯰鯰鯰鯰鯰　　　　　鯰鯰鯰鯰鯰鯰鯰
# 　　　　　鯰鯰鯰鯰鯰鯰鯰鯰鯰鯰鯰鯰鯰鯰鯰鯰鯰

from logger import getLogger
from skstack_wrapper import SkstackWrapper
from typing import NamedTuple


class Enamazu:
    logger = getLogger(__name__)

    def __init__(self, rbid, rbpass, dev_name, baudrate):
        self.sks = SkstackWrapper(
            rbid=rbid, rbpass=rbpass, dev_name=dev_name, baudrate=baudrate)
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self):
        self.connect
        pass

    def connect(self):
        self.sks.connect()
        pass

    def close(self):
        self.sks.close()
        pass


class SmeterPropsInfo(NamedTuple):
    epc: int


# プロパティのGetアクセス可でサポートが必須のプロパティのみ
class SmeterProps:
    INSTALLATION_LOCATION = SmeterPropsInfo(b"\x81")
    STANDARD_VERSION_INFORMATION = SmeterPropsInfo(b"\x82")
    FAULT_STATUS = SmeterPropsInfo(b"\x88")
    MANUFACTURER_CODE = SmeterPropsInfo(b"\x8A")
    SERIAL_NO = SmeterPropsInfo(b"\x8D")
    CURRENT_TIME_SETTING = SmeterPropsInfo(b"\x97")
    CURRENT_DATE_SETTING = SmeterPropsInfo(b"\x98")
    STATUS_CHANGE_ANNOUNCEMENT_PROPERTY_MAP = SmeterPropsInfo(b"\x9D")
    SET_PROPERTY_MAP = SmeterPropsInfo(b"\x9E")
    GET_PROPERTY_MAP = SmeterPropsInfo(b"\x9F")
    OPERATION_STATUS = SmeterPropsInfo(b"\x80")
    COEFFICIENT = SmeterPropsInfo(b"\xD3")
    NUMBER_OF_EFFECTIVE_DIGITS_FOR_CUMULATIVE_AMOUNT_OF_ELECTRIC_ENERGY = SmeterPropsInfo(
        b"\xD7")
    MEASURED_CUMULATIVE_AMOUNT_OF_ELECTRIC_ENERGY = SmeterPropsInfo(b"\xE0")
    UNIT_FOR_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY = SmeterPropsInfo(b"\xE1")
    HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_1 = SmeterPropsInfo(
        b"\xE2")
    # MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY = SmeterPropsInfo(b"\xE3")
    # HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_1_ = SmeterPropsInfo(b"\xE4")
    DAY_FOR_WHICH_THE_HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_IS_TO_BE_RETRIEVED_1 = SmeterPropsInfo(
        b"\xE5")
    MEASURED_INSTANTANEOUS_ELECTRIC_ENERGY_ = SmeterPropsInfo(b"\xE7")
    MEASURED_INSTANTANEOUS_CURRENTS = SmeterPropsInfo(b"\xE8")
    CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_MEASURED_AT_FIXED_TIME = SmeterPropsInfo(
        b"\xEA")
    # CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_MEASURED_AT_FIXED_TIME = SmeterPropsInfo(b"\xEB")
    # HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_2 = SmeterPropsInfo(b"\xEC")
    # DAY_FOR_WHICH_THE_HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_IS_TO_BE_RETRIEVED_2 = SmeterPropsInfo(b"\xED")
