# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Helpful documentation links
helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("🥤 Order Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

# User input for smoothie order
name_on_order = st.text_input("Enter your name for the order:")
st.write(f"The name on your Smoothie will be: **{name_on_order}**")

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch available fruit options from Snowflake
fruit_options_df = session.table("smoothies.public.fruit_options").select(col("fruit_name"))

# Display ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", 
    fruit_options_df.to_pandas()["FRUIT_NAME"].tolist(),  # Convert Snowflake DF to Pandas list
    max_selections=5
)

if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)  # Efficiently format selected ingredients

    # Button to submit order
    if st.button("Submit Order"):
        query = f"""
            INSERT INTO smoothies.public.orders (name_on_order, ingredients)
            VALUES (%s, %s)
        """
        session.sql(query, params=(name_on_order, ingredients_string)).collect()  # Use safe parameterization
        st.success(f"Your Smoothie is ordered, **{name_on_order}**! ✅")
