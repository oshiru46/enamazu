from skstack_wrapper import SkstackWrapper
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

skstack_wrapper = SkstackWrapper(rbid, rbpass, serial_port)
try:
    skstack_wrapper.connect()
    skstack_wrapper.transmit(echonet_packet)
except Exception:
    skstack_wrapper.close()

print("finish")
