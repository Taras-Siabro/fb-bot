from db import engine, Base
from models import Group

print("Создаю таблицы...")
Base.metadata.create_all(bind=engine)
print("Готово!")