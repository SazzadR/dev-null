import shutil
import uuid
from pathlib import Path
from typing import List, Annotated

from fastapi import FastAPI, HTTPException, Request, status, Depends, APIRouter, UploadFile, File
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import session
from sqlalchemy.orm import Session, joinedload, load_only

from database import get_db
from models import User, Post
from schemas import (
    ErrorResponse400,
    ErrorResponse404,
    PostCreate,
    PostResponse,
    UserCreate,
    UserResponse, EmptyResponse, UserProfilePicture, UserUpdate, PostUpdate,
)

SessionDependency = Annotated[Session, Depends(get_db)]
app = FastAPI()
router = APIRouter()

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


@app.get("/", include_in_schema=False)
def home_view(request: Request, session: SessionDependency):
    posts = session.execute(
        select(Post)
        .options(
            load_only(Post.id, Post.title, Post.content, Post.date_posted)
            .joinedload(Post.author)
            .load_only(User.id, User.username, User.email)
        )
        .order_by(Post.id.desc())
    ).scalars()

    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@app.get("/posts/{post_id}", include_in_schema=False)
def post_get_view(request: Request, post_id: int, session: SessionDependency):
    post = session.execute(
        select(Post)
        .options(
            load_only(Post.id, Post.title, Post.content, Post.date_posted)
            .joinedload(Post.author)
            .load_only(User.id, User.username, User.email)
        )
        .where(Post.id == post_id)
    ).scalar()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    title = post.title[:20]
    return templates.TemplateResponse(
        request, "post.html", {"post": post, "title": title}
    )


@app.get("/users/{user_id}/posts", include_in_schema=False)
def user_post_list_view(request: Request, user_id: int, session: SessionDependency):
    user = session.execute(
        select(User.id, User.username).where(User.id == user_id)
    ).scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    posts = session.execute(
        select(Post)
        .options(
            load_only(Post.id, Post.title, Post.content, Post.date_posted)
            .joinedload(Post.author)
            .load_only(User.id, User.username, User.email)
        )
        .where(Post.user_id == user_id)
    ).scalars()

    return templates.TemplateResponse(
        request, "user_posts.html", {"user": user, "posts": posts, "title": ""}
    )


@router.post("/api/users/profile-picture", response_model=UserProfilePicture, tags=["users"])
def user_profile_picture_create_api_view(file: UploadFile = File()):
    try:
        new_file_name = f"{uuid.uuid4().hex}.{file.filename.split(".")[-1]}"
        new_file_path = f"profile_pics/{new_file_name}"
        destination = Path(f"media/{new_file_path}")
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    return {"file_path": new_file_path}


@router.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse400}},
    tags=["users"],
)
def user_create_api_view(user: UserCreate, session: SessionDependency):
    exists = session.scalar(
        select(
            select(User.id)
            .where(or_(User.username == user.username, User.email == user.email))
            .exists()
        )
    )
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username or email already exists",
        )

    new_user = User(
        username=user.username,
        email=user.email,
        profile_picture=user.profile_picture_path,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.get(
    "/api/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse404}},
    tags=["users"],
)
def user_get_api_view(user_id: int, session: SessionDependency):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


@router.patch(
    "/api/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse404}},
    tags=["users"],
)
def user_update_api_view(user_id: int, user_request: UserUpdate, session: SessionDependency):
    user = session.execute(select(User).where(User.id == user_id)).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if user_request.username:
        exists = session.scalar(
            select(
                select(User.id)
                .where(and_(User.username == user_request.username, User.id != user_id))
                .exists()
            )
        )
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists.")
        user.username = user_request.username

    if user_request.profile_picture_path:
        user.profile_picture = user_request.profile_picture_path

    session.commit()
    session.refresh(user)
    return user


@router.delete(
    "/api/users/{user_id}",
    response_model=EmptyResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse404}},
    tags=["users"],
)
def user_delete_api_view(user_id: int, session: SessionDependency):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    session.delete(user)
    session.commit()

    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/api/users/{user_id}/posts",
    response_model=List[PostResponse],
    responses={404: {"model": ErrorResponse404}},
    tags=["users"],
)
def user_post_list_api_view(user_id: int, session: SessionDependency):
    user = session.execute(
        select(User.id, User.username).where(User.id == user_id)
    ).scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    posts = session.execute(
        select(Post)
        .options(
            load_only(Post.id, Post.title, Post.content, Post.date_posted)
            .joinedload(Post.author)
            .load_only(User.id, User.username, User.email)
        )
        .where(Post.user_id == user_id)
    ).scalars()

    return posts


@router.post(
    "/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED, tags=["posts"]
)
def post_create_api_view(post: PostCreate, session: SessionDependency):
    # TODO: Set the first user for now. Later replace with authenticated user.
    user = session.scalar(select(User).order_by(User.id.desc()).limit(1))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found."
        )

    new_post = Post(
        title=post.title,
        content=post.content,
        user_id=user.id,
    )
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post


@router.get("/api/posts", response_model=List[PostResponse], tags=["posts"])
def post_list_api_view(session: SessionDependency):
    posts = (
        session.execute(
            select(Post).options(
                load_only(Post.id, Post.title, Post.content, Post.date_posted),
                joinedload(Post.author).load_only(User.id, User.username, User.email),
            )
        )
        .scalars()
        .all()
    )

    return posts


@router.get(
    "/api/posts/{post_id}",
    response_model=PostResponse,
    responses={404: {"model": ErrorResponse404}},
    tags=["posts"],
)
def post_get_api_view(post_id: int, session: SessionDependency):
    post = session.execute(
        select(Post)
        .options(
            load_only(Post.id, Post.title, Post.content, Post.date_posted)
            .joinedload(Post.author)
            .load_only(User.id, User.username, User.email)
        )
        .where(Post.id == post_id)
    ).scalar()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    return post


@router.patch(
    "/api/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse404}},
    tags=["posts"],
)
def post_update_api_view(post_id: int, post_request: PostUpdate, session: SessionDependency):
    post = session.execute(select(Post).where(Post.id == post_id)).scalar()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if post_request.title:
        post.title = post_request.title

    if post_request.content:
        post.content = post_request.content

    session.commit()
    session.refresh(post)
    return post


@router.delete(
    "/api/posts/{post_id}",
    response_model=EmptyResponse,
    responses={404: {"model": ErrorResponse404}},
    tags=["posts"],
)
def post_delete_api_view(post_id: int, session: SessionDependency):
    post = session.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    session.delete(post)
    session.commit()

    return Response(status_code=status.HTTP_200_OK)


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
