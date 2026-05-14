from peewee import *
from datetime import datetime


BaseDeDatos = MySQLDatabase("ToDoListApp", user = "root", password = "FBMM1477",
                            host = "localhost", port = 3306)

class BaseModel(Model):
  class Meta:
    database = BaseDeDatos

class User(BaseModel):
  id = AutoField()
  username = CharField(max_length = 50, unique = True)
  password = CharField(max_length = 50)
  created_at = DateTimeField(default = datetime.now)

  class Meta:
    table_name = "users"

class Task(BaseModel):
  title = CharField(max_length = 100)
  description = TextField(null = True)
  completed = BooleanField(default = False)
  user = ForeignKeyField(User.username, backref = "tasks", on_delete = "CASCADE")
  created_at = DateTimeField(default = datetime.now)

  class Meta:
    table_name = "tasks"
