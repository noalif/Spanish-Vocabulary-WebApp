import streamlit as st
import pandas as pd
import base64


class Vocabulary:
    def __init__(self):
        # Read the CSV file into a DataFrame
        self.vocabulary_df = pd.read_csv("common_spanish_words.csv", header=None, names=["Spanish", "English"])

def advanced_radio(options, default=None):
    selected_option = st.sidebar.radio("How do you want to practice today?", options,
                               index=options.index(default) if default else None)
    return selected_option


def show_1_language(vocabulary, language, vocabulary_len):

    if st.button(label='next word'):
        if st.session_state.word_num == (vocabulary_len - 1):
            st.session_state.word_num = (vocabulary_len - 1)
        else:
            st.session_state.word_num += 1


    if st.button(label='prev word'):
        if st.session_state.word_num == 0:
            st.session_state.word_num = 0
        else:
            st.session_state.word_num -= 1

    if st.button(label='start over'):
        st.session_state.word_num = 0

    word_num = st.session_state.word_num
    curr_word = vocabulary[language].iloc[[word_num]]
    st.write(curr_word)


def add_background(image_file):
    """
    :param image_file: backround
    :return:
    """
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


def flashcards(vocabulary_df, vocabulary_len):

    if 'word_num' not in st.session_state:
        st.session_state.word_num = 0

    st.write("- Pick a language and read some of the words \n"
             "- Then, try to translate them to the other language \n"
             "- After you finished, select the other language to see the results")
    lang = st.radio('which language do you want to see?', ['Spanish', 'English'])

    if lang == 'Spanish':
        show_1_language(vocabulary_df, 'Spanish', vocabulary_len)

    elif lang == 'English':
        show_1_language(vocabulary_df, 'English', vocabulary_len)


def memory_tips():
    st.markdown("#### Before practicing, here are some tricks to improve your memory:")
    with open('memory_tips.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    st.markdown(text, unsafe_allow_html=True)


def main():
    add_background('pic_1.jpg')
    st.title("Momento School - Practice Time :)")

    sidebar_options = ["Memory cheat sheet", "Flashcards", "Full Vocabulary", ]
    selected_option = advanced_radio(sidebar_options, default="Memory cheat sheet")

    vocabulary = Vocabulary()
    vocabulary_df = vocabulary.vocabulary_df
    vocabulary_len = len(vocabulary_df)

    if selected_option == "Memory cheat sheet":
        memory_tips()

    elif selected_option == "Flashcards":
        flashcards(vocabulary_df, vocabulary_len)

    elif selected_option == "Full Vocabulary":
        st.dataframe(vocabulary_df)


if __name__ == "__main__":
    main()