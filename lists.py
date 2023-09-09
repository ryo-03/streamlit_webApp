import streamlit as st
import psycopg2

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])
conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        # try:
        #     cur.execute(query)
        # except Exception as e:
        #     print(f'Error {e}')
        #     conn.rollback()
        # return cur.fetchall()
        return cur.fetchall()
botanical_name_list =[]   
somali_name_list = []
arabic_name_list = []
english_name_list = []
tree_type_list = []
climatic_zone_list = []
utilities_list = []

query = run_query("SELECT * FROM tree")
for i in query:
    if [1]:
        botanical_name_list.append(i[1])
    if i[2]:
        somali_name_list.append(i[2])
    if i[3]:
        arabic_name_list.append(i[3])
    if i[4]:
        english_name_list.append(i[4])
    if i[5] and i[5] not in tree_type_list:
        tree_type_list.append(i[5])

query = run_query("SELECT * FROM climatic")
for i in query:
    climatic_zone_list.append(i[1])

query = run_query("SELECT * FROM utility")
for i in query:
    utilities_list.append(i[1])


select_list = ["Somali", "Arabic", "English", "Other Regional Spelling", "Tree Type",
            "Climatic Zone","Minimum Rainfall", "Maximum Rainfall", 
            "Lowest Altitude", "Highest Altitude", "Lowest Temperature", 
            "Highest Temperature", "Utilities"]

