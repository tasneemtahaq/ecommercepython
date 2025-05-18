from src.database import Base, engine

def migrate():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Database migrated successfully!")

if __name__ == "__main__":
    migrate()