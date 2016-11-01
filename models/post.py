from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from . import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, primary_key=True)
    from_id = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
    _likes = Column('likes', Integer, default=0)
    _reposts = Column('reposts', Integer, default=0)
    text = Column(String)
    # attachment = relationship(Attachments)
    # attachment_id = Column(Integer, ForeignKey('attachment.id'))

    @property
    def likes(self):
        return self._likes

    @likes.setter
    def likes(self, value):
        self._likes = value['count']

    @property
    def reposts(self):
        return self._reposts

    @reposts.setter
    def reposts(self, value):
        self._reposts = value['count']
