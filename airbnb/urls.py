from handlers import (
    HouseDetailHandler,
    HouseListHandler,
    UserListHandler,
    UserDetailHandler,
    OrderListHandler,
    OrderDetailHandler,
)
from daos import HouseDAO, UserDAO, OrderDAO, AiopgService


urls = [
    (r'/houses', HouseListHandler, {'DAO': HouseDAO, 'database': AiopgService}),
    (r'/houses/(?P<_id>\w+)', HouseDetailHandler, {'DAO': HouseDAO, 'database': AiopgService}),
    (r'/users', UserListHandler, {'DAO': UserDAO, 'database': AiopgService}),
    (r'/users/(?P<_id>\w+)', UserDetailHandler, {'DAO': UserDAO, 'database': AiopgService}),
    (r'/orders', OrderListHandler, {'DAO': OrderDAO, 'database': AiopgService}),
    (r'/orders/(?P<_id>\w+)', OrderDetailHandler, {'DAO': OrderDAO, 'database': AiopgService}),
]
