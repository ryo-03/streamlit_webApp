import streamlit as st
import lists
import produce_SQl_statement


conn = st.experimental_connection("mysql", type="sql")

def main():

    st.title("Tree Manager")

    menu = ["Home","Search", "Add", "Update"]
    choice = st.sidebar.selectbox("Menu", menu)
    

    if choice == "Home":
        st.subheader("Home")
    elif choice == "Search":
        st.subheader("Search")
        search_english = st.multiselect(
            'Select an English Name',
            lists.english_name_list
        )
        
        search_somali = st.multiselect(
            'Select a Somali Name',
            lists.somali_name_list
        )
        st.write('List:', search_somali)

        search_arabic = st.multiselect(
            'Select an Arabic Name',
            lists.arabic_name_list
        )

        search_tree_type = st.multiselect(
            'Select a Tree Type',
            lists.tree_type_list
        )

        search_climatic_zone = st.multiselect(
            'Select a Climatic Zone',
            lists.climatic_zone_list
        )

        search_utilities = st.multiselect(
            'Select Utilities',
            lists.utilities_list
        )

        

        search_rainfall = st.slider(
            'Select a range of values',
            0, 1500, (300, 1200))
        st.write('Values:', search_rainfall)
        search_altitude = st.slider(
            'Select a range of values',
            0, 2500, (500, 2000))
        st.write('Values:', search_altitude)
        search_temperature = st.slider(
            'Select a range of values',
            15, 30, (20, 25))
        st.write('Values:', search_temperature)

        select_list = st.multiselect(
            'Select the Data You Want to See',
            lists.select_list
        )

        if st.button('Search!'):
            
            query_statement = produce_SQl_statement.produce_statement(search_english,
                                                                      search_somali, 
                                                                      search_utilities, 
                                                                      select_list)
            df = conn.query(query_statement, ttl=0)
            st.table(df)
            

    elif choice == "Add":
        st.subheader("Add")
    elif choice == "Update":
        st.subheader("Update")


    
    

    

if __name__ == '__main__':
    main()