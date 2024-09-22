import pymysql

DB_CONFIG = {
        'host'        :'35.222.24.104',
        'user'        :'root',
        'password'    :'j}(biN#qCJkt(|tK',
        'database'    :'amora_general',
        'port'        :3306
}

#Login Purposes
def check_email_query(email):
    # Open a connection to the database
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM employees WHERE personal_email = %s"
            cursor.execute(sql, (email))
            result = cursor.fetchone()
           
            print(result)
            return result

    finally:
      if connection:
          connection.close

def input_query(query):
            
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        list = cursor.fetchall()
        result = []
        for value in list:
            result.append(value)
        return list
    except Exception as e :
        print("exception: ", e)
    finally:
        connection.close()




def query_info(key,val):
     sql_query = f"select g_id as g_id, g_name as g_name, g_link as g_link, g_category as g_category  from guidelines where g_id = {val}"
     selected_guidelines = input_query(sql_query)
     arr = list(selected_guidelines[0])
     return arr