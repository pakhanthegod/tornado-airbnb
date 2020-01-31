from handlers import HouseDetailHandler, HouseListHandler, UserListHandler
from daos import HouseDAO, UserDAO


urls = [
    (r'/houses', HouseListHandler, {'DAO': HouseDAO}),
    (r'/houses/(?P<id>\w+)', HouseDetailHandler, {'DAO': HouseDAO}),
    (r'/users', UserListHandler, {'DAO': UserDAO}),
]
