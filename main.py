import uuid
from typing import Any, Sequence

from sqlalchemy import ForeignKey, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


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

    def __init__(self, **kw: Any) -> None:  # noqa: ANN401
        super().__init__(**kw)


class Post(Base):
    __tablename__ = "posts"

    postId: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.userId"))
    content: Mapped[str] = mapped_column(String(32))

    def __init__(self, **kw: Any) -> None:  # noqa: ANN401
        super().__init__(**kw)


class Like(Base):
    __tablename__ = "likes"

    likeId: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    post_id: Mapped[str] = mapped_column(String(36), ForeignKey("posts.postId"))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.userId"))

    def __init__(self, **kw: Any) -> None:  # noqa: ANN401
        super().__init__(**kw)


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
def add_post(session: Session, user_id: str, content: str) -> None:
    post = Post(user_id=user_id, content=content)
    session.add(post)
    session.commit()
    session.refresh(post)


# creating likes
def add_like(session: Session, user_id: str, post_id: str) -> None:
    new_like = Like(post_id=post_id, user_id=user_id)
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


def get_user_like_post(session: Session, post_id: str) -> Sequence:
    return session.scalars(
        select(User, Like)
        .filter(Like.post_id == post_id)
        .filter(User.userId == Like.user_id)
    ).all()


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


def test_data_add_post() -> None:
    add_post(
        session=session,
        user_id="b98e5a6d-18ae-43ad-a37c-4f48ad8869df",
        content="Kuzuzangpo la!",
    )
    add_post(
        session=session,
        user_id="c0eb7b89-9756-4aa4-a357-d4bebf529bdf",
        content="Morning in Thimphu",
    )
    add_post(
        session=session,
        user_id="d4026a9d-34d1-4630-9e78-d79e0bfc7669",
        content="Ema Datshi time",
    )
    add_post(
        session=session,
        user_id="16827944-486d-4027-94ea-f9b6c7d7edc3",
        content="Heading to Paro",
    )
    add_post(
        session=session,
        user_id="7b55ccff-35f7-4b9a-a2cc-7e4cebf25ffd",
        content="Bhutan is beautiful",
    )


def test_data_add_like() -> None:
    # Pema likes their own "Kuzuzangpo la!" post
    add_like(
        session=session,
        user_id="b98e5a6d-18ae-43ad-a37c-4f48ad8869df",
        post_id="9f8f6e15-46eb-4783-9e90-1d2ad203e48d",
    )

    # Jigdrel likes Pema's greeting
    add_like(
        session=session,
        user_id="c0eb7b89-9756-4aa4-a357-d4bebf529bdf",
        post_id="9f8f6e15-46eb-4783-9e90-1d2ad203e48d",
    )

    # Karma likes Jigdrel's "Morning in Thimphu"
    add_like(
        session=session,
        user_id="7b55ccff-35f7-4b9a-a2cc-7e4cebf25ffd",
        post_id="ef8d5aa7-fb36-4938-9606-83d6ede5d99f",
    )

    # Sonam likes the "Ema Datshi time" post
    add_like(
        session=session,
        user_id="16827944-486d-4027-94ea-f9b6c7d7edc3",
        post_id="39050ed2-c682-423b-8653-5115c635d86d",
    )

    # Dechen likes Karma's "Bhutan is beautiful" post
    add_like(
        session=session,
        user_id="25561b0d-1bc9-4cab-af84-2720ac05b0d7",
        post_id="695aff27-b529-475d-8403-34f0b61c5836",
    )

    # Dorji likes Sonam's "Heading to Paro" post
    add_like(
        session=session,
        user_id="1a3ced7e-cba2-4e6e-a93f-18a0045713c8",
        post_id="95a8b732-7bca-4c53-941e-6e6546ddc27b",
    )

    # Ugyen likes the "GNH Country" post
    add_like(
        session=session,
        user_id="7ddd121b-ddef-4cfa-b73b-dc4ca9c39858",
        post_id="bdad3cd5-6ab2-4588-8737-2bc05661836b",
    )
    # Tenzin likes Pema's post "Ema Datshi time"
    add_like(
        session=session,
        user_id="18b53de2-4888-4c3c-9421-f578b754fd57",
        post_id="39050ed2-c682-423b-8653-5115c635d86d",
    )

    # Sangay likes Sonam's post "Hello, Paro"
    add_like(
        session=session,
        user_id="2330a0a5-75b0-4f00-8a79-63dba67afe02",
        post_id="4588698d-b7c5-44a7-bb4a-718fc6a08a00",
    )

    # Pema (the other Pema) likes Karma's post "Its GNH Country"
    add_like(
        session=session,
        user_id="d4026a9d-34d1-4630-9e78-d79e0bfc7669",
        post_id="bdad3cd5-6ab2-4588-8737-2bc05661836b",
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
    users = get_user_like_post(session=session, post_id=post_id)
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
    display_user_like_post(post_id="95a8b732-7bca-4c53-941e-6e6546ddc27b")
