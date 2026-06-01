# ToDo List API

API REST desarrollada con FastAPI para la gestión de usuarios y tareas.

## Tecnologías

- Python
- FastAPI
- MySQL
- Peewee ORM
- Pydantic
- Passlib
- Bcrypt

## Funcionalidades

- Registro de usuarios
- Autenticación
- Gestión de tareas
- CRUD completo
- Validación de datos
- Hash de contraseñas

## Endpoints

POST /api/v1/users
GET /api/v1/users/{id}
DELETE /api/v1/users/{id}

POST /api/v1/tasks
GET /api/v1/tasks/{id}
PUT /api/v1/user/{user_id}/tasks/{task_id}
DELETE /api/v1/tasks/{id}

POST /api/v1/authentication