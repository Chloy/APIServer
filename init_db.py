from sqlalchemy import create_engine, MetaData
from api import models


DSN = "postgresql://postgres:1234@localhost:5432/pools"


def main():
    engine = create_engine(DSN)
    meta = MetaData()
    meta.create_all(engine, [models.question, models.choise])


if __name__ == '__main__':
    main()