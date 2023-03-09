import streamlit
import pandas as pd

streamlit.title('Recipes')
streamlit.header('Breakfast Menu')
streamlit.text('🫐Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚Hard-Boiled Free-Range Egg')
streamlit.text('🥑Avocado toast')

fruit_list_df = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_list_df.set_index('Fruit', inplace= True)

# picklist
fruit_selection = streamlit.multiselect("Pick some fruits:", list(fruit_list_df.index), ['Avocado', 'Strawberries'])
fruit_filter = fruit_list_df.loc[fruit_selection]

# display the table
streamlit.dataframe(fruit_filter)


