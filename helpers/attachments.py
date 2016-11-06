from json import dumps
from collections import defaultdict
from asyncio import get_event_loop
from asyncio import Semaphore
from asyncio import gather
from asyncio import coroutine
from asyncio import wait
from aiohttp import ClientSession
from contextlib import closing


class Attachments:

    def __repr__(self):
        return self.result

    def __init__(self, post_id: int, owner_id: int):
        self.post_id = post_id
        self.owner_id = owner_id

    def download(self, data):
        return (yield from self.async_download(data))

    @coroutine
    def async_download(self, data: list):
        types = defaultdict(lambda: self.default)
        types.update({
            # Commented types will be added of necessity
            # 'doc':,
            'photo': self.photo,
            # 'album':,
            # 'audio':,
            # 'poll':,
            # 'page':,
            # 'link':,
            # 'video':,
        })
        rv = []
        semaphore = Semaphore(4)
        with (yield from semaphore), closing(get_event_loop()) as loop, \
                closing(ClientSession()) as session:
            download_tasks = (types[e['type']](e, session) for e in data)
            rv = loop.run_until_complete(wait(gather(*download_tasks)))
        self.result = dumps(rv)
        return self.result

    @coroutine
    def photo(self, data: dict, session):
        path = 'cache/photos/'
        {'access_key': 'd56cf68d40a5f4ba7b',
         'aid': -7,
         'created': 1477433642,
         'height': 549,
         'owner_id': -101271420,
         'pid': 436935371,
         'post_id': 31289,
         'src': 'https://pp.vk.me/c836338/v836338795/802a/J4uaRcNHVjU.jpg',
         'src_big': 'https://pp.vk.me/c836338/v836338795/802b/624tc0jELKU.jpg',
         'src_small': 'https://pp.vk.me/c836338/v836338795/8029/L0ghgGdL7dY.jpg',
         'src_xbig': 'https://pp.vk.me/c836338/v836338795/802c/rKOqgxVH3uQ.jpg',
         'text': '',
         'user_id': 100,
         'width': 807,
         }
        fields = ('src_xxxbig', 'src_xxbig', 'src_xbig', 'src_big',
                  'src_small', 'src',
                  )

        for f in fields:
            try:
                link = data['photo'][f]
                filename = path + link.split('/')[-1]
            except KeyError:
                pass

        response = yield from session.get(link)
        with closing(response), open(filename, 'wb') as file:
            while True:  # save file
                chunk = yield from response.content.read(1 << 15)
                if not chunk:
                    break
                file.write(chunk)

    @coroutine
    def default(self, data, *_):
        return data
