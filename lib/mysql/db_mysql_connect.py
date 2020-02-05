import pymysql

def mysql_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        passwd="yourpassword",
        database="mydatabase"
    )