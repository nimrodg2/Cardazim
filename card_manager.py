from card import Card
from typing import Union
from os import PathLike, mkdir
import os
import json
from crypt_image import CryptImage
from PIL import Image


class CardManager:

    def save(self, card: Card, dir_path: Union[str, PathLike] = '.'):
        path = os.path.join(dir_path, CardManager.generate_identifier(card))
        mkdir(path)

        im_path = os.path.join(path, "image.jpg")
        card.image.image.save(im_path)

        data_dict = card.__dict__.copy()
        data_dict["image"] = im_path

        json_object = json.dumps(data_dict)
        json_file = os.path.join(path, "metadata.json")
        with open(json_file, "w") as f:
            f.write(json_object)

    # this might be weird if some "bad" chars are part of the name or creator
    @staticmethod
    def generate_identifier(card: Card) -> str:
        return card.name + "_" + card.creator + "_S" if card.solution is not None else ""

    @classmethod
    def load(cls, identifier: str) -> Card:
        json_file = os.path.join(identifier, "metadata.json")
        with open(json_file, "r") as f:
            d = json.load(f)
            return Card.create_from_path(*d.values())


b = Card.create_from_path("IRAN", "Nimrod", "Iran.png", "whatever", "whatever")
a = CardManager()
a.save(b)
CardManager.load(CardManager.generate_identifier(b))
