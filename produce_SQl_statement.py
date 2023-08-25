def order_statement():
    return ' ORDER BY tree.id'

def having_statement(query_dict):
    query = ""
    having = 0
    AND = 0

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

    utility_list = query_dict["utilities"]
    # query += " AND MIN(temperture_min) <= {} AND MAX(altitude_max) >= {}".format(altitude_range[0], altitude_range[1])
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
    
    if query_dict["climatic"]:
        li = query_dict["climatic"]
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
            query += " climatic_zone LIKE '%{}%'".format(li[i])

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
    if "Utilities" in select_list or utility_list:
        statement += """, STRING_AGG(DISTINCT (CASE 
                            WHEN utility_usage = 1 THEN utility_name 
                            WHEN utility_usage = 2 THEN UPPER(utility_name)
                            END), ', ') """
    return statement



def produce_statement(query_dict, select_list):
    statement = ""

    statement += data_to_view(select_list, query_dict["utilities"])
    statement += join_statement()
    statement += where_statement(query_dict)
    statement += group_statement()
    statement += having_statement(query_dict)

    statement += order_statement()
    print(statement)
    

    return statement
