from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.types import Binary
from sqlalchemy.types import Text
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from . import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)
    from_id = Column(Integer)
    date = Column(DateTime, nullable=False)
    likes_count = Column('likes_count', Integer, default=0)
    reposts_count = Column('reposts_count', Integer, default=0)
    _text = Column('text', Binary, nullable=True)
    attachments = Column(Text)
    photos = relationship("Photo", back_populates='post')
    UniqueConstraint('post_id', 'owner_id', name='uidx_PostId_OwnerId')

    @hybrid_property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value.encode('utf8')

    @text.expression
    def text(cls):
        return cls._text
