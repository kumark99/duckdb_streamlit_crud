import duckdb
import pandas as pd

# Connect to DuckDB (or create it if it doesn't exist)
con = duckdb.connect('employee.db')

# Create the emp table
con.execute('''
CREATE TABLE IF NOT EXISTS emp (
    id INTEGER PRIMARY KEY,
    firstname VARCHAR,
    lastname VARCHAR,
    dob DATE,
    doj DATE,
    sal DECIMAL,
    dept VARCHAR
)
''')

# Insert sample data
sample_data = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'firstname': ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Heidi'],
    'lastname': ['Doe', 'Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Martinez', 'Anderson', 'Taylor', 'Thomas'],
    'dob': ['1990-01-01', '1985-05-15', '1992-08-22', '1988-12-10', '1995-03-30', '1980-07-07', '1991-11-11', '1987-04-04', '1993-09-09', '1982-02-28'],
    'doj': ['2020-01-15', '2019-03-20', '2021-06-10', '2018-09-05', '2022-02-25', '2017-05-12', '2023-01-01', '2016-08-30', '2021-11-11', '2015-07-22'],
    'sal': [50000, 55000, 60000, 52000, 58000, 65000, 59000, 54000, 62000, 57000],
    'dept': ['HR', 'Engineering', 'Marketing', 'Sales', 'Finance', 'HR', 'Engineering', 'Marketing', 'Sales', 'Finance']
}

df = pd.DataFrame(sample_data)
con.execute('INSERT INTO emp SELECT * FROM df')
