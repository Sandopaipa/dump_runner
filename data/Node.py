from sqlalchemy import create_engine, \
    Integer, String, Column, Float

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
    node_to_any_number = Column(Integer, default=1)
    multicast_freq = Column(Float, nullable=True)

    dump_file_name = Column(String, nullable=True)


class NodeDataHandler:
    def __init__(
            self,
            default_dump_file_name=None,
            **kwargs
    ):

        self.dump_file_name = default_dump_file_name
        self.data = kwargs

    def _find(self, _obj: Node, session: Session):
        for field, value in self.data.items():
            search_dict = {}
            search_dict[field] = value
            print(search_dict.items())
            try:
                record = session.query(_obj).filter_by(**search_dict).one()
                print(record.id)
                return record
            except NoResultFound:
                continue


    def _create(self, session: Session, _obj: Node):
        if self.data['multicast'] is True:
            self.data['node_to_multicast_number'] = 1
        new_record = _obj(**self.data)
        session.add(new_record)
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

    def _update(self, _obj: Node, session: Session, id: int):
        BASE_KEYS = [
            'mac_addr',
            'subnet_ipvv6',
            'subnet_ipv4',
            'ygg_ipv6'
        ]
        result = {}
        for key, value in self.data.items():
            if str(key) in BASE_KEYS:
                old_value = getattr(_obj, str(key))
                if old_value != value and value is not None:
                    result[key] = value
            else:
                continue

        if self.data['multicast'] is True:
            result['node_to_multicast_number'] = _obj.node_to_multicast_number + 1
        result['node_to_any_number'] = _obj.node_to_any_number + 1

        session.query(_obj).filter(_obj.id == id).update(result)
        session.commit()


    def touch(self):

        session = Session(bind=engine)
        try:
            """
            Надо сделать так, чтобы поиск шел только по тем значениям, которые не 
            None.
            """
            node = self._find(_obj=Node, session=session)
            if node is None:
                self._create(session=session, _obj=Node)
            else:
                self._update(_obj=Node, session=session, id=node.id)
        except MultipleResultsFound:
            print("Ошибка: по имеющимся данным, найдено больше одного узла")

        except NoResultFound:
            print("Найден новый узлел")
            self._create(session=session)

        session.close()
