import psycopg2
import streamlit as st
import random
import ast

def connect_database():
   con = psycopg2.connect(
      database = "VirtualLibrary",
      user = "postgres",
      password = "kinhan33",
      host = "localhost",
      port = "5432"
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
      series varchar(500)
   );'''
cursor.execute(create_query)
con.commit()

def read_file(file_path):
   with open (file_path, 'r') as f:
      content = f.read()
      book_dict = ast.literal_eval(content)
      return book_dict

def insert_data(title, author, pages, status, format, series):
   con = connect_database()
   cursor = con.cursor()
   query = '''
   insert into book(Title, Author, Pages, Status, Format, Series)
   values(%s, %s, %s, %s, %s, %s);
   '''
   cursor.execute(query,(title, author, pages, status, format, series))
   con.commit()
   cursor.close()
   con.close()


file_path = "library.txt"
book_dict = read_file(file_path)

for title, details in book_dict.items():
   author = details['author']
   pages = details['pages']
   status = details['status']
   format = details['format']
   series = details['series']
   insert_data(title, author, pages, status, format, series)

