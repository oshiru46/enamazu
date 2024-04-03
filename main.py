from enamazu import Enamazu
import os

# Bルート認証ID
rbid = os.environ.get('ENAMAZU_RBID')
# Bルート認証パスワード
rbpass = os.environ.get('ENAMAZU_RBPASS')
# シリアルポート
serial_port = os.environ.get('ENAMAZU_SERIAL_PORT')


echonet_packet = b""
echonet_packet += b"\x10\x81"     # EHD
echonet_packet += b"\x00\x01"     # TID: 仮で1
echonet_packet += b"\x05\xFF\x01"  # SEOJ
echonet_packet += b"\x02\x88\x01"  # DEOJ
echonet_packet += b"\x62"         # ESV
echonet_packet += b"\x01"         # OPC
echonet_packet += b"\xE7"         # EPC
echonet_packet += b"\x00"         # PDC

try:
    with Enamazu(rbid, rbpass, serial_port) as namazu:
        namazu.get_measured_instantaneous_electric_energy()
except Exception as e:
    print(e)
    pass

print("finish")
