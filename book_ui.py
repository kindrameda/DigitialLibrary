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
if "bookstatus" not in st.session_state:
    st.session_state.bookstatus = "unread"
if "booktitle" not in st.session_state:
    st.session_state.booktitle = ""

st.title("Kindra's Library 📚")

options = ['', 'I finished a book', 'I want to read a book', 'I bought a new book!' ]
action = st.selectbox('What do you want to do?',options, format_func = formatting_selectbox)

st.markdown('''
    <style>
        .books-grid {
            display: grid;
            grid-template-columns: repeat(3, 2fr);
            gap: 70px;
            margin-bottom: 40px;
        }

        .book-card {
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            border: 1px solid red;
            background-color: #ffffff;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        .book-card img {
            width: 100%;
            height: 200px;
            object-fit: contain;
            border-radius: 5px;
            margin-bottom: 15px;
        }

        .book-card h4 {
            margin: 10px 0;
            color: #333333;
            font-size: 18px;
        }

        .book-card p {
            margin: 5px 0;
            color: #666666;
            font-size: 14px;
        }
    </style>
''', unsafe_allow_html=True)

if action == 'I finished a book':
    st.session_state.finishedbook = st.text_input(
        "Which book did you finish?", key="book_input"
    )

    if st.button("Submit"):
        st.session_state.bookstatus = 'read'
        booktitle = st.session_state.finishedbook
        st.session_state.booktitle = booktitle
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
    if "bookstatus" in st.session_state and st.session_state.bookstatus == 'read':
        if st.button('Undo'):
            undo_status = '''update book set status = 'unread' where title = %s'''
            cursor.execute(undo_status, (st.session_state.booktitle,))
            con.commit()
            st.success(f"I fixed your mistake!")
            st.session_state.bookstatus = 'unread'
            del st.session_state.bookstatus
            

elif action == "I want to read a book":
    read_options = ['', 'Pick a random unread book', 'Looking for something specific?']
    selected_option = st.selectbox('Choose your preference:', read_options, format_func = formatting_selectbox)
    if selected_option == 'Pick a random unread book':
        all_unread_query = '''select title, series_name, series_number from book where status = 'unread';'''
        #all_unread_query = '''select title, series from book where status = 'unread';'''
        cursor.execute(all_unread_query)
        all_unread_books = cursor.fetchall()
        #print (type (all_unread_books))
        book_dict = {}
        for book_tuple in all_unread_books:
            book_series_key = book_tuple[1]
            if book_series_key in book_dict:
                book_dict[book_series_key].update({book_tuple[0]: book_tuple[2]})
            else:
                book_dict[book_series_key] = {book_tuple[0]: book_tuple[2]}
        all_min_series_books = []

        for book_series_name, book_pair in book_dict.items():
            min_series = float('inf')
            min_pair = (None, None)
            for book_name, book_series_number in book_pair.items():
                if book_series_number < min_series:
                    min_series = book_series_number
                    min_pair = (book_name, book_series_number)
            all_min_series_books.append(min_pair)
      

        if all_unread_books:
            random_book = random.choice(all_min_series_books)
            st.write(random_book)
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
        book_series = st.text_input('standalone or series name?: ')
        book_series_number = st.number_input('Book number? (if standalone, enter 0):')
        if st.button('Submit'):
            try:
                insert_data(book_title, book_author, book_pages, book_status, book_format, book_series, book_series_number)
                st.success(f"{book_title} added successfully!")
            except Exception as e:
                st.error(f"Error adding book: {str(e)}")
                
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
                        
                        for i, book in enumerate(book_details):
                            # Start a new row every 3 books
                            if i % 2 == 0:
                                cols = st.columns(2)
                            
                            with cols[i % 2]:
                                with st.form(key=f"form_{i}"):
                                    st.markdown(
                                        f'''
                                        <div class="book-card">
                                            <img src='{book["picture"] if book["picture"] else "https://dryofg8nmyqjw.cloudfront.net/images/no-cover.png"}' alt='book_image'>
                                            <h4>{book["title"]}</h4>
                                            <p><strong>Author:</strong> {book["author"]}</p>
                                            <p><strong>Pages:</strong> {book["pages"]}</p>
                                            <p><strong> Series Name:</strong> {book["series_name"]}</p>
                                            <p><strong> Series Number:</strong> {book["series_number"]}</p>
                                        </div>
                                        ''', 
                                        unsafe_allow_html=True
                                    )
                                    
                                    book_format = st.selectbox(
                                        'Format:',
                                        ['', 'hardback', 'paperback', 'eBook', 'audio'],
                                        key=f"format_{i}",
                                        format_func=formatting_selectbox
                                    )
                                    
                                    if st.form_submit_button('Add to Library'):
                                        if book_format == '':
                                            st.error("Please choose a book format before adding.")
                                        else:
                                            try:
                                                success = insert_data(
                                                    title=book['title'],
                                                    author=book['author'],
                                                    status='unread',
                                                    pages=int(book['pages']) if book['pages'] else 0,
                                                    format=book_format,
                                                    series_name=book['series_name'],
                                                    series_number = book['series_number']
                                                )
                                                if success:
                                                    st.success(f'{book["title"]} added to your Library!')
                                            except Exception as e:
                                                st.error(f"Error adding book: {e}")