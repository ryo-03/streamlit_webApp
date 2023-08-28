import streamlit as st
import lists
import produce_SQl_statement
import psycopg2
from collections import defaultdict


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])
conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        try:
            cur.execute(query)
        except Exception as e:
            print(f'Error {e}')
            conn.rollback()
        return cur.fetchall()


def search_page():
    query_dict = defaultdict(list)

    st.subheader("Search")
    search_english = st.multiselect(
        'Select an English Name',
        lists.english_name_list
    )
    query_dict["english"] = search_english
        
    search_somali = st.multiselect(
        'Select a Somali Name',
        lists.somali_name_list
    )
    query_dict["somali"] = search_somali

    search_arabic = st.multiselect(
        'Select an Arabic Name',
        lists.arabic_name_list
    )
    query_dict["arabic"] = search_arabic

    search_tree_type = st.multiselect(
        'Select a Tree Type',
        lists.tree_type_list
    )
    query_dict["type"] = search_tree_type

    search_climatic_zone = st.multiselect(
        'Select a Climatic Zone',
        lists.climatic_zone_list
    )
    query_dict["climatic"] = search_climatic_zone

    search_utilities = st.multiselect(
        'Select Utilities',
        lists.utilities_list
    )
    query_dict["utilities"] = search_utilities

        
    if st.checkbox("Limit Rainfall Range"):
        search_rainfall = st.slider(
            'Select a range of values',
            0, 1500, (700, 800)
        )
        query_dict["rainfall"] = list(search_rainfall)
        st.write(f"I want a tree that can live less than :green[{search_rainfall[0]}mm]\
                  but more than :green[{search_rainfall[1]}mm] of rainfall")

    if st.checkbox("Limit Altitude Range"):
        search_altitude = st.slider(
            'Select a range of values',
            0, 2500, (1200, 1300)
        )
        query_dict["altitude"] = list(search_altitude)
        st.write(f"I want a tree that can live below :green[{search_altitude[0]}m]\
                 but  also above :green[{search_altitude[1]}m]")

    if st.checkbox("Limit Temperature Rnage"):
        search_temperature = st.slider(
            'Select a range of values',
            15, 30, (20, 25)
        )
        query_dict["temperature"] = list(search_temperature)
        st.write("If you don't want to limit the range, slide the points to each end")
        

    select_list = st.multiselect(
        'Select the Data You Want to See',
        lists.select_list
    )
    st.write(query_dict)

    if st.button('Search!'):
            
        query_statement = produce_SQl_statement.produce_statement(query_dict,
                                                                      select_list)
        st.write("The search is based on the following inputs!!")
        for k,v in query_dict.items():
            if v:
                st.write(k,v)
        st.write(query_statement)
        rows = run_query(query_statement)

        st.table(rows)


def main():

    st.title("Tree Manager")

    menu = ["Home","Search", "Add", "Update"]
    choice = st.sidebar.selectbox("Menu", menu)
    

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Search":
        search_page()

    elif choice == "Add":
        st.subheader("Add")
    elif choice == "Update":
        st.subheader("Update")


    
    

    

if __name__ == '__main__':
    main()