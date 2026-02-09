import uuid
from typing import Any, Sequence

from sqlalchemy import ForeignKey, Integer, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)


class Base(DeclarativeBase):
    pass


# Utils
def generate_uuid() -> str:
    return str(uuid.uuid4())


# custom error
class InviladInput(Exception):
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.message} (Status: {self.status_code})"


# Tables
class User(Base):
    __tablename__ = "users"

    userId: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(32), unique=True)
    profile_name: Mapped[str] = mapped_column(String(32))

    # Relationship
    post: Mapped[list["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = "posts"

    postId: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.userId"))
    content: Mapped[str] = mapped_column(String(32))

    # Relationship
    author: Mapped["User"] = relationship(back_populates="post")
    likes: Mapped[list["Like"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )


class Like(Base):
    __tablename__ = "likes"

    likeId: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    post_id: Mapped[str] = mapped_column(String(36), ForeignKey("posts.postId"))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.userId"))

    # Relationship
    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")


# creating User
def add_user(
    session: Session,
    first_name: str,
    last_name: str,
    email: str,
    profile_name: str,
) -> None:

    user_exists = session.scalar(select(User).filter(User.email == email))
    if user_exists:
        raise InviladInput(
            message=f"User with email:{email} already exist", status_code=409
        )

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        profile_name=profile_name,
    )
    session.add(user)
    session.commit()
    session.refresh(user)


# creating post
def add_post(session: Session, user: User, content: str) -> Post:
    post = Post(author=user, content=content)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


# creating likes
def add_like(session: Session, user: User, post: Post) -> None:
    new_like = Like(user=user, post=post)
    session.add(new_like)
    session.commit()
    session.refresh(new_like)


# Retreaving Post
def get_all_posts(session: Session) -> Sequence[Post]:
    return session.query(Post).all()


def get_all_users(session: Session) -> Sequence[User]:
    return session.query(User).all()


def get_post_with_user_id(session: Session, user_id: str) -> Sequence[Post]:
    return session.scalars(select(Post).filter(Post.user_id == user_id)).all()


def get_user_like_post(session: Session, post_id: str) -> Sequence | None:
    # return session.scalars(
    #     select(User).join(Like).filter(Like.post_id == post_id)  # noqa: ERA001
    # ).all()
    post = session.get(Post, post_id)
    if post is None:
        return []
    return [like.user for like in post.likes]


# Test Datas
def test_data_add_user() -> None:
    add_user(
        session=session,
        first_name="Pema",
        last_name="Dendup",
        email="pema@gmail.com",
        profile_name="Pema",
    )
    add_user(
        session=session,
        first_name="Dorji",
        last_name="Zangpo",
        email="dorjizangpo@gmail.com",
        profile_name="Alpha",
    )
    add_user(
        session=session,
        first_name="Jigdrel",
        last_name="Dorji",
        email="Jigdrel@gmail.com",
        profile_name="Joney",
    )
    add_user(
        session=session,
        first_name="Sangay",
        last_name="Nidup",
        email="sangayy@gmail.com",
        profile_name="Sangay",
    )
    add_user(
        session=session,
        first_name="Pema",
        last_name="Wangmo",
        email="pema.wangmo99@outlook.com",
        profile_name="PemaW",
    )
    add_user(
        session=session,
        first_name="Tenzin",
        last_name="Dorji",
        email="tenzin.dorji@druknet.bt",
        profile_name="TenzinD",
    )
    add_user(
        session=session,
        first_name="Sonam",
        last_name="Choden",
        email="sonamcho@gmail.com",
        profile_name="Sona_Cho",
    )
    add_user(
        session=session,
        first_name="Ugyen",
        last_name="Tshering",
        email="ugyentshering@gmail.com",
        profile_name="UgyenT",
    )
    add_user(
        session=session,
        first_name="Karma",
        last_name="Loday",
        email="karmaloday7@gmail.com",
        profile_name="KarmaL",
    )
    add_user(
        session=session,
        first_name="Dechen",
        last_name="Zangmo",
        email="dechenz@outlook.com",
        profile_name="DechenZ",
    )


# showing Output
def display_all_posts() -> None:
    print("All Posts")
    print(
        "-----------------------------------------------------------------------------------------------------"
    )
    all_post = get_all_posts(session=session)
    for post in all_post:
        print(post.postId, " | ", post.user_id, " | ", post.content)


def display_all_user() -> None:
    print("All Uaers")
    print(
        "-----------------------------------------------------------------------------------------------------"
    )
    all_user = get_all_users(session=session)
    for user in all_user:
        print(user.userId, " | ", user.first_name)


def display_users_post(user_id: str) -> None:
    print("post by user")
    print(
        "-----------------------------------------------------------------------------------------------------"
    )
    post_by_user = get_post_with_user_id(session=session, user_id=user_id)
    for post in post_by_user:
        print(post.postId, " | ", post.user_id, " | ", post.content)


def display_user_like_post(post_id: str) -> None:
    users: Sequence | None = get_user_like_post(session=session, post_id=post_id)
    if users is None:
        return
    print(f"Post ID: {post_id}, Total Likes:{len(users)}\nThey are: ")
    for user in users:
        print(f"Name: {user.first_name} {user.last_name} \t email: {user.email}")


# assining database engine
db = "sqlite:///socialDB.db"
engine = create_engine(url=db, echo=False)


# creating table
Base.metadata.create_all(bind=engine)  # noqa: ERA001

# creating session
SessionLocal = sessionmaker(bind=engine)

# code goes here with satement
with SessionLocal() as session:
    # pema = User(
    #     first_name="Pema1",
    #     last_name="Dendup",
    #     email="pema1231@gmail.com",
    #     profile_name="Pema",
    # )
    # dorji = User(
    #     first_name="Dorji1",
    #     last_name="Zangpo",
    #     email="dorji1231@gmail.com",
    #     profile_name="Alpha",
    # )
    # session.add_all([pema, dorji])
    # session.commit()
    # session.refresh(pema)
    # session.refresh(dorji)

    # p_post = add_post(session=session, user=pema, content="Happy Jurmey")
    # d_post = add_post(session=session, user=dorji, content="Happy Jurmey")

    # p_liked_d = add_like(session=session, user=pema, post=d_post)
    # d_liked_p = add_like(session=session, user=dorji, post=p_post)
    display_user_like_post("2b03dea3-eadc-4a81-9474-48bf15a9cdd8")
