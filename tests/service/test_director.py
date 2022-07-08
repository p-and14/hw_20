from unittest.mock import MagicMock

import pytest

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)
    d1 = Director(id=1, name="Тейлор Шеридан")
    d2 = Director(id=2, name="Квентин Тарантино")
    d3 = Director(id=3, name="Владимир Вайншток")

    director_dao.get_one = MagicMock(return_value=d1)
    director_dao.get_all = MagicMock(return_value=[d1, d2, d3])
    director_dao.create = MagicMock(return_value=Director(id=4))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None, "Не находит режиссёра по ID"
        assert director.id is not None, "Не находит режиссёра по ID"
        assert director.name == "Тейлор Шеридан", "Находит неверного режиссёра по ID"

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) > 0, "Не находит всех режиссёров"

    def test_create(self):
        director_d = {"name": "Стив Энтин"}

        director = self.director_service.create(director_d)

        assert director.id is not None, "Не создаёт режиссёра"

    def test_update(self):
        director_d = {"id": 1, "name": "Роб Маршалл"}
        self.director_service.update(director_d)

    def test_partially_update(self):
        director_d = {"id": 1, "name": "Роб Маршалл"}
        self.director_service.partially_update(director_d)

    def test_delete(self):
        self.director_service.delete(1)
