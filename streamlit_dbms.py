import streamlit as st
import lists
import produce_SQl_statement
import psycopg2


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])
conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def main():

    st.title("Tree Manager")

    menu = ["Home","Search", "Add", "Update"]
    choice = st.sidebar.selectbox("Menu", menu)
    

    if choice == "Home":
        st.subheader("Home")
    elif choice == "Search":

        query_dict = {}

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
        query_dict["climate"] = search_climatic_zone

        search_utilities = st.multiselect(
            'Select Utilities',
            lists.utilities_list
        )
        query_dict["utilities"] = search_utilities

        

        search_rainfall = st.slider(
            'Select a range of values',
            0, 1500, (300, 1200))
        st.write("If you don't want to limit the range, slide the points to each end")
        query_dict["rainfall"] = search_rainfall 

        search_altitude = st.slider(
            'Select a range of values',
            0, 2500, (500, 2000))
        st.write("If you don't want to limit the range, slide the points to each end")
        query_dict["altitude"] = search_altitude
        search_temperature = st.slider(
            'Select a range of values',
            15, 30, (20, 25))
        st.write("If you don't want to limit the range, slide the points to each end")
        query_dict["temperature"] = search_temperature

        select_list = st.multiselect(
            'Select the Data You Want to See',
            lists.select_list
        )

        if st.button('Search!'):
            
            query_statement = produce_SQl_statement.produce_statement(query_dict,
                                                                      select_list)
            st.write(query_statement)
            rows = run_query(query_statement)
            st.table(rows)
            

    elif choice == "Add":
        st.subheader("Add")
    elif choice == "Update":
        st.subheader("Update")


    
    

    

if __name__ == '__main__':
    main()