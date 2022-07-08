from unittest.mock import MagicMock

import pytest

from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)
    m1 = Movie(id=1, title="Йеллоустоун")
    m2 = Movie(id=2, title="Омерзительная восьмерка")
    m3 = Movie(id=3, title="Вооружен и очень опасен")

    movie_dao.get_one = MagicMock(return_value=m1)
    movie_dao.get_all = MagicMock(return_value=[m1, m2, m3])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None, "Не находит фильм по ID"
        assert movie.id is not None, "Не находит фильм по ID"
        assert movie.title == "Йеллоустоун", "Находит неверный фильм по ID"

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0, "Не находит все фильмы"

    def test_create(self):
        movie_d = {"title": "Джанго освобожденный"}
        movie = self.movie_service.create(movie_d)

        assert movie.id is not None, "Не создаёт фильм"

    def test_update(self):
        movie_d = {"id": 1, "title": "Рокетмен"}
        self.movie_service.update(movie_d)

    def test_delete(self):
        self.movie_service.delete(1)
