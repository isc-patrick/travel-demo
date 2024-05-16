import os, pandas as pd
from sentence_transformers import SentenceTransformer
import py_iris_utils.connection as connection
from py_iris_utils.connection import load_config
from loguru import logger

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

CONFIG_PATH = os.environ.get("IRIS_VECTOR_DEMO_CONFIG", "../config/demo_config.json")
config = load_config(CONFIG_PATH) 

iris = connection.IRISConnection(config)

def show_place_count():
    with iris.engine.connect() as conn:
        with conn.begin():
            print("Testing data")
            result = conn.execute(text("Select Count(*) from Place"))
            print(result.fetchall())

# Confirm connection
try:
    iris.engine.connect()
    logger.info("Connected to IRIS")
except Exception as e:
    print("Error connecting to IRIS: ", e)
    exit(-1)

df = pd.read_csv('../data/travel_info1.csv')
df.fillna('', inplace=True)

print("Data loaded now generating embeddings")
# Load a pre-trained sentence transformer model, dime = 384 and create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2') 

embeddings = model.encode(df['general'].tolist(), normalize_embeddings=True)
df['general_vector'] = embeddings.tolist()

# Generate embeddings for todo
embeddings_todo = model.encode(df['todo'].tolist(), normalize_embeddings=True)
df['todo_vector'] = embeddings_todo.tolist()

show_place_count()
# # Try and create table. This amy already exist depending if volumes are mounted
# try:
#     with iris.engine.connect() as conn:
#         with conn.begin():
#             for index, row in df.iterrows():
#                 sql = text("""
#                 CREATE TABLE Place (name varchar(100), general varchar(3641144), todo varchar(3641144), 
#                                     region1 varchar(200),region2 varchar(200), region3 varchar(200),
#                                     todo_vector  VECTOR(DOUBLE, 384), general_vector  VECTOR(DOUBLE, 384)) 
#                 """)
#                 conn.execute(sql)
# except Exception as e:
#     print("Table already exists, truncating data")
try:
    with iris.engine.connect() as conn:
        with conn.begin():
            conn.execute(text("TRUNCATE TABLE Place"))
except Exception as e:
    print(f"Could not truncate - {e}")

# Insert data
print("Starting data load")
with iris.engine.connect() as conn:
    with conn.begin():
        for index, row in df.iterrows():
            sql = text("""
                INSERT INTO Place 
                (name,general,todo,region1,region2,region3, general_vector, todo_vector) 
                VALUES (:name,:general,:todo,:region1,:region2,:region3, TO_VECTOR(:general_vector), TO_VECTOR(:todo_vector))
            """)
            conn.execute(sql, {
                'name': row['place'], 
                'general': row['general'], 
                'todo': row['todo'], 
                'region1': row['region1'], 
                'region2': row['region2'], 
                'region3': row['region3'], 
                'general_vector': str(row['general_vector']),
                'todo_vector': str(row['todo_vector'])
            })

show_place_count();