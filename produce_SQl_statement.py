def group_statement():
    return "GROUP BY tree.id"

def join_statement():
    return """
            FROM tree 
            LEFT JOIN regional_spelling
			    ON regional_spelling.tree_id = tree.id
            JOIN climatic_zone
	            ON climatic_zone.tree_id = tree.id
            JOIN climatic
	            ON climatic.id = climatic_zone.climatic_id
            JOIN utility_usage
                ON utility_usage.tree_id = tree.id
            JOIN utility
                ON utility.id = utility_usage.utility_id 
            """
            

def data_to_view(select_list, utility_list):
    statement = "SELECT botanical_name AS `Botanical Name`"

    if "Somali" in select_list:
        statement += ", somali_name AS `Somali Name`"
    if "Arabic" in select_list:
        statement += ", arabic_name AS `Arabic Name`"
    if "English" in select_list:
        statement += ", english_name AS `English Name`"
    if "Other Regional Spelling" in select_list:
        statement += ", GROUP_CONCAT(DISTINCT spelling SEPARATOR ', ') AS `Other Regional Spelling`"
    if "Tree Type" in select_list:
        statement += ",  GROUP_CONCAT(DISTINCT tree_type SEPARATOR ', ') AS `Tree Type`"
    if "Climatic Zone" in select_list:
        statement += ", GROUP_CONCAT(DISTINCT climatic_zone SEPARATOR ', ') AS `Climatic Zone`"
    if "Minimum Rainfall" in select_list:
        statement += ", MIN(rainfall_min) AS `Minimum Rainfall`"
    if "Maximum Rainfall" in select_list:
        statement += ", Max(rainfall_max) AS `Maximum Rainfall`"
    if "Lowest Altitude" in select_list:
        statement += ", MIN(altitude_min) AS `Lowest Altitude`"
    if "Highest Altitude" in select_list:
        statement += ", MAX(altitude_max) AS `Highest Altitude`"
    if "Utilities" in select_list or utility_list:
        statement += """
                        , GROUP_CONCAT(DISTINCT CONCAT(CASE 
                            WHEN utility_usage = 1 THEN utility_name 
                            WHEN utility_usage = 2 THEN UPPER(utility_name)
                            END) SEPARATOR ', ') as `Usage`
                    """
    return statement



def produce_statement(english_list, somali_list, utility_list, select_list):
    statement = ""

    statement += data_to_view(select_list, utility_list)
    statement += join_statement()

    statement += group_statement()
    

    return statement
