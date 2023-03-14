import streamlit
import pandas as pd
import requests as rq
import snowflake.connector

streamlit.title('Bert\'s Kitchen')
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


# fruit advice section 
streamlit.header('Fruit Advice! 🍌🍍🍎')
fruit_choice = streamlit.text_input("What fruit would you like more info about?",'Kiwi')
streamlit.write('The user entered', fruit_choice)

# fruityvice API response
fruityvice_response = rq.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")

# normalise json 
fruityvice_norm = pd.json_normalize(fruityvice_response.json())

# display table
streamlit.dataframe(fruityvice_norm)

# fetch snowflake data
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)



