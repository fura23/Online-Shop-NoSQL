# NoSQL Online Store

Rozszerzenie projektu sklepu internetowego w Pythonie i MongoDB przygotowane w ramach zaliczenia z NoSQL.

## Features

Projekt zawiera wymagania na ocenę 5, czyli:
- walidację pustych pól tekstowych,
- walidację adresu email,
- walidację numeru telefonu,
- wyświetlanie wszystkich zamówień wybranego klienta,
- agregację liczby zamówień dla każdego klienta,
- agregację łącznej wartości zamówień dla każdego klienta.

## Tech Stack

- Python 3
- MongoDB
- PyMongo

## Project Structure

- `final.py` – główny plik projektu z implementacją i testami
- `NoSQL_zadania_zaliczeniowe.pdf` – treść zadania
- `README.md` – opis projektu

## Implemented Functions

### Validation
- `is_empty_string()`
- `validate_email()`
- `validate_phone()`

### Products
- `add_product()`
- `view_product()`
- `view_all_products()`
- `update_product()`
- `delete_product()`

### Customers
- `add_customer()`
- `view_customer()`
- `view_all_customers()`
- `update_customer()`
- `delete_customer()`

### Orders
- `add_order()`
- `view_orders_by_customer()`

### Aggregation
- `count_orders_per_customer()`
- `total_spent_per_customer()`

## Validation Rules

### Empty strings
Pola tekstowe nie mogą być puste ani składać się wyłącznie ze spacji.

### Email
Adres email musi:
- zawierać `@`,
- mieć niepustą nazwę użytkownika,
- mieć niepustą domenę,
- zawierać kropkę w domenie.

### Phone
Numer telefonu:
- może zawierać cyfry, spacje, myślniki i nawiasy,
- musi zawierać co najmniej 7 cyfr.

## Aggregation Results

Projekt implementuje dwie funkcje agregacyjne:
- `count_orders_per_customer()` – zwraca liczbę zamówień dla każdego klienta,
- `total_spent_per_customer()` – zwraca łączną wartość zamówień dla każdego klienta.


## Notes

Program tworzy bazę `online_store` oraz kolekcje:
- `products`
- `customers`
- `orders`

W pliku `final.py` znajdują się także przykładowe testy danych poprawnych i błędnych.

## Author

Projekt wykonany w ramach zaliczenia z przedmiotu NoSQL.

## License
This project is provided for viewing, downloading, running, and private modification only.
Redistribution, republication, commercial use, and claiming authorship or ownership are prohibited without prior written permission from the author.
