import contextlib
import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import get_config

_DATABASE_PATH = get_config("database", "path")

engine = create_engine(
    f"sqlite:///{_DATABASE_PATH}",
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
)

Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()  # typing: ignore[valid-type]


class BaseMixin(object):
    """model的基类,所有model都必须继承"""

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        index=True,
    )
    deleted_at = Column(DateTime)  # 可以为空, 如果非空, 则为软删


class HouseInfo(Base, BaseMixin):  # type: ignore[misc, valid-type]
    """房产信息数据模型"""

    __tablename__ = "house_info"
    key = Column(Integer, nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    location = Column(String(32), nullable=False)
    total_floor = Column(Integer, nullable=False)
    at_floor = Column(String(4), nullable=False)
    year = Column(Integer, nullable=False)
    layout = Column(String(8), nullable=False)
    area = Column(Float, nullable=False)
    direction = Column(String(2), nullable=False)
    follower = Column(Integer, nullable=False)
    upload_time = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    history = Column(String(1024), default="{}")
    status = Column(Integer, default=0)  # 0表示在售，1表示已下架
    url = Column(String(255), nullable=False)


Base.metadata.create_all(engine)


@contextlib.contextmanager
def get_session():
    s = Session()
    try:
        yield s
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()
