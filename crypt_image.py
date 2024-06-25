from __future__ import annotations
from typing import Union
from os import PathLike
import hashlib
from Crypto.Cipher import AES
from PIL import Image


class CryptImage:
    def __init__(self):
        self.image = None
        self.key_hash = None

    @classmethod
    def create_from_path(cls, path: Union[str, PathLike]) -> CryptImage:
        new_crypt_image = CryptImage()
        new_crypt_image.image = Image.open(path)
        return new_crypt_image

    @staticmethod
    def hash_key(key: bytes) -> bytes:
        hash_obj = hashlib.sha256(key)
        new_key = hash_obj.digest()
        hash_obj = hashlib.sha256(new_key)
        return hash_obj.digest()

    @staticmethod
    def image_to_bin(image: Image) -> bytes:
        new_bytes = bytearray()
        new_load = image.load()
        for j in range(image.height):
            for i in range(image.width):
                for h in range(3):
                    new_bytes += new_load[i, j][h].to_bytes(1)
        return bytes(new_bytes)

    @staticmethod
    def bin_to_image(img_bytes: bytes, width: int, height: int) -> Image:
        new_img = Image.new("RGB", (width, height))
        tup_lst = [(img_bytes[i], img_bytes[i + 1], img_bytes[i + 2]) for i in range(0, len(img_bytes), 3)]
        new_img.putdata(tup_lst)
        return new_img

    def encrypt(self, key: str) -> None:

        img_bytes = CryptImage.image_to_bin(self.image)

        cipher = AES.new(key.encode(), AES.MODE_EAX, nonce=b'arazim')
        ciphertext = cipher.encrypt(img_bytes)
        self.image = CryptImage.bin_to_image(ciphertext, self.image.width, self.image.height)
        self.key_hash = CryptImage.hash_key(key.encode())

    def decrypt(self, key: str) -> bool:
        if self.key_hash != CryptImage.hash_key(key.encode()):
            return False

        ciphertext = CryptImage.image_to_bin(self.image)
        cipher = AES.new(key.encode(), AES.MODE_EAX, nonce=b'arazim')
        img_bytes = cipher.decrypt(ciphertext)
        self.image = CryptImage.bin_to_image(img_bytes, self.image.width, self.image.height)
        self.key_hash = None
        return True


"""a = CryptImage.create_from_path("Iran_Pigeon.png")
a.encrypt('wowwwwww' * 2)
a.decrypt('wowwwwww' * 2)"""
"""b = CryptImage.image_to_bin(a.image)
c = CryptImage.bin_to_image(b, a.image.width, a.image.height)"""
