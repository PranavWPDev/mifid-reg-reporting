# import datetime
# from sqlalchemy import Column, Integer, String, Text, DateTime
# from db.in_memory import Base

# class SourceTrade(Base):
#     __tablename__ = "source_trades"

#     id = Column(Integer, primary_key=True)
#     trade_id = Column(String, unique=True, index=True)
#     payload = Column(Text)

#     source_channel = Column(String)
#     source_label = Column(String)
#     source_ref = Column(String)

#     created_at = Column(DateTime, default=datetime.datetime.utcnow)