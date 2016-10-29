import vk
import resources
from models import Wall
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


engine = create_engine('sqlite:///vk.db')
session = sessionmaker(bind=engine)()


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def main():
    # wall_owner_id = -77868632  # Force
    # wall_owner_id = -101555444  # CopyPaste
    wall_owner_id = -58010960  # target
    wall_columns = ['id', 'from_id', 'date', 'likes', 'reposts', 'text']

    api = vk.API(vk.Session())

    wall = resources.Wall(wall_owner_id, api)

    counter = 0

    for posts in wall:
        for post in posts[1:]:
            data = {'owner_id': wall_owner_id}
            data.update({key: post[key] for key in wall_columns})
            session.add(Wall(**data))
            counter += 1
        print(counter)

    session.commit()


if __name__ == '__main__':
    # init_db()
    main()
