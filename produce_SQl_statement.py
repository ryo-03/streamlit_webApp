


#################### FUNCTIONS USED FOR ADD FUNCTIONALITY ########################



def produce_add_utility_statement(utility_usage_dict):

    statement = ""
    utility_dict = {"Toothbrushes": 1, "Toolhandles": 2, "Timber": 3, "Tannins": 4, "Soil Improvement": 5,
                    "Shelterbelt": 6, "Sandune Fixation": 7, "Poles": 8, "People Shade": 9, 
                    "Nitrogen Fixation": 10, "Medicine": 11, "Livestock Shade": 12, "Live Fencing": 13,
                    "Intercropping": 14, "Insecticide": 15, "Honey": 16, "Hedge": 17, "Gums": 18, 
                    "Fuel": 19, "Fruit": 20, "Fodder": 21, "Edible Leaves": 22, "Dyes": 23, 
                    "Dead Fencing": 24, "Charcoal": 25, "Carving": 26, "Amenity": 27}
    for k,v in utility_usage_dict.items():
        if v != -1:
            statement += "INSERT INTO utility_usage VALUES ((SELECT MAX(id)+1 FROM utility_usage), "\
                "(SELECT MAX(id) FROM tree), {}, {}); ".format(utility_dict[k], v)
    return statement

def produce_add_climatic_statement(climatic_list):
    statement = ""
    climatic_dict = {"Very Dry": 1, "Lowland Dry": 2, 
                     "Highland Dry": 3, "Lowland Wet": 4, "Highland Wet": 5}
    for i in climatic_list:
        statement += "INSERT INTO climatic_zone VALUES ((SELECT MAX(id)+1 FROM climatic_zone), "\
        " {}, (SELECT MAX(id) FROM tree)); ".format(climatic_dict[i])

    return statement 

def produce_add_statement(query_dict):

    insert_statement = "INSERT INTO tree (id, botanical_name"
    values_statement = "VALUES((SELECT MAX(id)+1 FROM tree), '{}'".format(query_dict["botanical"])
    if "somali" in query_dict:
        insert_statement += ", somali_name"
        values_statement += ", '{}'".format(query_dict["somali"])
    if "arabic" in query_dict:
        insert_statement += ", arabic_name"
        values_statement += ", '{}'".format(query_dict["arabic"])

    if "english" in query_dict:
        insert_statement += ", english_name"
        values_statement += ", '{}'".format(query_dict["english"])

    if "tree_type" in query_dict:
        insert_statement += ", tree_type"
        values_statement += ", '{}'".format(query_dict["tree_type"])

    insert_statement += ") "
    values_statement += "); "

    return insert_statement + values_statement




####################### FUNCTIONS USED FOR SEARCH FUNCTIONALITY ###################



def order_statement():
    return ' ORDER BY tree.id'

def having_statement(query_dict):
    query = ""
    having = 0
    AND = 0

    if query_dict["climatic"]:
        li = query_dict["climatic"]
        if having == 0:
            query += " HAVING"
            having = 1
        if AND == 1:
            query += " AND"
        else: 
            AND = 1
        for i in range(len(li)):
            if i > 0:
                query += " AND"
            query += " STRING_AGG(DISTINCT climatic_zone, ', ') LIKE '%{}%'".format(li[i])
        
    if query_dict["rainfall"]:
        if having == 0:
            query += " HAVING"
            having = 1
        if AND == 1:
            query += " AND"
        else: 
            AND = 1
        query += " MIN(rainfall_min) <= {} AND MAX(rainfall_max) >= {}"\
            .format(query_dict["rainfall"][0], query_dict["rainfall"][1])
    
    if query_dict["altitude"]:
        if having == 0:
            query += " HAVING"
            having = 1
        if AND == 1:
            query += " AND"
        else: 
            AND = 1
        query += " MIN(altitude_min) <= {} AND MAX(altitude_max) >= {}"\
            .format(query_dict["altitude"][0], query_dict["altitude"][1])
        
    if query_dict["temperature"]:
        if having == 0:
            query += " HAVING"
            having = 1
        if AND == 1:
            query += " AND"
        else: 
            AND = 1
        query += " MIN(temperature_min) <= {} AND MAX(temperature_max) >= {}"\
            .format(query_dict["temperature"][0], query_dict["temperature"][1])

    utility_list = query_dict["utilities"]
    if query_dict["utilities"]:
        if having == 0:
            query += " HAVING"
            having = 1
        if AND == 1:
            query += " AND"
        else: 
            AND = 1
        for i in range(len(utility_list)):
            if i > 0:
                query += " AND"
            query += " utility_list LIKE '%{}%'".format(utility_list[i])
    

    return query

def group_statement():
    return ' GROUP BY tree.id'

def where_statement(query_dict):
    query = ""
    where = 0
    OR = 0
    if query_dict["botanical"]:
        li = query_dict["botanical"]
        if where == 0:
            query += " WHERE"
            where = 1
        if OR == 1:
            query += " OR"
        else:
            OR = 1
        for i in range(len(li)):
            if i > 0:
                query += " OR"
            query += " botanical_name LIKE '%{}%'".format(li[i])

    if query_dict["somali"]:
        li = query_dict["somali"]
        if where == 0:
            query += " WHERE"
            where = 1
        if OR == 1:
            query += " OR"
        else:
            OR = 1
        for i in range(len(li)):
            if i > 0:
                query += " OR"
            query += " somali_name LIKE '%{}%'".format(li[i])

    if query_dict["arabic"]:
        li = query_dict["arabic"]
        if where == 0:
            query += " WHERE"
            where = 1
        if OR == 1:
            query += " OR"
        else:
            OR = 1
        for i in range(len(li)):
            if i > 0:
                query += " OR"
            query += " arabic_name LIKE '%{}%'".format(li[i])

    if query_dict["english"]:
        li = query_dict["english"]
        if where == 0:
            query += " WHERE"
            where = 1
        if OR == 1:
            query += " OR"
        else:
            OR = 1
        for i in range(len(li)):
            if i > 0:
                query += " OR"
            query += " english_name LIKE '%{}%'".format(li[i])

    if query_dict["type"]:
        li = query_dict["type"]
        if where == 0:
            query += " WHERE"
            where = 1
        if OR == 1:
            query += " OR"
        else:
            OR = 1
        for i in range(len(li)):
            if i > 0:
                query += " OR"
            query += " tree_type LIKE '%{}%'".format(li[i])


    return query


def join_statement():
    return """
            FROM tree
            LEFT JOIN regional_spelling 
                ON regional_spelling.tree_id = tree.id 
            INNER JOIN climatic_zone 
                ON climatic_zone.tree_id = tree.id 
            INNER JOIN climatic 
                ON climatic.id = climatic_zone.climatic_id 
            INNER JOIN utility_usage 
                ON utility_usage.tree_id = tree.id 
            INNER JOIN utility 
                ON utility.id = utility_usage.utility_id 
            """
            

def data_to_view(select_list, utility_list):
    statement = 'SELECT botanical_name AS "Botanical Name"'

    if "Somali" in select_list:
        statement += ', somali_name AS "Somali Name"'
    if "Arabic" in select_list:
        statement += ', arabic_name AS "Arabic Name"'
    if "English" in select_list:
        statement += ', english_name AS "English Name"'
    if "Other Regional Spelling" in select_list:
        statement += """, STRING_AGG(DISTINCT spelling, ', ') AS "Other Regional Spelling" """
    if "Tree Type" in select_list:
        statement += """,  STRING_AGG(DISTINCT tree_type, ', ') AS "Tree Type" """
    if "Climatic Zone" in select_list:
        statement += """, STRING_AGG(DISTINCT climatic_zone, ', ') AS "Climatic Zone" """
    if "Minimum Rainfall" in select_list:
        statement += ', MIN(rainfall_min) AS "Minimum Rainfall"'
    if "Maximum Rainfall" in select_list:
        statement += ', Max(rainfall_max) AS "Maximum Rainfall"'
    if "Lowest Altitude" in select_list:
        statement += ', MIN(altitude_min) AS "Lowest Altitude"'
    if "Highest Altitude" in select_list:
        statement += ', MAX(altitude_max) AS "Highest Altitude"'
    if "Lowest Temperature" in select_list:
        statement += ', MIN(temperature_min) AS "Lowest Temperature"'
    if "Highest Temperature" in select_list:
        statement += ', MAX(temperature_max) AS "Highest Temperature"'  
    if "Utilities" in select_list or utility_list:
        statement += """, STRING_AGG(DISTINCT (CASE 
                            WHEN utility_usage = 1 THEN utility_name 
                            WHEN utility_usage = 2 THEN UPPER(utility_name)
                            END), ', ')  AS "Utilities" """
    return statement



def produce_search_statement(query_dict, select_list):
    statement = ""

    statement += data_to_view(select_list, query_dict["utilities"])
    statement += join_statement()
    statement += where_statement(query_dict)
    statement += group_statement()
    statement += having_statement(query_dict)

    statement += order_statement()
    print(statement)
    

    return statement


