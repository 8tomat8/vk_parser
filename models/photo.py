from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from . import Base


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    # post = relationship('Post', back_populates='photos')
    link = Column(String, nullable=False)
    text = Column(String, nullable=False)
