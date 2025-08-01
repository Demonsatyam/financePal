# import sys
# import os

# # This line ensures that we can import from the 'database' package
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from database.db import Base, engine
# # This import is CRITICAL. It loads your models so that Base knows about them.
# from database import models

# def reset_database():
#     """
#     Drops all tables and recreates them based on the current models.
#     WARNING: This will delete all existing data.
#     """
#     print("--- ⚠️  WARNING: This will delete all data in the database. ⚠️ ---")
#     confirm = input("Are you sure you want to continue? (y/n): ")
#     if confirm.lower() != 'y':
#         print("Database reset cancelled.")
#         return

#     print("Connecting to the database...")
#     print("Dropping all tables...")
#     Base.metadata.drop_all(bind=engine)
#     print("Tables dropped successfully.")

#     print("\nCreating all tables based on current models...")
#     Base.metadata.create_all(bind=engine)
#     print("✅ Tables created successfully.")
#     print("✅ Database reset complete.")

# if __name__ == "__main__":
#     reset_database()