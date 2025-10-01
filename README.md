# Sprint 4 — BooksCollector (tests)

## Что проверяется
- `add_new_book` — добавление книги, валидация имени (1..40), без дублей.
- `set_book_genre` — установка жанра только для существующей книги и из допустимых жанров.
- `get_book_genre` — возврат жанра/пусто/None.
- `get_books_with_specific_genre` — фильтрация по жанру (только допустимые).
- `get_books_genre` — словарь всех книг с жанрами.
- `get_books_for_children` — исключение жанров с возрастным рейтингом (`Ужасы`, `Детективы`).
- `add_book_in_favorites` / `delete_book_from_favorites` / `get_list_of_favorites_books`.

## Как запустить
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -v tests.py