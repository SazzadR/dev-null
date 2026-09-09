from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import PostCreate, PostResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "title": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vulputate nulla neque, in posuere nisl porttitor eu. Nam ultricies accumsan mi, bibendum congue nunc ultrices a. Ut non lorem placerat, convallis dui euismod, efficitur ligula. Sed quis metus eu nulla vehicula efficitur. Etiam egestas iaculis sodales. Interdum et malesuada fames ac ante ipsum primis in faucibus. Cras ultricies faucibus dolor et eleifend. Suspendisse accumsan tellus auctor lorem bibendum, vel ultricies turpis pretium. Pellentesque posuere enim ipsum. Nullam ultrices nibh vitae fermentum maximus. Donec ornare turpis et convallis imperdiet. Nullam molestie nibh nisl, at lacinia quam maximus sed. Quisque fringilla eros vitae ligula blandit, egestas dignissim lacus hendrerit. Sed nec congue elit.",
        "author": "John Doe",
        "date_posted": "September 7, 2026",
    },
    {
        "id": 2,
        "title": "Contrary to popular belief, Lorem Ipsum is not simply random text.",
        "content": "Donec ac nulla eget velit ornare commodo. Aliquam viverra tristique volutpat. Etiam in lacinia enim. Vivamus sit amet tristique dui. Nulla at est eu est porta vestibulum et ut massa. Nullam vulputate vitae erat ac luctus. Vestibulum vitae metus in velit iaculis dignissim. Aenean sapien nibh, blandit sed lacus sit amet, ullamcorper malesuada eros. Duis ante nulla, mollis et eleifend convallis, malesuada in tortor. Vestibulum ut nisl laoreet, accumsan ex eget, pellentesque erat. Suspendisse euismod blandit condimentum.",
        "author": "Jane Doe",
        "date_posted": "September 8, 2026",
    },
]


@app.get("/", include_in_schema=False, name="home")
def home_page(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@app.get("/posts/{post_id}", include_in_schema=False, name="get_post")
def get_post_page(request: Request, post_id: int):
    for post in posts:
        if post["id"] == post_id:
            title = post["title"][:20]
            return templates.TemplateResponse(
                request, "post.html", {"post": post, "title": title}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts", response_model=List[PostResponse])
def get_posts():
    return posts


@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.post(
    "/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
def post_create(post: PostCreate):
    _id = (max(post["id"] for post in posts) + 1) if posts else 1
    post = {
        "id": _id,
        "title": post.title,
        "content": post.content,
        "author": "John Doe",
        "date_posted": date.today().strftime("%B %d, %Y"),
    }
    posts.append(post)

    return post


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
