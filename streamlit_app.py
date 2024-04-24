# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Customize the fruits you want in your custom Smoothie!
    """
)

#librería col

from snowflake.snowpark.functions import col

#seleccino la columna

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

#añado multiselect

ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
)

#los datos devueltos son listas
st.write(ingredients_list)
st.text(ingredients_list)

# "if ingredients_list" significa "if ingredients_list is not null" 

if ingredients_list:

    #creo la variable "ingredients_string"

    ingredients_string= ''
    
    #loop for
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen #+ añade fruit_chosen a lo que ya existe
    
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    #st.write(my_insert_stmt)
    #añado el submit button
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
