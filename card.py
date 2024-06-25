from __future__ import annotations
from PIL import Image
from typing import Union
from os import PathLike
from crypt_image import CryptImage


class Card:
    def __init__(self, name, creator, image, riddle, solution=None):
        self.name = name
        self.creator = creator
        self.image: CryptImage = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self):
        return "<Card name=" + self.name + ', creator=' + self.creator + ">"

    def __str__(self):
        val = "Card " + self.name + " by " + self.creator + '\n'
        val += "riddle: " + self.riddle + '\n'
        val += "solution: "
        if self.solution is not None:
            val += self.solution
        else:
            val += "unsolved"
        return val

    @classmethod
    def create_from_path(cls, name: str, creator: str, path: Union[str, PathLike], riddle: str, solution: str):
        new_image = CryptImage.create_from_path(path)
        return Card(name, creator, new_image, riddle, solution)

    def serialize(self) -> bytes:
        A = bytes()
        A += (len(self.name)).to_bytes(4, "little")
        A += self.name.encode()
        A += (len(self.creator)).to_bytes(4, "little")
        A += self.creator.encode()
        A += self.image.image.height.to_bytes(4, "little")
        A += self.image.image.width.to_bytes(4, "little")
        A += CryptImage.image_to_bin(self.image)
        A += self.image.key_hash if self.image.key_hash is not None else (0).to_bytes(32, "little")
        A += (len(self.riddle)).to_bytes(4, "little")
        A += self.riddle.encode()
        return A

    @classmethod
    def deserialize(cls, data) -> Card:
        name_len = int.from_bytes(data[:4], "little")
        data = data[4:]
        name = data[:name_len].decode()
        data = data[name_len:]
        creator_len = int.from_bytes(data[:4], "little")
        data = data[4:]
        creator = data[:creator_len].decode()
        data = data[creator_len:]
        img_height = int.from_bytes(data[:4], "little")
        data = data[4:]
        img_width = int.from_bytes(data[:4], "little")
        data = data[4:]
        image = CryptImage.bin_to_image(data[:img_height * img_width * 3], img_width, img_height)
        data = data[img_height * img_width * 3:]
        riddle_len = int.from_bytes(data[:4], "little")
        data = data[4:]
        riddle = data[:riddle_len].decode()
        return Card(name, creator, image, riddle)
