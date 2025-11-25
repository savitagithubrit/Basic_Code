import pandas as pd
from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.orm import sessionmaker
from .db_conn import Base, engine, SessionLocal
from database import df_flipkart, df_amazon   # already loaded in database.py


# -------------------------------------------------------
# ORM MODELS
# -------------------------------------------------------

class Flipkart(Base):
    __tablename__ = 'flipkart_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255))
    price = Column(Float)
    rating = Column(Float)


class Amazon(Base):
    __tablename__ = 'amazon_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255))
    price = Column(Float)
    rating = Column(Float)

class Users(Base):
    _tablename_ = "users"    


# -------------------------------------------------------
# CREATE TABLES
# -------------------------------------------------------

Base.metadata.drop_all(engine)     # remove old wrong tables
Base.metadata.create_all(engine)
print("✔ Tables recreated successfully")


session = SessionLocal()


# -------------------------------------------------------
# INSERT FLIPKART DATA
# -------------------------------------------------------

df_flipkart.columns = df_flipkart.columns.str.strip()

df_flipkart.rename(
    columns={
        "Price (₹)": "Price",
        "rating": "Rating"
    },
    inplace=True
)

for _, row in df_flipkart.iterrows():
    session.add(
        Flipkart(
            product_name=str(row["Product Name"]),
            price=float(row["Price"]),
            rating=float(row["Rating"])
        )
    )

print("✔ Flipkart data inserted!")


# -------------------------------------------------------
# INSERT AMAZON DATA
# -------------------------------------------------------

df_amazon.columns = df_amazon.columns.str.strip()

df_amazon.rename(
    columns={
        "Price (₹)": "Price",
        "rating": "Rating"
    },
    inplace=True
)

for _, row in df_amazon.iterrows():
    session.add(
        Amazon(
            product_name=str(row["Product Name"]),
            price=float(row["Price"]),
            rating=float(row["Rating"])
        )
    )

print("✔ Amazon data inserted!")


# -------------------------------------------------------
# COMMIT + CLOSE
# -------------------------------------------------------

session.commit()
session.close()

print(" All data inserted successfully!")
