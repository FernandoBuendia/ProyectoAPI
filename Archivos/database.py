from peewee import *
from datetime import datetime

from .security import hash_password


BaseDeDatos = MySQLDatabase("ToDoListApp", user = "root", password = "FBMM1477",
                            host = "localhost", port = 3306)

class BaseModel(Model):
  class Meta:
    database = BaseDeDatos

class User(BaseModel):
  id = AutoField()
  username = CharField(max_length = 50, unique = True)
  password = CharField(max_length = 100)
  created_at = DateTimeField(default = datetime.now)

  class Meta:
    table_name = "users"

  @staticmethod
  def generate_password(password: str):
    return hash_password(password)

class Task(BaseModel):
  id = AutoField()
  title = CharField(max_length = 100)
  description = TextField(null = True)
  completed = BooleanField(default = False)
  user = ForeignKeyField(User, backref = "tasks", on_delete = "CASCADE")
  created_at = DateTimeField(default = datetime.now)

  class Meta:
    table_name = "tasks"
