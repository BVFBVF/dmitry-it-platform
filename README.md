# Backend API

Внутренняя платформа управления стажёрами.

**Стек:** Python 3.11+, Django 4.2, Django REST Framework, PostgreSQL, JWT (simplejwt), Docker.

## Быстрый старт

```bash
docker compose up --build
```

API: http://localhost:8000  
Admin: http://localhost:8000/admin/

После первого запуска создаются тестовые пользователи (пароль для всех: `password123`):

| Логин   | Роль   | Права                          |
|---------|--------|--------------------------------|
| admin   | admin  | полный доступ                  |
| mentor  | mentor | чтение + создание ревью        |
| viewer  | viewer | только чтение                  |

## Авторизация

### POST /api/auth/login/

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'
```

Ответ:
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### POST /api/auth/refresh/

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

### GET /api/auth/me/

```bash
curl http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

## Сотрудники (Employees)

Все запросы требуют заголовок `Authorization: Bearer <access_token>`.

### GET /api/employees/ — список

Параметры:
- `status` — фильтр: `active`, `blocked`, `finished`
- `search` — поиск по имени
- `page` — номер страницы (пагинация, 20 на страницу)
- `ordering` — сортировка: `name`, `-readiness_score`, `created_at`

```bash
curl "http://localhost:8000/api/employees/?status=active&search=Иван" \
  -H "Authorization: Bearer <access_token>"
```

### GET /api/employees/{id}/ — детали

```bash
curl http://localhost:8000/api/employees/1/ \
  -H "Authorization: Bearer <access_token>"
```

### POST /api/employees/ — создать (только admin)

```bash
curl -X POST http://localhost:8000/api/employees/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван Петров",
    "status": "active",
    "stack": ["Python", "Django", "PostgreSQL"],
    "readiness_score": 45,
    "mentor": 2
  }'
```

### PATCH /api/employees/{id}/ — обновить статус и readiness_score (только admin)

```bash
curl -X PATCH http://localhost:8000/api/employees/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "blocked", "readiness_score": 60}'
```

### DELETE /api/employees/{id}/ — удалить (только admin)

```bash
curl -X DELETE http://localhost:8000/api/employees/1/ \
  -H "Authorization: Bearer <access_token>"
```

## Задачи (Tasks)

### GET /api/tasks/

```bash
curl "http://localhost:8000/api/tasks/?assignee=1&status=in_progress" \
  -H "Authorization: Bearer <access_token>"
```

### POST /api/tasks/ — создать (только admin)

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Настроить CI/CD",
    "assignee": 1,
    "status": "todo",
    "deadline": "2026-08-01T12:00:00Z",
    "subtasks": [
      {"title": "Dockerfile", "done": false},
      {"title": "GitHub Actions", "done": false}
    ]
  }'
```

## Ревью (Reviews)

### GET /api/reviews/

```bash
curl "http://localhost:8000/api/reviews/?employee=1" \
  -H "Authorization: Bearer <access_token>"
```

### POST /api/reviews/ — создать (admin и mentor)

```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "employee": 1,
    "criteria_scores": {
      "code_quality": 8,
      "communication": 7,
      "initiative": 9
    },
    "feedback": "Хороший прогресс, нужно больше практики с тестами.",
    "result": "not_ready"
  }'
```

Значения `result`: `ready`, `not_ready`, `repeat_sprint`.

## Модели

### Employee
| Поле             | Тип      | Описание                              |
|------------------|----------|---------------------------------------|
| name             | string   | Имя стажёра                           |
| avatar           | image    | Аватар (опционально)                  |
| status           | enum     | `active` / `blocked` / `finished`     |
| stack            | array    | Стек технологий                       |
| readiness_score  | int      | 0–100                                 |
| current_task     | FK Task  | Текущая задача                        |
| mentor           | FK User  | ID ментора                            |

### Task
| Поле      | Тип     | Описание                                    |
|-----------|---------|---------------------------------------------|
| title     | string  | Название                                    |
| assignee  | FK      | Сотрудник                                   |
| status    | enum    | `todo` / `in_progress` / `review` / `done`  |
| deadline  | datetime| Дедлайн                                     |
| subtasks  | JSON    | Подзадачи                                   |

### Review
| Поле             | Тип      | Описание                                    |
|------------------|----------|---------------------------------------------|
| employee         | FK       | Сотрудник                                   |
| criteria_scores  | JSON     | Оценки по критериям                         |
| feedback         | text     | Комментарий                                 |
| result           | enum     | `ready` / `not_ready` / `repeat_sprint`     |
| created_at       | datetime | Дата создания                               |

## Роли и права

| Действие                    | viewer | mentor | admin |
|-----------------------------|--------|--------|-------|
| Чтение employees/tasks      | ✓      | ✓      | ✓     |
| CRUD employees              |        |        | ✓     |
| Чтение reviews              | ✓      | ✓      | ✓     |
| Создание reviews            |        | ✓      | ✓     |
| Изменение/удаление reviews  |        |        | ✓     |

## Локальная разработка без Docker

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# PostgreSQL должен быть запущен, настройки в .env
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Postman

Импортируйте коллекцию `postman/Stajirovk_API.postman_collection.json`.

Переменные коллекции:
- `base_url` — `http://localhost:8000`
- `access_token` — заполняется автоматически после Login
