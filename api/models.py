from sqlalchemy import MetaData, Table, Column, \
    Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine as get_sql_engine
from aiopg.sa import create_engine
from aiohttp import web


Base = declarative_base()


def create_engine():
    return get_sql_engine("postgresql://postgres:1234@localhost/todolist")


async def get_engine(app: web.Application):
    engine = await create_engine(
        database='todolist',
        user='postgres',
        password='1234',
        host='localhost',
        port='5432'
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


meta = MetaData()


class User(Base):
    __tablename__  = 'user'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)

    todos = relationship('Todo', secondary='user_todo', viewonly=True)

    def __repr__(self) -> str:
        return str(self.name)


class User_Todo(Base):
    __tablename__ = 'user_todo'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    todo_id = Column(Integer, ForeignKey('todo.id'), primary_key=True)

    user = relationship(
        'User', 
        backref=backref('user_todo', cascade='all, delete-orphan')
    )
    todo = relationship(
        'Todo',
        backref=backref('user_todo', cascade='all, delete-orphan')
    )


class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)

    users = relationship('User', secondary='user_todo', viewonly=True)
    tasks = relationship('Task', secondary='todo_task ', viewonly=True)

    def __repr__(self) -> str:
        return str(self.name)


class Todo_Task(Base):
    __tablename__ = 'todo_task'
    todo_id = Column(Integer, ForeignKey('todo.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    todo = relationship(
        'Todo',
        backref=backref('todo_task', cascade='all, delete-orphan')
    )
    task = relationship(
        'Task',
        backref=backref('todo_task', cascade='all, delete-orphan')
    )


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(500), nullable=False)

    todos = relationship('Todo', secondary='todo_task', viewonly=True)

    def __repr__(self) -> str:
        return f"{self.name}: {self.desc[:15]}..."