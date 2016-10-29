from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from .wall import Wall


__all__ = ['Wall', 'Base']
