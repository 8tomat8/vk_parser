from urllib.requests import urlretrieve


def photo(data, post_id, owner_id):
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
    fields = ('src_xxxbig', 'src_xxbig', 'src_xbig', 'src_small', 'src')

    for f in fields:
        try:
            link = data[f]
            filename = link.split('/')[-1]
            urlretrieve(link, path + filename)

        except:
            pass


def default():
    pass