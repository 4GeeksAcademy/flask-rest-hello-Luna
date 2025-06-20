from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str]=mapped_column(String(25), unique=True, nullable=False)
    firstname: Mapped[str]=mapped_column(String(25), unique=True, nullable=False)
    lastname: Mapped[str]=mapped_column(String(25), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    followers: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys='Follower.user_to_id',
        back_populates='followed',
        cascade='all, delete-orphan'
    )
    following: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys='Follower.user_from_id',
        back_populates='follower',
        cascade='all, delete-orphan'
    )
    posts: Mapped[list['Post']] = relationship(
        back_populates='user', cascade='all, delete-orphan')
    commented: Mapped[list['Comment']] = relationship(
        back_populates='author', cascade='all, delete-orphan'
    )

class Follower(db.Model):
    __tablename__='follower'
    user_from_id: Mapped[int]=mapped_column(ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int]=mapped_column(ForeignKey('user.id'), primary_key=True)

    follower: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_from_id],
        back_populates='following'
    )
    followed: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_to_id],
        back_populates='followers'
    )

class Post(db.Model):
    __tablename__='post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('user.id'))
    user:Mapped['User']=relationship(
        back_populates='posts')
    media:Mapped[list['Media']]=relationship(
        back_populates='post', cascade='all, delete-orphan'
    )
    comments:Mapped[list['Comment']]=relationship(
        back_populates='post_commented', cascade='all, delete-orphan')

class Media(db.Model):
    __tablename__='media'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type:Mapped[str]= mapped_column(String(25), nullable=False)
    url:Mapped[str]= mapped_column(String(50), nullable=False)
    post_id: Mapped[int]=mapped_column(ForeignKey('post.id'))
    post:Mapped['Post']=relationship(
        back_populates='media')

class Comment(db.Model):
    __tablename__='comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str]= mapped_column(String(200), nullable=False)
    author_id: Mapped[int]= mapped_column(ForeignKey('user.id'))
    author:Mapped['User']=relationship(
        back_populates='commented')
    post_id: Mapped[int]= mapped_column(ForeignKey('post.id'))
    post_commented:Mapped['Post']=relationship(
        back_populates='comments')