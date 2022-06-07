#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import nfc
from nfc.tag.tt4 import Type4BTag
from commands.verify.get_retry_count import get_retry_count

# constant
WAIT_SEC = 5


def startup(target):
    print("[onStart]")
    return target


def discoverd(target):
    print("[onDiscover]")
    return True


def connected(tag: nfc.tag.Tag):
    # IDm,PMMなどの情報を出力する
    print("[onConnect]")

    print("\t", tag.type)
    if isinstance(tag, Type4BTag):
        print("\t tag is Type4")

        retry_count = get_retry_count(tag)
        print("\t retry count is", retry_count)

    else:
        print("\terror: tag isn't Type4BTag")
    return True


def released(tag: nfc.tag.Tag):
    print("[onRelease]")


def main():
    # 読み込み時のハンドラを接待して待機する
    clf = nfc.ContactlessFrontend('usb')

    # Read & Write
    rdwr_options = {
        "on-startup": startup,
        "on-discover": discoverd,
        "on-connect": connected,
        "on-release": released,
    }

    while True:
        startTime = time.time()
        def after5s(): return time.time() - startTime > 5
        try:
            tag = clf.connect(
                rdwr=rdwr_options,
                terminate=after5s
            )
            # Ctrl+cを押下した場合に停止させる
            if tag is False:
                print("exit")
                break

            time.sleep(WAIT_SEC)

        except Exception as e:
            print("handled Exception: %s" % e)

    clf.close()


if __name__ == "__main__":
    main()
