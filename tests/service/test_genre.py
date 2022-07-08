from unittest.mock import MagicMock

import pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)
    g1 = Genre(id=1, name="Комедия")
    g2 = Genre(id=2, name="Семейный")
    g3 = Genre(id=3, name="Фэнтези")

    genre_dao.get_one = MagicMock(return_value=g1)
    genre_dao.get_all = MagicMock(return_value=[g1, g2, g3])
    genre_dao.create = MagicMock(return_value=Genre(id=4))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None, "Не находит жанр по ID"
        assert genre.id is not None, "Не находит жанр по ID"
        assert genre.name == "Комедия", "Находит неверного жанр по ID"

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert len(genres) > 0, "Не находит все жанры"

    def test_create(self):
        genre_d = {"name": "Драма"}
        genre = self.genre_service.create(genre_d)

        assert genre.id is not None, "Не создаёт жанр"

    def test_update(self):
        genre_d = {"id": 1, "name": "Приключения"}
        self.genre_service.update(genre_d)

    def test_partially_update(self):
        genre_d = {"id": 1, "name": "Приключения"}
        self.genre_service.partially_update(genre_d)

    def test_delete(self):
        self.genre_service.delete(1)
