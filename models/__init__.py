from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from .post import Post
from .photo import Photo


__all__ = ['Post', 'Photo', 'Base']
