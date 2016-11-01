import vk
import trafaret as t
from datetime import datetime
import resources
from models import Post
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
    mask = t.Dict({
        'from_id': t.Int,
        'date': lambda v: datetime.fromtimestamp(v),
        'text': t.String(allow_blank=True),
        t.Key('id') >> 'post_id': t.Int,
        t.Key('likes') >> 'likes_count': lambda v: int(v['count']),
        t.Key('reposts') >> 'reposts_count': lambda v: int(v['count']),
        t.Key('attachments', optional=True) >>
        'attachments': t.List(t.Dict().allow_extra('*'))
    }).ignore_extra('*')
    api = vk.API(vk.Session())

    posts = resources.Posts(wall_owner_id, api)

    counter = 0

    for post in posts:
        data = mask.check(post)
        data['owner_id'] = wall_owner_id
        if data.get('attachments'):
            del data['attachments']
        session.add(Post(**data))
        counter += 1
        if not counter % 100:
            print(counter)

    session.commit()


if __name__ == '__main__':
    # init_db()
    main()
