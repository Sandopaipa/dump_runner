from sqlalchemy import create_engine, MetaData, Table, \
    Integer, String, Column, Float, or_

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/stc_db", echo=False)
session = sessionmaker(bind=engine)

Base = declarative_base()


class Node(Base):
    """
    Класс, имплементирующий модель узла в БД.
    """
    """Название таблицы в БД"""
    __tablename__ = 'nodes'
    """Уникальный идентификатор записи"""
    id = Column(Integer, primary_key=True)
    """Параметры, собираемые из дампов"""
    mac_addr = Column(String, nullable=True)
    subnet_ipv4 = Column(String, nullable=True)
    subnet_ipv6 = Column(String, nullable=True)
    ygg_ipv6 = Column(String, nullable=True)
    """Вычисляемые параметры"""
    node_to_multicast_number = Column(Integer, default=0)
    node_to_any_number = Column(Integer, default=0)
    multicast_freq = Column(Float, nullable=True)

    dump_file_name = Column(String, nullable=True)


class NodeDataHandler:
    def __init__(
            self,
            default_mac=None,
            default_subnet_ipv4=None,
            default_subnet_ipv6=None,
            default_ygg_ipv6=None,
            default_multicasting=False,
            default_dump_file_name=None
    ):
        self.mac_addr = default_mac
        self.subnet_ipv4 = default_subnet_ipv4
        self.subnet_ipv6 = default_subnet_ipv6
        self.ygg_ipv6 = default_ygg_ipv6
        self.multicasting = default_multicasting
        self.node_to_any = 0
        self.dump_file_name = default_dump_file_name

    def _create(self, session: Session):
        _multicasting = 0
        if self.multicasting is True:
            _multicasting = 1
        data = Node(
            mac_addr=self.mac_addr,
            subnet_ipv4=self.subnet_ipv4,
            subnet_ipv6=self.subnet_ipv6,
            ygg_ipv6=self.ygg_ipv6,
            node_to_multicast_number=_multicasting,
            node_to_any_number=1,
            dump_file_name=self.dump_file_name
        )
        session.add(data)
        session.commit()

    def _select_attr(self, node: Node, attr: str, value):
        if attr == 'subnet_ipv4':
            node.subnet_ipv4 = value
        elif attr == 'ygg_ipv6':
            node.ygg_ipv6 = value
        elif attr == 'mac_addr':
            node.mac_addr = value
        elif attr == 'subnet_ipv6':
            node.subnet_ipv6 = value
        elif attr == 'node_to_multicast_number':
            node.node_to_multicast_number += value
        elif attr == 'node_to_any_number':
            node.node_to_any_number += 1

    def _update(
            self,
            node: Node,
            session: Session,
            **kwargs
    ):
        for attr, value in vars(node).items():
            new_value = kwargs.get(attr)
            if value != new_value and new_value is not None and attr != 'node_to_multicast_number':
                value = new_value
            elif attr == 'node_to_multicast_number' and self.multicasting is True:
                value = 1
            else:
                continue
#            print(attr)
            self._select_attr(node, attr, value)
        session.add(node)
        session.commit()

    def touch(self):
        session = Session(bind=engine)
        try:
            node = session.query(Node).filter(or_(
                Node.mac_addr == self.mac_addr,
                Node.subnet_ipv4 == self.subnet_ipv4,
                Node.subnet_ipv6 == self.subnet_ipv6,
                Node.ygg_ipv6 == self.ygg_ipv6,
            )).one()
            self._update(
                node,
                session=session,
                mac_addr=self.mac_addr,
                subnet_ipv4=self.subnet_ipv4,
                subnet_ipv6=self.subnet_ipv6,
                ygg_ipv6=self.ygg_ipv6,
                node_to_any_number=self.node_to_any
            )
        except MultipleResultsFound:
            print("Ошибка: по имеющимся данным, найдено больше одного узла")

        except NoResultFound:
            print("Найден новый узлел")
            self._create(session=session)

        session.close()
