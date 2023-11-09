"""
Создание заданной модели данных в БД.
"""

from data.Node import *

session = Session(bind=engine)
Base.metadata.create_all(engine)