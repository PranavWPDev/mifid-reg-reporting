# import datetime
# from sqlalchemy import (
#     create_engine,
#     Column,
#     String,
#     Float,
#     Integer,
#     DateTime,
#     Text,
#     Boolean,
# )
# from sqlalchemy.orm import declarative_base, sessionmaker

# from config import get_settings

# settings = get_settings()

# engine = create_engine(f"sqlite:///{settings.sqlite_path}")
# Base = declarative_base()
# SessionLocal = sessionmaker(bind=engine)


# class TradeRaw(Base):
#     __tablename__ = "trade_raw"
#     id = Column(Integer, primary_key=True)
#     run_id = Column(String, index=True)
#     trade_id = Column(String, index=True)
#     raw_json = Column(Text)
#     ingested_at = Column(DateTime, default=datetime.datetime.utcnow)


# class TradeEnriched(Base):
#     __tablename__ = "trade_enriched"
#     id = Column(Integer, primary_key=True)
#     run_id = Column(String, index=True)
#     trade_id = Column(String, index=True)
#     enriched_json = Column(Text)
#     enriched_at = Column(DateTime, default=datetime.datetime.utcnow)


# class TradeValidated(Base):
#     __tablename__ = "trade_validated"
#     id = Column(Integer, primary_key=True)
#     run_id = Column(String, index=True)
#     trade_id = Column(String, index=True)
#     validated_json = Column(Text)
#     passed = Column(Boolean, default=False)
#     validated_at = Column(DateTime, default=datetime.datetime.utcnow)


# class ExceptionRecord(Base):
#     __tablename__ = "exceptions"
#     id = Column(Integer, primary_key=True)
#     run_id = Column(String, index=True)
#     trade_id = Column(String, index=True)
#     field = Column(String)
#     category = Column(String)
#     severity = Column(String)
#     description = Column(Text)
#     status = Column(String, default="OPEN")


# class CorrectionRecord(Base):
#     __tablename__ = "corrections"
#     id = Column(Integer, primary_key=True)
#     run_id = Column(String, index=True)
#     trade_id = Column(String, index=True)
#     field = Column(String)
#     original_value = Column(String)
#     proposed_value = Column(String)
#     confidence = Column(Float, default=0.0)
#     applied = Column(Boolean, default=False)
#     reasoning = Column(Text)


# class HitlQueue(Base):
#     __tablename__ = "hitl_queue"
#     id = Column(Integer, primary_key=True)
#     run_id = Column(String, index=True)
#     trade_id = Column(String, index=True)
#     exception_id = Column(Integer)
#     proposed_value = Column(String)
#     reasoning = Column(Text)
#     status = Column(String, default="PENDING")
#     reviewer_decision = Column(String, nullable=True)


# class AuditLog(Base):
#     __tablename__ = "audit_log"
#     id = Column(Integer, primary_key=True)
#     run_id = Column(String, index=True)
#     trade_id = Column(String, index=True)
#     agent = Column(String)
#     action = Column(String)
#     detail = Column(Text)
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)


# class RunMetadata(Base):
#     __tablename__ = "run_metadata"
#     id = Column(Integer, primary_key=True)
#     run_id = Column(String, index=True)
#     source_file = Column(String, nullable=True)
#     total_trades = Column(Integer, default=0)
#     exceptions_count = Column(Integer, default=0)
#     auto_corrected = Column(Integer, default=0)
#     hitl_count = Column(Integer, default=0)
#     status = Column(String, default="start")
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)


# def init_db():
#     Base.metadata.create_all(engine)
#     print(f"✅ SQLite DB initialized at {settings.sqlite_path}")

import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    Integer,
    DateTime,
    Text,
    Boolean,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from config import get_settings

settings = get_settings()

engine = create_engine(f"sqlite:///{settings.sqlite_path}")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


# =========================================================
# 🔥 MULTI-CHANNEL BUFFER TABLE
# =========================================================
class TradeBuffer(Base):
    __tablename__ = "trade_buffer"

    id = Column(Integer, primary_key=True)

    trade_id = Column(String, index=True)
    batch_id = Column(String, index=True)

    source_channel = Column(String)   # ui / rest / pubsub / gcs / scheduler / db
    source_system = Column(String)
    source_ref = Column(String)

    trace_id = Column(String, index=True)

    payload = Column(Text)

    # RECEIVED → MOVED → PROCESSED
    status = Column(String, default="RECEIVED")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# =========================================================
# 🔥 NEW: PIPELINE QUEUE (CRITICAL)
# =========================================================
class PipelineQueue(Base):
    __tablename__ = "pipeline_queue"

    id = Column(Integer, primary_key=True)

    trade_id = Column(String, index=True)
    run_id = Column(String, index=True)

    source_channel = Column(String)

    payload = Column(Text)

    # READY → PROCESSING → DONE
    status = Column(String, default="READY")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# =========================================================
# EXISTING TABLES
# =========================================================

class TradeRaw(Base):
    __tablename__ = "trade_raw"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    trade_id = Column(String, index=True)
    raw_json = Column(Text)
    ingested_at = Column(DateTime, default=datetime.datetime.utcnow)


class TradeEnriched(Base):
    __tablename__ = "trade_enriched"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    trade_id = Column(String, index=True)
    enriched_json = Column(Text)
    enriched_at = Column(DateTime, default=datetime.datetime.utcnow)


class TradeValidated(Base):
    __tablename__ = "trade_validated"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    trade_id = Column(String, index=True)
    validated_json = Column(Text)
    passed = Column(Boolean, default=False)
    validated_at = Column(DateTime, default=datetime.datetime.utcnow)


class ExceptionRecord(Base):
    __tablename__ = "exceptions"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    trade_id = Column(String, index=True)
    field = Column(String)
    category = Column(String)
    severity = Column(String)
    description = Column(Text)
    status = Column(String, default="OPEN")


class CorrectionRecord(Base):
    __tablename__ = "corrections"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    trade_id = Column(String, index=True)
    field = Column(String)
    original_value = Column(String)
    proposed_value = Column(String)
    confidence = Column(Float, default=0.0)
    applied = Column(Boolean, default=False)
    reasoning = Column(Text)


class HitlQueue(Base):
    __tablename__ = "hitl_queue"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    trade_id = Column(String, index=True)
    exception_id = Column(Integer)
    proposed_value = Column(String)
    reasoning = Column(Text)
    status = Column(String, default="PENDING")
    reviewer_decision = Column(String, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    trade_id = Column(String, index=True)
    agent = Column(String)
    action = Column(String)
    detail = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class RunMetadata(Base):
    __tablename__ = "run_metadata"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    source_file = Column(String, nullable=True)
    total_trades = Column(Integer, default=0)
    exceptions_count = Column(Integer, default=0)
    auto_corrected = Column(Integer, default=0)
    hitl_count = Column(Integer, default=0)
    status = Column(String, default="start")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# =========================================================
# INIT DB
# =========================================================
def init_db():
    Base.metadata.create_all(engine)
    print(f"✅ SQLite DB initialized at {settings.sqlite_path}")