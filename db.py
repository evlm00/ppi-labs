from schemas.users import User
from schemas.posts import Post

class DummyDatabase:
    users: dict[int, User] = {}
    posts: dict[int, Post] = {}

db = DummyDatabase()
db.users[0] = { 'id': 0, 'email': 'mee@mail.com' }
db.users[1] = { 'id': 1, 'email': 'you@mail.com' }
