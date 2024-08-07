# Import python packages
import streamlit as st # for streamlit func
# for snowpark column fucntion "col"
from snowflake.snowpark.functions import col
import requests
import pandas as pd

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the Snowpark dataframe to a pandas dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

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

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ',search_on, '.')
        
        # displays the info for fruit nutriton from fruity vice
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)
        

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




