import pytest
from main import BooksCollector

def test_smoke_import_and_empty_state():
    bc = BooksCollector()
    assert bc.get_books_genre() == {}

# --- add_new_book: валидные имена (границы 1 и 40) ---
@pytest.mark.parametrize("name", ["А", "Война и мир", "X" * 40])
def test_add_new_book_valid_names_added_with_empty_genre(name):
    bc = BooksCollector()
    bc.add_new_book(name)
    assert name in bc.get_books_genre() and bc.get_book_genre(name) == ""

    # --- add_new_book: невалидные имена (пусто и >40) ---
@pytest.mark.parametrize("name", ["", "Y" * 41])
def test_add_new_book_invalid_names_not_added(name):
    bc = BooksCollector()
    bc.add_new_book(name)
    assert name not in bc.get_books_genre()

    # --- add_new_book: дубликаты не добавляются ---
def test_add_new_book_duplicate_not_added_twice():
    bc = BooksCollector()
    bc.add_new_book("Дюна")
    bc.add_new_book("Дюна")
    assert list(bc.get_books_genre().keys()).count("Дюна") == 1

    # --- set_book_genre: ок, если книга есть и жанр допустим ---
def test_set_book_genre_ok_when_book_exists_and_genre_allowed():
    bc = BooksCollector()
    bc.add_new_book("Солярис")
    bc.set_book_genre("Солярис", "Фантастика")
    assert bc.get_book_genre("Солярис") == "Фантастика"
    
    # --- set_book_genre: игнор, если книги нет ---
def test_set_book_genre_ignored_for_unknown_book():
    bc = BooksCollector()
    bc.set_book_genre("Неизвестная", "Фантастика")
    assert bc.get_book_genre("Неизвестная") is None
    
    # --- set_book_genre: игнор, если жанр не из списка ---
def test_set_book_genre_ignored_for_disallowed_genre():
    bc = BooksCollector()
    bc.add_new_book("Сказки")
    bc.set_book_genre("Сказки", "Ромком")  # нет такого жанра в списке
    assert bc.get_book_genre("Сказки") == ""

    # --- get_book_genre: пустая строка, если жанр не задан ---
def test_get_book_genre_returns_empty_string_if_not_set():
    bc = BooksCollector()
    bc.add_new_book("Евгений Онегин")
    assert bc.get_book_genre("Евгений Онегин") == ""

    # --- get_book_genre: None, если книги нет ---
def test_get_book_genre_returns_none_if_book_absent():
    bc = BooksCollector()
    assert bc.get_book_genre("НЛО в Питере") is None

    # --- get_books_with_specific_genre: нормальная фильтрация ---
def test_get_books_with_specific_genre_filters_correctly():
    bc = BooksCollector()
    bc.add_new_book("Книга1"); bc.set_book_genre("Книга1", "Комедии")
    bc.add_new_book("Книга2"); bc.set_book_genre("Книга2", "Комедии")
    bc.add_new_book("Книга3"); bc.set_book_genre("Книга3", "Ужасы")
    assert sorted(bc.get_books_with_specific_genre("Комедии")) == ["Книга1", "Книга2"]

    # --- get_books_with_specific_genre: если жанр недопустим, возвращает пусто ---
def test_get_books_with_specific_genre_returns_empty_for_disallowed_genre():
    bc = BooksCollector()
    bc.add_new_book("Книга"); bc.set_book_genre("Книга", "Комедии")
    assert bc.get_books_with_specific_genre("Романтика") == []
    
    # --- get_books_for_children: исключаем возрастные жанры (Ужасы, Детективы) ---
def test_get_books_for_children_excludes_age_restricted_genres():
    bc = BooksCollector()
    bc.add_new_book("Жуть"); bc.set_book_genre("Жуть", "Ужасы")
    bc.add_new_book("Шерлок"); bc.set_book_genre("Шерлок", "Детективы")
    bc.add_new_book("Том и Джерри"); bc.set_book_genre("Том и Джерри", "Мультфильмы")
    assert bc.get_books_for_children() == ["Том и Джерри"]

    # --- add_book_in_favorites: только существующие книги и без дублей ---
def test_add_book_in_favorites_only_if_in_books_genre_and_no_duplicates():
    bc = BooksCollector()
    bc.add_new_book("Богатырь")
    bc.add_book_in_favorites("Богатырь")
    bc.add_book_in_favorites("Богатырь")   # второй раз — игнор
    bc.add_book_in_favorites("НетТакой")   # книги нет — игнор
    assert bc.get_list_of_favorites_books() == ["Богатырь"]

    # --- delete_book_from_favorites: удаляет если есть ---
def test_delete_book_from_favorites_removes_when_present():
    bc = BooksCollector()
    bc.add_new_book("Робот"); bc.add_book_in_favorites("Робот")
    bc.delete_book_from_favorites("Робот")
    assert bc.get_list_of_favorites_books() == []

    # --- get_list_of_favorites_books: возвращает список ---
def test_get_list_of_favorites_books_returns_list():
    bc = BooksCollector()
    bc.add_new_book("A"); bc.add_book_in_favorites("A")
    assert isinstance(bc.get_list_of_favorites_books(), list)