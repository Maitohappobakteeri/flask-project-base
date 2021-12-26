from .base import Base

from sqlalchemy import Column, Integer, CHAR, ForeignKey, Boolean, DateTime


class AuthToken(Base):
    __tablename__ = 'auth_token'

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    jti = Column(CHAR(37), primary_key=True)
    owner = Column(Integer, ForeignKey('user.id'), nullable=False)
    access = Column(Boolean, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    client = Column(Integer, nullable=False)
