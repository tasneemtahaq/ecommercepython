from src.database import Base, engine

print("Creating database tables...")
Base.metadata.create_all(engine)
print("Database initialized successfully!")