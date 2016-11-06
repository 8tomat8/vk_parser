from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Text
from . import Base


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='photos')
    link = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
