import streamlit as st
import lists
import produce_SQl_statement
import psycopg2
from collections import defaultdict


conn = st.experimental_connection("postgresql", type="sql")
st.markdown("""
<style>
.monospace {
    font-family:monospace;
}
</style>
""", unsafe_allow_html=True)

######## SEARCH PAGE ##################
def search_page():
    query_dict = defaultdict(list)

    st.subheader("Search")
    search_botanical = st.multiselect(
        'Select an Botanical Name',
        lists.botanical_name_list
    )
    query_dict["botanical"] = search_botanical
        
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

    search_english = st.multiselect(
        'Select an English Name',
        lists.english_name_list
    )
    query_dict["english"] = search_english

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
        st.write(f"I want a tree that can live below :green[{search_temperature[0]} degrees]\
                 but  also above :green[{search_temperature[1]} degrees]")
        

    select_list = st.multiselect(
        'Select the Data You Want to See',
        lists.select_list
    )

    if st.button('Search!'):
            
        query_statement = produce_SQl_statement.produce_search_statement(query_dict,
                                                                      select_list)
        st.write("The search is based on the following inputs!!")
        for k,v in query_dict.items():
            if v:
                st.write(k,v)
        st.markdown('<h6 class="monospace">' + query_statement + '</h6>', unsafe_allow_html=True)
        df = conn.query(query_statement)
        

        st.dataframe(df, hide_index=True)
        
############# ADD PAGE ########
def add_page():

    def enable():
        if botanical_input:
            st.session_state["disabled"] =  False
        else:
            st.warning("Enter Botanical Name before adding other info!!")
            st.session_state["disabled"] = True

    def update_dict(utility, usage_freq, utility_usage_dict):
        if usage_freq > -1:
            utility_usage_dict[utility] = usage_freq
        elif usage_freq == -1 and utility in utility_usage_dict:
            utility_usage_dict.pop(utility)

    def uncheck():
        if not botanical_input:
            st.session_state["somali"] = False
            st.session_state["arabic"] = False
            st.session_state["english"] = False
            st.session_state["tree_type"] = False
            st.session_state["climate"] = False
            st.session_state["utility"] = False
    
    def reset():
        st.session_state["botanical"] = False
        st.session_state["somali"] = False
        st.session_state["arabic"] = False
        st.session_state["english"] = False
        st.session_state["tree_type"] = False
        st.session_state["climate"] = False
        st.session_state["utility"] = False
    
    if 'disabled' not in st.session_state:
        st.session_state["disabled"] = True
    if 'utility_usage_dict' not in st.session_state:
        st.session_state['utility_usage_dict'] = defaultdict(int)

    insertable = 0
    query_dict = defaultdict(str)
    st.subheader("Add Page")
    botanical_input = st.text_input("Enter Botanical Name", key="botanical")
    uncheck()
    enable()
    botanical_list = [x.lower() for x in lists.botanical_name_list]
    if botanical_input.lower() in botanical_list:
        st.warning("TREE ALREADY EXISTS!!")
    else:
        query_dict["botanical"] = botanical_input
        insertable = 1

    if st.checkbox("I know Somali Name!", disabled=st.session_state.disabled, key="somali"):
        somali_input = st.text_input("Enter Somali Name")
        if somali_input:
            query_dict["somali"] = somali_input

    if st.checkbox("I know Arabic Name!", disabled=st.session_state.disabled, key="arabic"):
        arabic_input = st.text_input("Enter Arabic Name")
        if arabic_input:
            query_dict["arabic"] = arabic_input
    
    if st.checkbox("I know English Name!", disabled=st.session_state.disabled, key="english"):
        english_input = st.text_input("Enter English Name")
        if english_input:
            query_dict["english"] = english_input

    if st.checkbox("I know Tree Type!", disabled=st.session_state.disabled, key="tree_type"):
        tree_type_input = st.text_input("Enter Tree Type")
        if tree_type_input:
            query_dict["tree_type"] = tree_type_input
    
    query_add_statement = produce_SQl_statement.produce_add_statement(query_dict)
    st.markdown('<h6 class="monospace">' + query_add_statement + '</h6>', unsafe_allow_html=True)

    if st.checkbox("I want to enter climate zone!", disabled=st.session_state.disabled, key="climate"):
        climatic_zone = st.multiselect('', lists.climatic_zone_list)
        if climatic_zone:
            query_add_climatic_statement = produce_SQl_statement.produce_add_climatic_statement(climatic_zone)
            st.markdown('<h6 class="monospace">' + query_add_climatic_statement + '</h6>', unsafe_allow_html=True)
            query_add_statement += query_add_climatic_statement
    
    utility_usage_dict = st.session_state.get('utility_usage_dict')

    if st.checkbox("I want to add utility usage!!", disabled=st.session_state.disabled, key="utility"):
        st.warning("If you don't know what the tree is used for, leave it as -1")
        for i in lists.utilities_list:
            utility_freq = st.radio(i, [-1, 0, 1, 2], horizontal=True)
            utility_usage_dict[i] = utility_freq
        
        st.write(utility_usage_dict)

        # st.radio("Toothbrush", ["0", "1", "2"], horizontal=True)
        # utility = st.selectbox('', lists.utilities_list)
        # if utility:
        #     usage_freq = st.select_slider(
        #         "From 0 to 2, how often is {} used for {}? If you don't know, choose -1".format(botanical_input, utility),
        #         options=[-1, 0, 1, 2])
        #     if st.button('Add'):
        #         update_dict(utility, usage_freq, utility_usage_dict)        
        # st.write(utility_usage_dict)

        query_add_utility_statement = produce_SQl_statement.produce_add_utility_statement(utility_usage_dict)
        st.markdown('<h6 class="monospace">' + query_add_utility_statement + '</h6s>', unsafe_allow_html=True)
        query_add_statement += query_add_utility_statement

    notify_text = "Botanical Name: {}".format(botanical_input)
    if st.button("ADD TREE!!"):
        st.warning("YOU ARE ABOUT TO ADD THE FOLLOWING INFO TO DATABASE")
        st.markdown('<h6 class="monospace">' + query_add_statement + '</h6>', unsafe_allow_html=True)
        if st.button("OK!"):
            df = conn.query(query_add_statement)
            reset()

def update_page():
    tree_to_update = st.selectbox("Which tree do you want to update?", lists.botanical_name_list, index=None, placeholder="Select tree...")
    if tree_to_update:
        q = conn.query(""" SELECT botanical_name AS "Botanical Name", somali_name AS "Somali Name", \
               arabic_name AS "Arabic Name", english_name AS "English Name", \
               STRING_AGG(DISTINCT spelling, ', ') AS "Other Regional Spelling" , \
               STRING_AGG(DISTINCT tree_type, ', ') AS "Tree Type" , \
               STRING_AGG(DISTINCT climatic_zone, ', ') AS "Climatic Zone" , \
               STRING_AGG(DISTINCT (CASE WHEN utility_usage = 1 THEN utility_name WHEN utility_usage = 2 THEN UPPER(utility_name) END), ', ') AS "Utilities" \
               FROM tree LEFT JOIN regional_spelling ON regional_spelling.tree_id = tree.id \
               INNER JOIN climatic_zone ON climatic_zone.tree_id = tree.id INNER JOIN climatic ON climatic.id = climatic_zone.climatic_id \
               INNER JOIN utility_usage ON utility_usage.tree_id = tree.id INNER JOIN utility ON utility.id = utility_usage.utility_id 
               WHERE botanical_name LIKE '%{}%' GROUP BY tree.id ORDER BY tree.id""".format(tree_to_update))

        edited_q = st.data_editor(q, hide_index=True)

        st.write(q)
        st.write(edited_q)
    
    if st.button("UPDATE!!"):
        query_update_statement = ""
        table_dict = {"Arabic Name": ["tree", "arabic_name"], "Botanical Name": ["tree","botanical_name"], "English Name": ["tree", "english_name"],
                      "Somali Name": ["tree", "somali_name"], "Tree Type": ["tree", "tree_type"],
                      }
        diff = q.compare(edited_q)
        st.write(diff)
        for column in diff:
            columnName, self_or_other = column
            if self_or_other == "other":
                columnData = diff[column][0]
                st.write("New " + columnName + ": " + columnData)
                query_update_statement += produce_SQl_statement.produce_update_statement(tree_to_update, columnName, columnData, table_dict)

        st.markdown('<h6 class="monospace">' + query_update_statement + '</h6s>', unsafe_allow_html=True)

                
    
    

    
            
   
    

def main():

    st.title("Tree Manager")

    menu = ["Home","Search", "Add", "Update"]
    choice = st.sidebar.selectbox("Menu", menu)
    

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Search":
        search_page()

    elif choice == "Add":
        add_page()
    elif choice == "Update":
        update_page()
        


    
    

    

if __name__ == '__main__':
    main()