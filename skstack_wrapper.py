import serial
from logger import getLogger


class SkstackWrapper:
    logger = getLogger(__name__)

    def __init__(self, rbid, rbpass, dev_name, baudrate=115200):
        type(self).logger.debug("initializing")
        self.serial = serial.Serial(dev_name, baudrate)

        # 一応ログにバージョンを残しておく目的。
        # しばらく放置しているとスリープ状態に入るからかecho backでなく
        # 0x000Aが返ることがあるため、リトライする
        self.send_skver(retry_count=1)

        self.send_skreset()
        # rbid, rbpassを持ちたくないのでここでセットする
        self.send_sksetrbid(rbid, retry_count=1)
        self.send_sksetpwd(rbpass)

        # Rubyの`defined?`相当のことのやり方が分からなかったので、適当な値で初期化
        self.ipv6_addr = ""

        pass

    # 1. serial.write
    # 2. check echo back
    # 3. get response, return it
    # retry_count: 0: none
    def send_bytes(self, bdata, retry_count=0, hides_data=False, checks_echoback=True):
        if not bdata.endswith(b"\r\n"):
            type(self).logger.warn("Detected lack of \\r\\n. appending.")
            bdata += b"\r\n"
        if hides_data:
            type(self).logger.debug("writing data: ********")
        else:
            type(self).logger.debug(
                f"writing data: {bdata.hex()} (in hex), {self.try_decode(bdata)}")
        for attempted in range(retry_count + 1):
            self.serial.write(bdata)
            echoback = self.serial.readline()

            # HACK: echobackのチェックなしのとき、リトライ制御をしない仕様で本当にいいのか？
            if not checks_echoback:
                type(self).logger.debug("skipping to check echoback.")
                break
            # bytearrayでの比較が可能かぱっとわからなかったのでhex文字列で比較する
            if bdata.hex() == echoback.hex():
                type(self).logger.debug(
                    "received correct echo back. receiving response")
                break
            elif bytearray(filter(lambda x: x >= 0x20 or x == 0x0d or x == 0x0a, bdata)).hex() == echoback.hex():
                # 制御文字(のうち少なくとも0x10以下)部分はなぜか受信できていなさそうなので、削ったものと比較する。
                # ただし最後の改行文字は削らない。
                type(self).logger.debug(
                    "received (almost) correct echo back. receiving response")
                break

            if hides_data:
                message = "unexpected echo back. expected ********, but was ********"
            else:
                message = f"unexpected echo back. expected {bdata.hex()}, but was {echoback.hex()} (in hex)."
            if attempted >= retry_count:  # retry count over
                type(self).logger.error(message)
                raise Exception(message)
            else:
                type(self).logger.warn(f"{message} Retrying...")
                continue

        response = self.serial.readline()
        type(self).logger.debug(
            f"received response: {response.hex()} (in hex), {self.try_decode(response)} (decoded)")

        return response

    def send_bytes_then_ok(self, bdata, retry_count=0, hides_data=False):
        response = self.send_bytes(bdata, retry_count, hides_data)
        # HACK: "OK"の前後に改行があっても許すようにしたい
        expected = "OK\r\n".encode()
        if response.hex() != expected.hex():
            message = f"unexpected response. expected OK({expected.hex()} in hex, but was {response.hex()})"
            type(self).logger.error(message)
            raise Exception(message)

        type(self).logger.debug("OK!")
        pass

    def receive_bytes(self):
        response = self.serial.readline()
        type(self).logger.debug(
            f"received response: {response.hex()} (in hex), {self.try_decode(response)} (decoded)")

        return response

    def try_decode(self, bytes, trims=True):
        try:
            if trims:
                return bytes.decode().rstrip('\r\n')
            else:
                return bytes.decode()
        except Exception:
            return "(could not decode)"

    def send_sksetrbid(self, rbid, retry_count=0):
        type(self).logger.debug("[SKSETRBID] Setting Route-B ID")
        self.send_bytes_then_ok(
            f"SKSETRBID {rbid}\r\n".encode(), retry_count, True)
        pass

    def send_sksetpwd(self, password, retry_count=0):
        type(self).logger.debug("[SKSETPWD] Setting Password")
        self.send_bytes_then_ok(
            f"SKSETPWD C {password}\r\n".encode(), retry_count, True)
        pass

    def send_skver(self, retry_count=0):
        type(self).logger.debug("[SKVER] getting SKVER")
        ever = self.send_bytes("SKVER\r\n".encode(),
                               retry_count=retry_count).decode().strip()
        # response:
        # EVER {version}<CR><LF>
        # OK<CR><LF>
        if not ever.startswith("EVER "):
            message = f"[SKVER] Unexpected response. Expected EVER event, but was {ever}"
            type(self).logger.error(message)
            raise Exception(message)
        version = ever[5:]
        type(self).logger.info(f"[SKVER] SKVER -> {version}")

        ok = self.serial.readline().decode().strip()
        if ok != "OK":
            message = f"[SKVER] Unexpected response. Expected OK, but was {ok}"
            type(self).logger.error(message)
            raise Exception(message)
        type(self).logger.debug("[SKVER] Received OK")

        return version

    def send_skreset(self):
        # echobackで直前に送信した"SKVER\r\n"が返ってくることもあった。謎
        self.send_bytes_then_ok("SKRESET\r\n".encode())
        pass

    # mode:
    # - 0: EDスキャン
    # - 2: アクティブスキャン(IEあり)
    # - 3: アクティブスキャン(IEなし)
    # channel_mask:
    # duration:
    def send_skscan(self, mode=2, channel_mask="FFFFFFFF", duration=7):
        data_str = f"SKSCAN {mode} {channel_mask} {duration}"
        type(self).logger.debug(f"[SKSCAN] {data_str}")
        self.send_bytes_then_ok(f"{data_str}\r\n".encode())

        # 起きるかわからないが一応の無限ループ対策
        max_lines = 100
        dict = {}
        for i in range(max_lines):
            response = self.receive_bytes()
            # SKSCANのレスポンスでASCII以外が含まれていることはないかもしれないが一応変数を分ける
            response_str = self.try_decode(response)

            if response_str.startswith("EVENT 22"):
                type(self).logger.debug(
                    "[SKSCAN] Detected SKSCAN finish symbol(EVENT 22).")
                break
            elif response_str.startswith("  "):
                # 先頭がスペース2個の場合はkey:valueでデータが送られてくる
                # 行儀よく処理するならおそらく、"EPANDESC"を受信した次の行から送られるkey:valueを処理する、となる
                knv = response_str.strip().split(':')
                type(self).logger.debug(
                    f"[SKSCAN] Received. Key: {knv[0]}, Value: {knv[1]}")
                dict[knv[0]] = knv[1]
            else:
                type(self).logger.debug(
                    f"[SKSCAN] Skipping unknown response: {response_str}")
        else:  # breakで抜けなかった場合はelseに行くらしい
            message = "[SKSCAN] Read line over. Could not find finish symbol(EVENT 22)"
            type(self).logger.error(message)
            raise Exception(message)

        return dict

    # 仮想レジスタの内容を(表示・)設定する
    def send_sksreg(self, register, value):
        self.send_bytes_then_ok(f"SKSREG {register} {value}\r\n".encode())
        pass

    def send_skll64(self, mac_addr):
        response = self.send_bytes(f"SKLL64 {mac_addr}\r\n".encode())
        ipv6_addr = response.decode().strip('\r\n')

        return ipv6_addr

    def send_skjoin(self, ipv6_addr):
        self.send_bytes_then_ok(f"SKJOIN {ipv6_addr}\r\n".encode())
        pass

    def send_sksendto(self, ipv6_addr, data, port="0E1A", sec="1"):
        # \r\nOK\r\nっぽい。これでいけないかも？
        header = "SKSENDTO 1 {0} {1} {2} {3:04X} ".format(
            ipv6_addr, port, sec, len(data))
        type(self).logger.debug(f"[SKSENDTO] Header: {header}")
        command = header.encode() + data
        # echobackにはECHONET Lite payload部がすっぽりないデータが返ってくる
        # ("SKSENDTO 1 (略) 000E \r\n")
        # echobackをチェックするメリットを把握していないが、雑にノーチェックにする
        # EVENT 21(UDP送信完了)
        event21_res = self.send_bytes(command, checks_echoback=False)
        if not self.try_decode(event21_res).startswith("EVENT 21"):
            message = "[SKSENDTO] UDP send failure because could not receive EVENT 21."
            type(self).logger.error(message)
            raise Exception(message)
        echonet_res_data = self.wait_erxudp()
        return echonet_res_data

    def wait_erxudp(self):
        type(self).logger.debug("Waiting for receiving ERXUDP...")
        # 起きるかわからないが一応の無限ループ対策
        max_lines = 10
        for i in range(max_lines):
            response = self.receive_bytes()
            response_str = self.try_decode(response)

            if response_str.startswith("ERXUDP"):
                # HACK: 送信先・元もチェックした方がよさそうな気もする
                type(self).logger.debug(
                    "Succeeded to receive UDP response. Recieved ERXUDP.")
                udp_response = response_str.strip().split(' ')[8]
                return udp_response
            else:
                type(self).logger.debug("Skipping response. It's not ERXUDP.")
                continue
        else:
            message = f"Read {max_lines} lines, but could not receive ERXUDP."
            type(self).logger.error(message)
            raise Exception(message)

    def wait_skjoined(self):
        # 起きるかわからないが一応の無限ループ対策
        max_lines = 100
        for i in range(max_lines):
            response = self.receive_bytes()
            response_str = self.try_decode(response)

            if response_str.startswith("EVENT 24"):
                message = "Failed to join because EVENT 24 received."
                type(self).logger.error(message)
                raise Exception(message)
            elif response_str.startswith("EVENT 25"):
                type(self).logger.debug(
                    "Succeeded to join. Received EVENT 25.")
                return
            else:
                type(self).logger.debug(
                    f"Skipping unknown response: {response_str}")
        else:
            message = "Seems to fail joining. Could not Receive neither EVENT 24 nor 25."
            type(self).logger.error(message)
            raise Exception(message)

        pass

    # auto closableみたいなことがPythonでできるならそれに対応したいな
    def connect(self):
        type(self).logger.debug("connecting...")
        scan_dict = self.send_skscan()
        # これ、Channelだけじゃなくてここで参照するものを一通りチェックすべきではあるな
        if "Channel" not in scan_dict:
            message = "Could not detect logical Channel number from SKSCAN"
            type(self).logger.error(message)
            raise Exception(message)
        type(self).logger.debug(
            "Setting logical channel number into register(S2)")
        self.send_sksreg("S2", scan_dict["Channel"])
        type(self).logger.debug("Setting Pan ID into register(S3)")
        self.send_sksreg("S3", scan_dict["Pan ID"])

        # MACアドレス(64bit)をIPv6リンクローカルアドレスに変換するらしい
        ipv6_addr = self.send_skll64(scan_dict["Addr"])
        # PANA接続シーケンスを開始するらしい
        self.send_skjoin(ipv6_addr)
        self.wait_skjoined()

        self.ipv6_addr = ipv6_addr

    def close(self):
        type(self).logger.debug("closing...")
        self.serial.close()
        type(self).logger.debug("closed")

    # ECHONET Liteコマンドを送る
    # data: ECHONET Liteフレーム
    def transmit(self, data):
        type(self).logger.debug("transmitting...........")

        # HACK: ipv6_addrの設定有無をもって接続状態を見るのがかっこ悪い
        if self.ipv6_addr == "":
            raise Exception("call connect first.")

        return self.send_sksendto(self.ipv6_addr, data)
