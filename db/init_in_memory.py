import os
from sqlalchemy import text
from db.in_memory import engine, Base


def init_in_memory_db():
    """
    ✅ Create all tables in in-memory SQLite DB
    """
    Base.metadata.create_all(engine)
    print("✅ In-memory DB tables created")


def seed_from_sql():
    """
    ✅ Load seed.sql and insert data into in-memory DB
    """
    try:
        # 📁 Navigate to backend root
        base_dir = os.path.dirname(os.path.dirname(__file__))

        # 📄 Path to seed.sql
        sql_path = os.path.join(base_dir, "seeds", "seed.sql")

        print(f"📄 Loading SQL from: {sql_path}")

        # 📖 Read SQL file
        with open(sql_path, "r") as f:
            sql = f.read()

        # 🚀 Execute SQL
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()

        print("✅ Seed data inserted successfully")

    except Exception as e:
        print(f"❌ Error seeding DB: {e}")