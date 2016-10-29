class Wall:

    COUNT = 100
    fields_list = ['post_type', 'date', 'domain', 'id', 'from_id', 'text',
                   'attachments', 'likes', 'reposts']
    posts_transmitted = 0
    total_count = 0
    _current_offset = 0

    def __init__(self, owner_id, api=None, start_iteration=0):
        if not api:
            from vk import Session, API
            self.api = API(Session())
        else:
            self.api = api
        self.owner_id = owner_id
        self.iteration = start_iteration

    def __iter__(self):
        while True:
            posts = self.__get_posts(self.iteration)

            if not self.total_count:
                self.total_count = posts[0]

            if self.total_count < self.COUNT:
                self._current_offset -= self.COUNT
                posts = self.__get_posts(self.iteration, self.total_count)

            self.total_count -= len(posts) - 1
            self.iteration += 1

            yield posts

            if self.total_count == 0:
                assert StopIteration
                break

    def __get_posts(self, iteration, count=COUNT):
        rv = self.api.wall.get(
            owner_id=self.owner_id,
            offset=self._current_offset,
            count=count,
            fields=','.join(self.fields_list)
        )
        self._current_offset += self.COUNT

        return rv
