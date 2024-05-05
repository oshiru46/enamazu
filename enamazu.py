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
from objects_requirer import *

class Enamazu:
    logger = getLogger(__name__)

    def __init__(self, rbid, rbpass, dev_name, baudrate=115200):
        # HACK: メタプログラミングの機能でvnameを変数から取得できないか？
        require_not_none(rbid, "rbid")
        require_not_empty(rbid, "rbid")
        require_not_none(rbpass, "rbpass")
        require_not_empty(rbpass, "rbpass")
        require_not_none(dev_name, "dev_name")
        require_not_empty(dev_name, "dev_name")
        self.sks = SkstackWrapper(
            rbid=rbid, rbpass=rbpass, dev_name=dev_name, baudrate=baudrate)
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, ex_type, ex_value, trace):
        # HACK: 例外をログ出力するなりしたい
        self.close()
        pass

    def connect(self):
        self.sks.connect()
        pass

    def close(self):
        self.sks.close()
        pass

    def get_measured_instantaneous_electric_energy(self):

        en_frame = Enamazu.construct_en_frame_props_get(
            [SmeterProps.MEASURED_INSTANTANEOUS_ELECTRIC_ENERGY])

        response = self.sks.transmit(en_frame)
        # TODO: parse response
        pass

    @classmethod
    def construct_en_frame_props_get(cls, prop_list, tid=b"\x00\x01", seoj=b"\x05\xFF\x01", deoj=b"\x02\x88\x01"):
        # EHD1: 0x10 -> ECHONET Lite規格
        # EHD2: 0x81 -> 形式1
        # ESV : 0x62 -> プロパティ値読み出し要求(Get)
        esv = b"\x62"
        opc = len(prop_list).to_bytes(1, byteorder='big')
        frame = b"\x10\x81" + tid + seoj + deoj + esv + opc

        for prop in prop_list:
            # PDC: 0x00 -> EDTのバイト数 = 0(Getなのでこちらから送信するデータはなし)
            pdc = b"\x00"
            frame += prop.epc + pdc

        return frame


class SmeterPropsInfo(NamedTuple):
    epc: int


# see https://echonet.jp/wp/wp-content/uploads/pdf/General/Standard/AIF/lvsm/lvsm_aif_ver1.10.pdf
#     ２．３オブジェクト別搭載ECHONET プロパティ（EPC）
# プロパティのGetアクセス可でサポートが必須のプロパティのみ
# 1分積算電力量計測値(正方向、逆方向計測値) (0xD0)についてはGet必須ではあるが、
# 英語版に英訳がなく名称を考えるのが大変なので非サポートにする。
class SmeterProps:
    """設置場所"""
    INSTALLATION_LOCATION = SmeterPropsInfo(b"\x81")
    """規格Version 情報"""
    STANDARD_VERSION_INFORMATION = SmeterPropsInfo(b"\x82")
    """異常発生状態"""
    FAULT_STATUS = SmeterPropsInfo(b"\x88")
    """メーカコード"""
    MANUFACTURER_CODE = SmeterPropsInfo(b"\x8A")
    """製造番号"""
    SERIAL_NO = SmeterPropsInfo(b"\x8D")
    """現在時刻設定"""
    CURRENT_TIME_SETTING = SmeterPropsInfo(b"\x97")
    """現在年月日設定"""
    CURRENT_DATE_SETTING = SmeterPropsInfo(b"\x98")
    """状変アナウンスプロパティマップ"""
    STATUS_CHANGE_ANNOUNCEMENT_PROPERTY_MAP = SmeterPropsInfo(b"\x9D")
    """Set プロパティマップ"""
    SET_PROPERTY_MAP = SmeterPropsInfo(b"\x9E")
    """Get プロパティマップ"""
    GET_PROPERTY_MAP = SmeterPropsInfo(b"\x9F")
    """動作状態"""
    OPERATION_STATUS = SmeterPropsInfo(b"\x80")
    """B ルート識別番号"""
    B_ROUTE_ID = SmeterPropsInfo(b"\xC0")
    """係数"""
    COEFFICIENT = SmeterPropsInfo(b"\xD3")
    """積算電力量有効桁数"""
    NUMBER_OF_EFFECTIVE_DIGITS_FOR_CUMULATIVE_AMOUNT_OF_ELECTRIC_ENERGY = SmeterPropsInfo(
        b"\xD7")
    """積算電力量計測値（正方向計測値）"""
    MEASURED_CUMULATIVE_AMOUNT_OF_ELECTRIC_ENERGY = SmeterPropsInfo(b"\xE0")
    """積算電力量単位（正方向、逆方向計測値）"""
    UNIT_FOR_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY = SmeterPropsInfo(b"\xE1")
    """積算電力量計測値履歴１（正方向計測値）"""
    HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_1 = SmeterPropsInfo(
        b"\xE2")
    # """積算電力量計測値（逆方向計測値）"""
    # MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY = SmeterPropsInfo(b"\xE3")
    # """積算電力量計測値履歴１（逆方向計測値）"""
    # HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_1_ = SmeterPropsInfo(b"\xE4")
    """積算履歴収集日１"""
    DAY_FOR_WHICH_THE_HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_IS_TO_BE_RETRIEVED_1 = SmeterPropsInfo(
        b"\xE5")
    """瞬時電力計測値"""
    MEASURED_INSTANTANEOUS_ELECTRIC_ENERGY = SmeterPropsInfo(b"\xE7")
    """瞬時電流計測値"""
    MEASURED_INSTANTANEOUS_CURRENTS = SmeterPropsInfo(b"\xE8")
    """定時積算電力量計測値（正方向計測値）"""
    CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_MEASURED_AT_FIXED_TIME = SmeterPropsInfo(
        b"\xEA")
    # """定時積算電力量計測値（逆方向計測値）"""
    # CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_MEASURED_AT_FIXED_TIME = SmeterPropsInfo(b"\xEB")
    # """積算電力量計測値履歴２（正方向、逆方向計測値）"""
    # HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_2 = SmeterPropsInfo(b"\xEC")
    # """積算履歴収集日２"""
    # DAY_FOR_WHICH_THE_HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_IS_TO_BE_RETRIEVED_2 = SmeterPropsInfo(b"\xED")
    """積算電力量計測値履歴３（正方向、逆方向計測値）"""
    HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_3 = SmeterPropsInfo(
        b"\xEE")
    """積算履歴収集日３"""
    DAY_FOR_WHICH_THE_HISTORICAL_DATA_OF_MEASURED_CUMULATIVE_AMOUNTS_OF_ELECTRIC_ENERGY_IS_TO_BE_RETRIEVED_3 = SmeterPropsInfo(
        b"\xEF")
