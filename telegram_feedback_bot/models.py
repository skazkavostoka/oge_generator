from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)

    lessons = relationship('Lesson', back_populates='student', cascade='all, delete-orphan')


class ParentChild(Base):
    __tablename__ = 'ParentChild'

    id=Column(Integer, primary_key=True, autoincrement=True)
    parent_id=Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    child_id=Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))

    parent = relationship('User', foreign_keys=[parent_id])
    child = relationship('User', foreign_keys=[child_id])



class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    hw_res = Column(String, nullable=True)
    cw_res = Column(String, nullable=True)
    test_res = Column(String, nullable=True)

    student = relationship('User', back_populates='lessons')

