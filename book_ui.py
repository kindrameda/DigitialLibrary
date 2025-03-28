import streamlit as st
from app import connect_database
import random
from app import insert_data
from utils import formatting_selectbox
from goodreads_scrape import fetch_book_details

con = connect_database()
cursor = con.cursor()

if "finishedbook" not in st.session_state:
    st.session_state.finishedbook = ""
if "submit" not in st.session_state:
    st.session_state.submit = False

st.title("Kindra's Library 📚")

options = ['', 'I finished a book', 'I want to read a book', 'I bought a new book!' ]
action = st.selectbox('What do you want to do?',options, format_func = formatting_selectbox)

st.markdown('''
    <style>
        .col-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 40px; /* Increased space between cards */
        }

        .book-container {
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
            text-align: center;
            width: 300px;
            color: black;
            margin-bottom: 20px;
            flex: 1;
            max-width: 350px;
        }

        .book-container img {
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 5px;
        }
    </style>
''', unsafe_allow_html=True)

if action == 'I finished a book':
    st.session_state.finishedbook = st.text_input(
        "Which book did you finish?", key="book_input"
    )

    if st.button("Submit"):
        booktitle = st.session_state.finishedbook
        if booktitle:
            check_book = '''select * FROM book WHERE title = %s;'''
            cursor.execute(check_book, (booktitle,))
            bookdata = cursor.fetchall()
            if bookdata:
                st.write("Book details found:")
                st.write(bookdata)
                change_status = '''update book set status = 'read' where title = %s'''
                check_status = '''select status from book where title = %s;'''
                cursor.execute(check_status,(booktitle,))
                bookstatus = cursor.fetchall()
                if bookstatus[0][0] == 'read':
                    st.error("You already read this! 🙅🏼‍♀️")
                else:
                    cursor.execute(change_status,(booktitle,))
                    con.commit()
                    st.success(f'You finished {booktitle}, good job!')

            else:
                st.write(f"Not found, would you like to add {booktitle} to your library?")
            
elif action == "I want to read a book":
    read_options = ['', 'Pick a random unread book', 'Looking for something specific?']
    selected_option = st.selectbox('Choose your preference:', read_options, format_func = formatting_selectbox)
    if selected_option == 'Pick a random unread book':
        all_unread_query = '''select title from book where status = 'unread';'''
        cursor.execute(all_unread_query)
        all_unread_books = cursor.fetchall()
        if all_unread_books:
            random_book = random.choice(all_unread_books)
            st.write(random_book[0])
    elif selected_option == 'Looking for something specific?':
        book_options = ['','A short book', 'A long book', 'A physical book', 'An eBook']
        selected_book = st.selectbox('Filter by:', book_options, format_func = formatting_selectbox)
        if selected_book == 'A short book':
            cursor.execute('''select title from Book where pages <= 400 and status = 'unread';''')
        elif selected_book == 'A long book':
            cursor.execute('''select title from Book where pages > 400 and status = 'unread';''')
        elif selected_book == 'A physical book':
            cursor.execute('''select title from Book where (format = 'hardback' or format = 'paperback') and status = 'unread';''')
        elif selected_book == 'An eBook':
            cursor.execute('''select title from Book where format = 'eBook' and status = 'unread';''')
        if selected_book != '':
            all_selected_books = cursor.fetchall()
            all_book_names = []
            for book in all_selected_books:
                all_book_names.append(book[0])
            randomly_picked_book = random.choice(all_book_names)
            st.write(randomly_picked_book)
        
elif action == 'I bought a new book!':
    search_books = ['', 'Manual Entry', 'Goodreads search']
    selected_book = st.selectbox('Search by:', search_books, format_func = formatting_selectbox)
    if selected_book == 'Manual Entry':
        book_title = st.text_input('Enter Book Title: ')
        book_author = st.text_input('Enter Author: ')
        book_pages = st.number_input('Enter pages: ')
        book_status = 'unread'
        book_format = st.text_input('Format: ')
        book_series = st.text_input('Standalone or series?: ')
        if st.button('Submit'):
            insert_data(book_title, book_author, book_pages, book_status, book_format, book_series)
    elif selected_book == 'Goodreads search':
        search_by = st.text_input('Enter ISBN or Title')
        if st.button('Search'):
            if search_by:
                with st.spinner('Searching for books...'):
                    book_details = fetch_book_details(search_by = search_by)
                    if book_details:
                        if search_by.isnumeric():
                            st.write(f'Results for ISBN {search_by}: ')
                        else:
                            st.write(f'Results for title {search_by}: ')
                        
                        for book in book_details:
                            st.markdown(
                                f'''
                                    <div class='book-container'>
                                        <img src='{book['picture'] if book['picture'] else 'https://dryofg8nmyqjw.cloudfront.net/images/no-cover.png'}' alt='book_image'>
                                        <h4>{book['title']}</h4>
                                        <p><strong>Author: </strong>{book['author']}</p>
                                        <p><strong>Pages: </strong>{book['pages']}</p>
                                    </div>
                                ''', unsafe_allow_html=True
                            )