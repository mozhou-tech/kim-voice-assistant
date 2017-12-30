# -*- coding: utf-8-*-
import hashlib
import hmac
import base64


def to_md5_base64(self, strBody):
    hash = hashlib.md5()
    hash.update(self.body)
    m = hash.digest().encode('base64').strip()
    hash = hashlib.md5()
    return hash.digest().encode('base64').strip()


def to_sha1_base64(self, stringToSign, secret):
    hmacsha1 = hmac.new(secret, stringToSign, hashlib.sha1)
    return base64.b64encode(hmacsha1.digest())