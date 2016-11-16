from json import dumps
from collections import defaultdict
from collections import namedtuple
from asyncio import get_event_loop
from asyncio import gather
from aiohttp import ClientSession
from contextlib import closing

from models import Photo


class Attachments:

    def __repr__(self):
        return self.result

    def __init__(self, post_id: int, owner_id: int):
        self.post_id = post_id
        self.owner_id = owner_id
        __objects = namedtuple('objects', ['objects', 'links'])
        self.objects_to_save = __objects({}, [])

    def prepare(self, data):
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
        loop = get_event_loop()
        with closing(ClientSession()) as s:
            tasks = (types[e['type']](e, s) for e in data)
            rv = loop.run_until_complete(gather(*tasks))
            self.result = dumps([r for r in rv if r])

        return self.result,\
            self.objects_to_save.objects,\
            self.objects_to_save.links

    async def photo(self, data: dict, session):
        __type = 'photos'
        fields = ('src_xxxbig', 'src_xxbig', 'src_xbig', 'src_big',
                  'src', 'src_small',
                  )

        for f in fields:
            try:
                link = data['photo'][f]
                filename = link.split('/')[-1]
                break
            except KeyError:
                pass

        # path = 'cache/photos/'
        # async with session.get(link) as response:
        #     with closing(response), open(path + filename, 'wb') as file:
        #         while True:  # save file
        #             chunk = await response.content.read(1 << 15)
        #             if not chunk:
        #                 break
        #             file.write(chunk)
        self.objects_to_save.objects.setdefault(__type, []).append(
            Photo(post_id=self.post_id,
                  link=link,
                  text=data['photo']['text'],
                  filename=filename),
        )
        self.objects_to_save.links.append({'link': link, 'type': __type})

    async def default(self, data, *_):
        return data
