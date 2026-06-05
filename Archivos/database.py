from datetime import datetime

from peewee import *

from .security import hash_password, verify_password

BaseDeDatos = MySQLDatabase(
    "ToDoListApp", user="root", password="FBMM1477", host="localhost", port=3306
)


class BaseModel(Model):
    class Meta:
        database = BaseDeDatos


class User(BaseModel):
    id = AutoField()
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "users"

    @staticmethod
    def generate_password(password: str):
        return hash_password(password)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.select().where(cls.username == username).first()

        if user and verify_password(password, user.password):
            return user


class Task(BaseModel):
    id = AutoField()
    title = CharField(max_length=100)
    description = TextField(null=True)
    completed = BooleanField(default=False)
    user_id = ForeignKeyField(User.id, backref="tasks", on_delete="CASCADE")
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "tasks"
