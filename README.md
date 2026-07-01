# dmitry-it-platform

Бэкенд для внутренней платформы управления стажёрами.
Стек: Python 3.11+, Django, Django REST Framework, PostgreSQL, Docker

## Задача — 2 крупные фичи

### 1. REST API сотрудников

Эндпоинты:
- GET /api/employees/ — список с фильтрацией по статусу, поиском по имени
- GET /api/employees/{id}/ — детальная страница
- POST /api/employees/ — создать
- PATCH /api/employees/{id}/ — обновить статус, readiness score
- DELETE /api/employees/{id}/ — удалить

Модели:
- Employee: name, avatar, status (active/blocked/finished),
  stack (array), readiness_score (0-100), current_task, mentor_id
- Task: title, assignee, status (todo/in_progress/review/done),
  deadline, subtasks (JSON)
- Review: employee, criteria scores (JSON), feedback,
  result (ready/not_ready/repeat_sprint), created_at

Требования:
- Валидация через DRF serializers
- Пагинация на всех списках
- docker-compose.yml — приложение + PostgreSQL одной командой
- Postman-коллекция или README с примерами запросов

### 2. Авторизация и роли

- JWT авторизация (djangorestframework-simplejwt)
- Роли: admin / mentor / viewer
- Пермишены: viewer только читает, mentor создаёт ревью,
  admin всё
- Эндпоинты: POST /api/auth/login/, POST /api/auth/refresh/,
  GET /api/auth/me/

## Запуск
docker-compose up --build

## Сдача
Когда готово — скинь ссылку на репо.
Вопросы пиши, отвечу в течение дня.
