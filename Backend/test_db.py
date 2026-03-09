from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql://tender_user:123456@localhost:5432/tender_ai"

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("Kết nối thành công")
        print(result.scalar())
except OperationalError as e:
    print("Kết nối thất bại:")
    print(e)