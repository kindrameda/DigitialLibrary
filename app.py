import psycopg2
import streamlit as st
import random
import ast
from dotenv import load_dotenv
import os

load_dotenv()
def connect_database():
   con = psycopg2.connect(
      # database = os.getenv("database"),
      # user = os.getenv("user"),
      # password = os.getenv("password"),
      # host = os.getenv("host"),
      # port = os.getenv("port")
      # os.getenv('uri')
      st.secrets["connection"]["uri"]
   )
   return con

con = connect_database()
cursor = con.cursor()
create_query = '''
   create table if not exists book(
      title varchar(500),
      author varchar(500),
      pages int,
      status varchar(500),
      format varchar(500),
      series_name varchar(500),
      series_number int
   );'''
cursor.execute(create_query)
con.commit()

def read_file(file_path):
   with open (file_path, 'r') as f:
      content = f.read()
      book_dict = ast.literal_eval(content)
      return book_dict

def insert_data(title, author, pages, status, format, series_name, series_number):
   con = connect_database()
   cursor = con.cursor()
   query = '''
   insert into book(title, author, pages, status, format, series_name, series_number)
   values(%s, %s, %s, %s, %s, %s, %s);
   '''
   cursor.execute(query,(title, author, pages, status, format, series_name, series_number))
   con.commit()
   cursor.close()
   con.close()

# def add_new_column(column_name, column_type):
#    con = connect_database()
#    cursor = con.cursor()
#    query = f'''alter table book add column {column_name} {column_type}; '''
#    cursor.execute(query)
#    con.commit()
#    cursor.close()
#    con.close()

def drop_table():
   con = connect_database()
   cursor = con.cursor()
   query = '''drop table if exists book;
   '''
   cursor.execute(query)
   con.commit()
   cursor.close()
   con.close()
   
# drop_table()

file_path = "library.txt"
book_dict = read_file(file_path)

for title, details in book_dict.items():
   author = details['author']
   pages = details['pages']
   status = details['status']
   format = details['format']
   series_name = details['series_name']
   series_number = details['series_number']
   #insert_data(title, author, pages, status, format, series_name, series_number)

