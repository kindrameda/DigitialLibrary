import streamlit as st
st.title('Kindra\'s Library 📚')
st.write('This is a test, text can go here')
st.markdown('''**something**''')
name = st.text_input('your name: ')
age = st.slider('enter your age: ', min_value = 10, max_value = 100)
st.button('hello')
if st.button('click me'): 
    st.warning('button is not clicked')
st.table({'Name': ['Kindra', 'Urvashi'], 'Age': [35, 35]})
st.number_input('Enter a number:')
st.checkbox('Car')
options = ['apple', 'pineapple', 'mango']
st.selectbox('choose a fruit ', options)
st.image('https://imgs.search.brave.com/vHPuV95_jD7DhVMFw0DcZFJgOY8fWmDYZkCGwCG26wY/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/cG9rZW1vbmRiLm5l/dC9zcHJpdGVzL2hv/bWUvbm9ybWFsLzJ4/L3Bpa2FjaHUuanBn')
st.video('https://youtu.be/amgPXKrFZVg?si=4b455LxJYEFxBKxK')
st.audio('https://music.apple.com/us/album/wake/590427297?i=590427304')
