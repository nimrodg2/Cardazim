import time
import pytest

import Cardazim.client
import Cardazim.card
import Cardazim.Connection
from Cardazim import listener
import threading


def test_t1(tcard: Cardazim.card.Card):
    ip = '127.0.0.1'
    port = 1729
    with listener.Listener(ip, port) as server:
        while True:
            with server.accept() as connection:
                new_data = connection.receive_message()
                new_card = Cardazim.card.Card.deserialize(new_data)
                if new_card.image.decrypt(tcard.solution):
                    new_card.solution = tcard.solution
                assert tcard.__repr__() == new_card.__repr__()


def test_t2(tcard):
    Cardazim.client.send_data('127.0.0.1', 1729, tcard)


def test_client():
    test_card = Cardazim.card.Card.create_from_path("t1", "c1", 'Iran_Pigeon.png', 'r1', 's1')
    t1 = threading.Thread(target=test_t1, args=(test_card))
    t1.start()
    time.sleep(3)
    t2 = threading.Thread(target=test_t2)
    t2.start()

