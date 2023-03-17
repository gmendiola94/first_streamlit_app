import streamlit
import pandas as pd
import requests as rq
import snowflake.connector
from urllib.error import URLError
from PIL import Image

streamlit.title("Bert's Kitchen")
image = Image.open('img/bert.png')
streamlit.image(image, caption='Hi, I\'m Bert')

streamlit.header("Breakfast Menu")
streamlit.text("🫐Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗Kale, Spinach & Rocket Smoothie")
streamlit.text("🥚Hard-Boiled Free-Range Egg")
streamlit.text("🥑Avocado toast")

fruit_list_df = pd.read_csv(
    "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
)
fruit_list_df.set_index("Fruit", inplace=True)

# picklist
fruit_selection = streamlit.multiselect(
    "Pick some fruits:", list(fruit_list_df.index), ["Avocado", "Strawberries"]
)
fruit_filter = fruit_list_df.loc[fruit_selection]

# display the table
streamlit.dataframe(fruit_filter)


# fruit advice (section)
def get_fruit_info(fruit_selected):
    fruityvice_response = rq.get(f"https://fruityvice.com/api/fruit/{fruit_selected}")
    fruityvice_norm = pd.json_normalize(fruityvice_response.json())
    return fruityvice_norm


streamlit.header("Fruit Advice! 🍌🍍🍎")
try:
    fruit_choice = streamlit.text_input("What fruit would you like more info about?")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        function_response = get_fruit_info(fruit_choice)
        streamlit.dataframe(function_response)

except URLError as e:
    streamlit.error()


# fetch snowflake fruit list (section)
streamlit.header("View Our Fruit List - Add Your Favorites!")


def get_fruit_list():
    with cnx.cursor() as cur:
        cur.execute("select * from fruit_load_list")
        return cur.fetchall()


if streamlit.button("Get Fruit List"):
    cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_list()
    cnx.close()
    streamlit.dataframe(my_data_rows)

# add new fruit to list
add_my_fruit = streamlit.text_input("What fruit would you like to add?")


def insert_new_fruit_snowflake(new_fruit):
    with cnx.cursor() as cur:
        cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
        return "Thanks for adding: " + new_fruit


if streamlit.button("Add fruit"):
    cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    function_response = insert_new_fruit_snowflake(add_my_fruit)
    cnx.close()
    streamlit.text(function_response)
