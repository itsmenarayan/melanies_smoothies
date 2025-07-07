# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose fruit you want to make custom smoothie!""")

name_on_order = st.text_input("Name on your Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# session = get_active_session()
cnx = st.connection("snowflack")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = f"""
INSERT INTO smoothies.public.orders (name_on_order, ingredients)
VALUES ('{name_on_order}', '{ingredients_string.strip()}')
"""

    st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Button')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
