from sqlalchemy import MetaData, Table, Column, \
    Integer, String, ForeignKey, Date
from aiopg.sa import create_engine
from aiohttp import web


async def get_engine(app: web.Application):
    engine = await create_engine(
        database='pools',
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


question = Table(
    'question',
    meta,
    Column('id', Integer, primary_key=True),
    Column('text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False)
)

choise = Table(
    'choise',
    meta,
    Column('id', Integer, primary_key=True),
    Column('text', String(100), nullable=False),
    Column('votes', Integer, nullable=False),
    Column('question_id', Integer, ForeignKey(
        'question.id',
        ondelete='CASCADE'
    ))
)