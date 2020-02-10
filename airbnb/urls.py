from handlers import (
    HouseDetailHandler,
    HouseListHandler,
    UserListHandler,
    UserDetailHandler,
)
from daos import HouseDAO, UserDAO, AiopgService


urls = [
    (r'/houses', HouseListHandler, {'DAO': HouseDAO, 'database': AiopgService}),
    (r'/houses/(?P<_id>\w+)', HouseDetailHandler, {'DAO': HouseDAO, 'database': AiopgService}),
    (r'/users', UserListHandler, {'DAO': UserDAO, 'database': AiopgService}),
    (r'/users/(?P<_id>\w+)', UserDetailHandler, {'DAO': UserDAO, 'database': AiopgService}),
]
