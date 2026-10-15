import os

import pytest

from model.database import Database
from model.house import House


@pytest.fixture
def house():
    h = House("ул. Ленина, 5")
    f = h.add_flat(101)
    f.add_room("спальня", 4, 5)
    f.add_room("кухня", 3, 3)
    f = h.add_flat(102)
    f.add_room("студия", 5, 6)
    return h


@pytest.fixture
def db(tmp_path):
    with Database(os.path.join(tmp_path, "test.db")) as d:
        yield d


def test_empty_database(db):
    assert len(db) == 0
    assert db.history() == []


def test_save_and_history(db, house):
    calc_id = db.save(house, 21, -5, 1)
    assert calc_id == 1
    assert len(db) == 1
    row = db.history()[0]
    assert row[0] == 1
    assert row[2] == "ул. Ленина, 5"
    assert row[3] == 59
    assert row[4] == pytest.approx(house.heat_power(21, -5, 1))


def test_load_house(db, house):
    calc_id = db.save(house, 21, -5, 1)
    h = db.load_house(calc_id)
    assert h.address == house.address
    assert len(h) == 2
    assert [f.number for f in h.flats] == [101, 102]
    assert [r.name for r in h.flats[0].rooms] == ["спальня", "кухня"]
    assert h.area() == house.area()
    assert h.volume() == house.volume()


def test_load_missing_house(db):
    assert db.load_house(99) is None


def test_save_wrong_params(db, house):
    with pytest.raises(ValueError):
        db.save(house, 10, 20, 1)
    assert len(db) == 0


def test_data_kept_after_reopen(tmp_path, house):
    path = os.path.join(tmp_path, "folder", "test.db")
    with Database(path) as d:
        d.save(house, 21, -5, 1)
        d.save(house, 20, -25, 1.5)
    with Database(path) as d:
        assert len(d) == 2
        assert repr(d) == "Database(2 расчётов)"
