# Import python packages
import streamlit as st # for streamlit func
# for snowpark column fucntion "col"
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":banana: Customize Your Smoothie! :strawberry:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# creates the text box for name input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# selects the table imported
# selects the fruit name column specifically
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# creates a choice list with the objects in my_dataframe
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections = 5
)



# if statement only runs if not null
if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    # creates the value for the sql 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values (' """ + ingredients_string + """', '""" +name_on_order+ """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    
    # creates a value to store a flag when an order is complete
    time_to_insert = st.button('Submit Order')

    # saves the selected objects to a table called orders
    # if statement only has it run when the time_to_insert
    # variable is not null
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

# New section to display fruityvice nutrition information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)
