from sqlalchemy import create_engine, \
    Integer, String, Column

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}", echo=False)
session = sessionmaker(bind=engine)

Base = declarative_base()


class Node(Base):
    """
    Класс, имплементирующий модель узла в БД.
    """
    __tablename__ = 'nodes'  # Название таблицы
    id = Column(Integer, primary_key=True)  # Идентификатор узла (записи в БД)
    """Параметры, собираемые из дампов"""
    mac_addr = Column(String, nullable=True)  # MAC-адрес узла
    subnet_ipv6 = Column(String, nullable=True)  # IPv6 адрес узла в подсети
    ygg_ipv6 = Column(String, nullable=True)  # IPv6 адрес узла в сети Yggdrasil
    """Вычисляемые параметры"""
    node_to_multicast_number = Column(Integer, default=0)  # Число произведенных мультиадресных рассылок
    node_to_any_number = Column(Integer, default=1)  # Общее число исходящих пакетов
    """Вспомогательные поля"""
    dump_file_name = Column(String, nullable=True)  # Имя файла. Для поиска узлов при работе с несколькими файлами


class NodeDataHandler:
    """
    Класс для работы с определенной в базе данных моделью.
    """
    def __init__(
            self,
            default_dump_file_name=None,
            **kwargs
    ):

        self.dump_file_name = default_dump_file_name
        self.data = kwargs

        """Ключевые поля для поиска"""
        self.BASE_KEYS = [
            'mac_addr',
            'subnet_ipv6',
            'subnet_ipv4',
            'ygg_ipv6',
            'dump_file_name'
        ]

    def _find(self, _obj: Node, session: Session):
        """
        Внутренний метод для поиска узла по собранным в дампе данным.
        Поиск выполняется только по тем полям, которые не имеют значения None.
        _obj:       экземпляр класса Node - представляет собой запись в базе данных
        session:    экземпляр класса Session для поддержания запросов к БД
        return:     record: Node - запись в таблице базы данных. Экземпляр класса Node.
        """
        search_dict = {}
        search_dict['dump_file_name'] = self.data['dump_file_name']

        for field, value in self.data.items():
            if str(field) in self.BASE_KEYS[:4] and value is not None:
                search_dict[field] = value
                try:
                    record = session.query(_obj).filter_by(**search_dict).one()
                    return record
                except NoResultFound:
                    del search_dict[field]
                except MultipleResultsFound:
                    print('Было найдено несколько узлов')
            else:
                continue

    def _create(self, session: Session, _obj: Node):
        """
        Внутренний метод для создания записи в базе данных.
        _obj:       экземпляр класса Node - представляет собой запись в базе данных
        session:    экземпляр класса Session для поддержания запросов к БД
        """
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

    def _update(self, _obj: Node, session: Session):
        """
        Внутренний метод для обновления записи в БД.
        _obj:       экземпляр класса Node - представляет собой запись в базе данных.
        session:    экземпляр класса Session для поддержания запросов к БД.
        """
        result = {}

        for key, value in self.data.items():
            if str(key) in self.BASE_KEYS and value is not None:
                old_value = getattr(_obj, str(key))
                if old_value is None or old_value != value:
                    result[key] = value
            else:
                continue

        if self.data['multicast'] is True:
            result['node_to_multicast_number'] = int(_obj.node_to_multicast_number) + 1

        result['node_to_any_number'] = int(_obj.node_to_any_number) + 1

        session.query(Node).filter(Node.id == _obj.id).update(result)
        session.commit()

    def touch(self):
        """
        Метод для создания или обновления записи в БД.
        """
        session = Session(bind=engine)
        try:
            node = self._find(_obj=Node, session=session)
            if node is None:
                for field, val in self.data.items():
                    if field in self.BASE_KEYS[:4] and val is not None:
                        self._create(session=session, _obj=Node)
                        break
                    else:
                        continue
            else:
                self._update(_obj=node, session=session)
        except MultipleResultsFound:
            print("Ошибка: по имеющимся данным, найдено больше одного узла")
        except NoResultFound:
            print("Найден новый узлел")
            self._create(session=session)

        session.close()
