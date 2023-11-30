import pandas as pd
import mysql.connector

# Load the CSV file into a DataFrame
df = pd.read_csv('./data.csv')

# Create a set of unique departments
unique_departments = set(df['Department'].dropna())

# Create a connection to the MySQL database
config = {
    'user': 'root',
    'password': 'CEREO2023',
    'host': 'localhost',
    'database': 'our_users1',
    'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

# Insert unique departments into the department table
for department in unique_departments:
    # Check if the department already exists in the department table
    check_query = "SELECT COUNT(*) FROM department WHERE name = %s"
    cursor.execute(check_query, (department,))
    count = cursor.fetchone()[0]
    
    # If the department doesn't exist, insert it
    if count == 0:
        insert_query = "INSERT INTO department (name) VALUES (%s)"
        cursor.execute(insert_query, (department,))

# Commit changes to the database
connection.commit()

# Close the cursor and the connection
cursor.close()
connection.close()
