from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
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
    text = Column(String)
    # photos = relationship("Photo", back_populates='post')
    UniqueConstraint('post_id', 'owner_id', name='uidx_PostId_OwnerId')
