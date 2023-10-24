from Node import *
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from Node import session
from sqlalchemy import or_


session = Session(bind=engine)
Base.metadata.create_all(engine)


"""search_fields = {
    'mac_addr': 'c0-c9-e3-45-72-77',
    'subnet_ipv6': 'fe00::',
    'subnet_ipv4': '0.0.0.0',
    'dictionary': {'a': 'b'}
}


node1 = NodeDataHandler(
    mac_addr='c0-c9-e3-45-72-78',
    subnet_ipv6='fe00::',
    subnet_ipv4='0.0.0.0',
    ygg_ipv6='0200::1',
    multicast=True
)
record = node1.touch()

node1.touch()
node2 = NodeDataHandler(
    default_mac='c0-c9-e3-45-72-77',
    default_subnet_ipv6='fe00::',
    default_multicasting=True
)
node2.touch()
node3 = NodeDataHandler(
    default_mac='c0-c9-e3-45-72-70',
    default_subnet_ipv6='fd80::',
    default_ygg_ipv6='0200::',
    default_subnet_ipv4='0.0.0.0',
    default_multicasting=False
)
node3.touch()
node4 = NodeDataHandler(
    default_ygg_ipv6='03f0::',
    default_mac='c0-c9-e3-45-72-77',
    default_subnet_ipv6='0200::'
)
node4.touch()"""