import pandas as pd
import mysql.connector

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
df = df.where(pd.notna(df), None)

# Create a connection to the MySQL database
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'our_users1',
    'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

# Prepare the INSERT statement
insert_query = ("INSERT INTO affiliate (firstname, lastname, email, wsuCampus, department, url, areaofinterest) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)")

# Loop through each row and insert into the affiliate table
for index, row in df.iterrows():
    firstname = row['Name'].split()[0] if row['Name'] else None
    lastname = ' '.join(row['Name'].split()[1:]) if row['Name'] else None
    email = row['Email'] if row['Email'] else None
    wsu_campus = row['WSU Campus'] if row['WSU Campus'] else None
    department = row['Department'] if row['Department'] else None
    url = row['URL'] if row['URL'] else None
    interest = remove_inside_p_tags(row['Please select which primary CEREO theme best describes your area of interest:']) if row['Please select which primary CEREO theme best describes your area of interest:'] else None

    # Check for duplicate names before inserting
    check_query = "SELECT id FROM affiliate WHERE firstname = %s AND lastname = %s"
    cursor.execute(check_query, (firstname, lastname))
    result = cursor.fetchone()
    
    # If no duplicate is found, insert the new record
    if not result:
        cursor.execute(insert_query, (firstname, lastname, email, wsu_campus, department, url, interest))

# Commit changes to the database
connection.commit()

# Close the cursor and the connection
cursor.close()
connection.close()
