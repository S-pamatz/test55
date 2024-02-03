import pandas as pd
import mysql.connector
import numpy as np

# Function to remove content inside <p></p> tags
def remove_inside_p_tags(text):
    while '<p>' in text and '</p>' in text:
        start = text.find('<p>')
        end = text.find('</p>') + 4
        text = text[:start] + text[end:]
    return text

# Load the CSV file into a DataFrame
df = pd.read_csv('./data.csv')

# Replace NaN values with None for database compatibility
# df.fillna(value=None, inplace=True)
df = df.where(pd.notna(df), None)


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

# Loop through each row and insert into the database
for index, row in df.iterrows():
    firstname = row['Name'].split()[0] if pd.notna(row['Name']) else None
    lastname = ' '.join(row['Name'].split()[1:]) if pd.notna(row['Name']) else None
    email = row['Email'] if pd.notna(row['Email']) else None
    wsuCampus = row['WSU Campus'] if pd.notna(row['WSU Campus']) else None
    department = row['Department'] if pd.notna(row['Department']) else None
    url = row['URL'] if pd.notna(row['URL']) else None
    interest = remove_inside_p_tags(row['Please select which primary CEREO theme best describes your area of interest:']) if pd.notna(row['Please select which primary CEREO theme best describes your area of interest:']) else None
    
    # Check if the entry already exists in the database
    check_query = "SELECT * FROM affiliate WHERE firstname = %s AND lastname = %s"
    cursor.execute(check_query, (firstname, lastname))
    result = cursor.fetchone()

    if not result:  # If entry doesn't exist, insert
        query = ("INSERT INTO affiliate (firstname, lastname, email, wsuCampus, department, url, areaofinterest) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        values = (firstname, lastname, email, wsuCampus, department, url, interest)
        
        cursor.execute(query, values)

# Commit changes to the database
connection.commit()

# Close the cursor and the connection
cursor.close()
connection.close()




# import pandas as pd
# import mysql.connector
# import re

# conn = mysql.connector.connect(
#     host="localhost",
#     user="root", # use your database username
#     password="CEREO2023", # use your database password
#     database="our_users1"
# )

# cursor = conn.cursor()

# def remove_inside_p_tags(text):
#     return re.sub(r'<p>.*?</p>', '', text)

# # Load the CSV file into a DataFrame
# df = pd.read_csv('./data.csv')

# # Loop through each row and print the specified columns
# # for index, row in df.iterrows():
# #     print("Membership Type:", row['Please indicate the kind of membership'])
# #     print("Name:", row['Name'])
# #     print("WSU Campus:", row['WSU Campus'])
# #     print("Department:", row['Department'])
# #     print("URL:", row['URL'])
# #     print("Email:", row['Email'])
    
# #     # Remove content inside <p> tags for the interest section
# #     interest = remove_inside_p_tags(row['Please select which primary CEREO theme best describes your area of interest:'])
# #     print("Interest:", interest)
    
# #     print("------")  # This will print a separator between entries

# interests = set()  # Create an empty set to store unique interests

# # Loop through each row to extract and clean interests
# # for index, row in df.iterrows():
# #     interest = remove_inside_p_tags(str(row['Please select which primary CEREO theme best describes your area of interest:']))
    
# #     # Add cleaned interest to the set
# #     interests.add(interest)

# # # Print the unique interests
# # print("Unique Interests:")
# # for interest in interests:
# #     print(interest)


# # for column in df.columns:
# #     print(column)

# for index, row in df.iterrows():
#     # Parse data
#     firstname, lastname = row['Name'].split(' ', 1)
#     email = row['Email']
#     wsu_campus = row['WSU Campus']
#     department = row['Department']
#     url = row['URL']
#     area_of_interest = remove_inside_p_tags(row['Please select which primary CEREO theme best describes your area of interest:'])
    
#     # Check if entry with the same name already exists
#     check_query = """
#     SELECT COUNT(*) FROM affiliate WHERE firstname = %s AND lastname = %s
#     """
#     cursor.execute(check_query, (firstname, lastname))
#     count = cursor.fetchone()[0]  # fetch the count result
    
#     # If the entry doesn't exist, insert the data
#     if count == 0:
#         # Construct the SQL insert statement
#         query = """
#         INSERT INTO affiliate (firstname, lastname, email, wsuCampus, department, url, areaofinterest)
#         VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (firstname, lastname, email, wsu_campus, department, url, area_of_interest)
        
#         # Execute the SQL command
#         cursor.execute(query, values)
        
#         # Commit the transaction
#         conn.commit()
