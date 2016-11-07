from json import dumps
from collections import defaultdict
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
        self.objects_to_save = []

    def download(self, data):
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
            download_tasks = (types[e['type']](e, s) for e in data)
            rv = dumps(loop.run_until_complete(gather(*download_tasks)))
            self.result = rv

        return self.result, self.objects_to_save

    async def photo(self, data: dict, session):
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
                  'src', 'src_small',
                  )

        for f in fields:
            try:
                link = data['photo'][f]
                filename = link.split('/')[-1]
                break
            except KeyError:
                pass

        async with session.get(link) as response:
            with closing(response), open(path + filename, 'wb') as file:
                while True:  # save file
                    chunk = await response.content.read(1 << 15)
                    if not chunk:
                        break
                    file.write(chunk)
        self.objects_to_save.append(Photo(post_id=self.post_id,
                                          link=link,
                                          text=data['photo']['text'],
                                          filename=filename))

    async def default(self, data, *_):
        return data
