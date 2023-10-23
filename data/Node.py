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

        self.BASE_KEYS = [
            'mac_addr',
            'subnet_ipv6',
            'subnet_ipv4',
            'ygg_ipv6',
            'dump_file_name'
        ]


    def _find(self, _obj: Node, session: Session):
        search_dict = {}
        search_dict['dump_file_name'] = self.data['dump_file_name']
        for field, value in self.data.items():
            if str(field) in self.BASE_KEYS and value is not None:
                search_dict[field] = value
            else:
                continue
            try:
                print(search_dict)
                record = session.query(_obj).filter_by(**search_dict).one()
                return record
            except NoResultFound:
                continue
            except MultipleResultsFound:
                print('Было найдено несколько узлов')



    def _create(self, session: Session, _obj: Node):
        record = {}

        for field, val in self.data.items():
            if str(field) in self.BASE_KEYS and val is not None:
                record[field] = val
        if self.data['multicast'] is True:
            record['node_to_multicast_number'] = 1
        else:
            del self.data['multicast']
        record['node_to_any_number'] = 1

        new_record = _obj(**record)
        session.add(new_record)
        session.commit()

    def _update(self, _obj: Node, session: Session, multicast_num: int, id: int):
        result = {}
        for key, value in self.data.items():
            if str(key) in self.BASE_KEYS[:4] and value is not None:
                old_value = getattr(_obj, str(key))
                if old_value is None or old_value != value:
                    result[key] = value
            else:
                continue

        if self.data['multicast'] is True:
            result['node_to_multicast_number'] = int(_obj.node_to_multicast_number) + 1

        result['node_to_any_number'] = int(_obj.node_to_any_number) + 1

        session.query(Node).filter(_obj.id == id).update(result)
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
                for field, val in self.data.items():
                    if field in self.BASE_KEYS[:4] and val is not None:
                        self._create(session=session, _obj=Node)
                        break
                    else:
                        continue
            else:
                self._update(_obj=node, session=session, multicast_num=int(node.node_to_multicast_number), id=node.id)
        except MultipleResultsFound:
            print("Ошибка: по имеющимся данным, найдено больше одного узла")

        except NoResultFound:
            print("Найден новый узлел")
            self._create(session=session)

        session.close()
