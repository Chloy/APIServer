from sqlalchemy import create_engine, MetaData
from api import models


DSN = "postgresql://postgres:1234@localhost:5432/todolist"


def main():
    engine = create_engine(DSN)
    models.Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()