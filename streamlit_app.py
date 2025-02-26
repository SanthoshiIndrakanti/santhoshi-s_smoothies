# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("🥤Order smoothie🥤")
st.write(f"""Choose the fruits you want in your custom Smoothie!""")


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe,max_selections=5)

if ingredients_list:
    # Convert list to comma-separated string
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        if ingredients_string:  # Add a comma only if it's not the first item
            ingredients_string += ', '
        ingredients_string += fruit_chosen

    # Correcting SQL Insert Statement (Ensure column order is correct)
    my_insert_stmt = """INSERT INTO smoothies.public.orders (name_on_order, ingredients)
                        VALUES ('""" + name_on_order + """', '""" + ingredients_string + """')"""

    # Button to submit order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
