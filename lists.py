import streamlit as st
import psycopg2

conn = st.experimental_connection("postgresql", type="sql")




botanical_name_list =[]   
somali_name_list = []
arabic_name_list = []
english_name_list = []
tree_type_list = []
climatic_zone_list = []
utilities_list = []

query = conn.query("SELECT * FROM tree")
print(query)
for row in query.itertuples():
    if row[2]:
        botanical_name_list.append(row[2])
    if row[3]:
        somali_name_list.append(row[3])
    if row[4]:
        arabic_name_list.append(row[4])
    if row[5]:
        english_name_list.append(row[5])
    if row[6] and row[6] not in tree_type_list:
        tree_type_list.append(row[6])

query = conn.query("SELECT * FROM climatic")
for row in query.itertuples():
    climatic_zone_list.append(row[2])

query = conn.query("SELECT * FROM utility")
for row in query.itertuples():
    utilities_list.append(row[2])


select_list = ["Somali", "Arabic", "English", "Other Regional Spelling", "Tree Type",
            "Climatic Zone","Minimum Rainfall", "Maximum Rainfall", 
            "Lowest Altitude", "Highest Altitude", "Lowest Temperature", 
            "Highest Temperature", "Utilities"]

