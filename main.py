import vk
import uvloop
import pickle as p
import trafaret as t
from tqdm import tqdm
from datetime import datetime
from asyncio import set_event_loop_policy

import resources
from helpers.dowloader import Downloader
from helpers.attachments import Attachments
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Post


set_event_loop_policy(uvloop.EventLoopPolicy())
DEBUG = False
engine = create_engine('mysql://root:@127.0.0.1/vk?charset=utf8', echo=DEBUG)

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
        t.Key('owner_id', default=wall_owner_id): t.Int(),
        t.Key('likes') >> 'likes_count': lambda v: int(v['count']),
        t.Key('reposts') >> 'reposts_count': lambda v: int(v['count']),
        t.Key('attachments', optional=True) >>
        'attachments': t.List(t.Dict().allow_extra('*'))
    }).ignore_extra('*')
    api = vk.API(vk.Session())

    posts = resources.Posts(wall_owner_id, api)

    posts_list = []
    to_download = []
    try:
        # raise Exception
        posts_list = p.load(open("posts{}.pikle".format(wall_owner_id), "rb"))
        to_download = p.load(open("toDownload{}.pikle".format(wall_owner_id), "rb"))

        if len(posts_list) is 0 or len(to_download) is 0:
            raise Exception
        print('~~~***!!!Data taken from pickle!!!***~~~')
    except:
        for post in tqdm(posts):
            data = mask.check(post)
            if data.get('attachments'):
                attachments = Attachments(data['post_id'], data['owner_id'])
                data['attachments'], objects, links = \
                    attachments.prepare(data['attachments'])

                data.update(**objects)
                to_download.extend(links)

            post = Post(**data)
            posts_list.append(post)

        p.dump(posts_list, open("posts{}.pikle".format(wall_owner_id), "wb"))
        p.dump(to_download, open("toDownload{}.pikle".format(wall_owner_id), "wb"))

    Downloader(to_download).download()
    session.add_all(posts_list)
    session.commit()


if __name__ == '__main__':
    # init_db()
    main()
