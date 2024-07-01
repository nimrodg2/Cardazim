from card import Card
from typing import Union
from os import PathLike, mkdir
import os
import json

from abc import ABC

import sqlite3


class CardDriver(ABC):
    def __init__(self):
        ...

    def save(self, card: Card):
        ...

    def load(self, identifier):
        ...

    def GetCreators(self):
        ...

    def GetCreatorCards(self, creator: str):
        ...


class FilesystemManager(CardDriver):
    def save(self, card: Card, dir_path: Union[str, PathLike] = '.'):
        path = os.path.join(dir_path, FilesystemManager.generate_identifier(card))
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


class DatabaseManager(CardDriver):
    def __init__(self, name: str = "DATABASE"):
        self.name = name
        self.con = sqlite3.connect(self.name)
        self.cursor = self.con.cursor()
        self.table = "CREATE TABLE DATABASE(NAME VARCHAR(255), CREATOR VARCHAR(255)), IMG_PATH VARCHAR(255), RIDDLE VARCHAR(255), SOLUTION VARCHAR(255)"
        self.cursor.execute(self.table)

    def save(self, card: Card):
        self.cursor.execute("INSERT INTO" + self.name + "(NAME, CREATOR, IMG_PATH, RIDDLE, SOLUTION) VALUES " + str((card.name, card.creator, card.path, card.riddle, card.solution)))
        self.con.commit()

    def load(self, identifier):
        identifier = identifier[:-2]
        A = identifier.split("_")
        self.cursor.execute("SELECT * FROM " + self.name + "WHERE NAME = " + A[0] + " AND CREATOR = " + A[1])
        output = self.cursor.fetchone()
        return Card.create_from_path(*output)

    def GetCreators(self):
        self.cursor.execute("SELECT CREATOR FROM " + self.name)
        return list(set(self.cursor.fetchall()))

    def GetCreatorCards(self, creator: str):
        self.cursor.execute("SELECT * FROM " + self.name + "WHERE CREATOR = " + creator)
        output = self.cursor.fetchall()
        return [Card.create_from_path(*entry) for entry in output]


class CardManager:
    def __init__(self, driver: CardDriver):
        self.driver: CardDriver = driver

    def save(self, card: Card):
        return self.driver.save(card)

    def load(self, identifier):
        return self.driver.load(identifier)
