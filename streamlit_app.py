import streamlit
import pandas
import requests
import snowflake.connector


streamlit.header(' Breakfast Menu')
streamlit.text('π₯£ Omega 3 & Blueberry Oatmeal')
streamlit.text('π₯Kale, Spinach & Rocket Smoothie')
streamlit.text('πHard-Boiled Free-Range Egg')
streamlit.text('π₯π avocado tost')
               
streamlit.header('ππ₯­ Build Your Own Fruit Smoothie π₯π')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple','Avocado'])

fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

# User inpute method
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

# take the json of the response and normalize it.
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# show data into a table 
streamlit.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list;")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_rows)
