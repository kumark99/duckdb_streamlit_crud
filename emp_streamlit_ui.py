import streamlit as st
import duckdb
import pandas as pd


# Connect to DuckDB
con = duckdb.connect('employee.db')

# Function to fetch all records
def fetch_all_records():
    return con.execute('SELECT * FROM emp').fetchdf()

# Function to add a new record
def add_record(data):
    con.execute('INSERT INTO emp VALUES (?, ?, ?, ?, ?, ?, ?)', data)

# Function to update a record
def update_record(id, data):
    con.execute('''
    UPDATE emp
    SET firstname = ?, lastname = ?, dob = ?, doj = ?, sal = ?, dept = ?
    WHERE id = ?
    ''', (*data, id))

# Function to delete a record
def delete_record(id):
    con.execute('DELETE FROM emp WHERE id = ?', (id,))

# Streamlit UI
st.set_page_config(layout="wide")
st.title('Employee CRUD Application with Analytics')

# Include Bootstrap CSS and Font Awesome
st.markdown("""
    <link
      rel="stylesheet"
      href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
      integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
      crossorigin="anonymous"
    >
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
    >
    <style>
    .action-icons {
        font-size: 1.5em;
        cursor: pointer;
        margin: 0 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False

if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None

# Button to add new employee
if st.button('Add New Employee'):
    st.session_state.show_add_form = True

# Form to add new employee
if st.session_state.show_add_form:
    with st.form('add_form'):
        id = st.number_input('ID', min_value=1, key='new_id')
        firstname = st.text_input('First Name', key='new_firstname')
        lastname = st.text_input('Last Name', key='new_lastname')
        dob = st.date_input('Date of Birth', key='new_dob')
        doj = st.date_input('Date of Joining', key='new_doj')
        sal = st.number_input('Salary', min_value=0.0, format="%.2f", key='new_sal')
        dept = st.text_input('Department', key='new_dept')
        submit_button = st.form_submit_button('Add Employee')

        if submit_button:
            add_record((id, firstname, lastname, dob, doj, sal, dept))
            st.success('Employee added successfully!')
            st.session_state.show_add_form = False

# Display aggregate statistics
st.header('Department-wise Statistics')
aggregate_stats = con.execute('''
    SELECT
        dept,
        COUNT(*) AS num_employees,
        AVG(sal) AS avg_salary,
        SUM(sal) AS total_salary
    FROM emp
    GROUP BY dept
''').fetchdf()
st.dataframe(aggregate_stats)

# Display all records with edit and delete icons using columns
st.header('Employee Records')
records = fetch_all_records()

# Convert DataFrame to list of dictionaries for custom display
records_dict = records.to_dict(orient='records')

# Display table headers
st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.markdown('<div class="row font-weight-bold">'
            '<div class="col">ID</div>'
            '<div class="col">First Name</div>'
            '<div class="col">Last Name</div>'
            '<div class="col">Date of Birth</div>'
            '<div class="col">Date of Joining</div>'
            '<div class="col">Salary</div>'
            '<div class="col">Department</div>'
            '<div class="col">Actions</div>'
            '</div>', unsafe_allow_html=True)

# Display table rows using Streamlit columns
for record in records_dict:
    cols = st.columns(8)  # 8 columns for each field
    cols[0].write(record['id'])
    cols[1].write(record['firstname'])
    cols[2].write(record['lastname'])
    cols[3].write(record['dob'])
    cols[4].write(record['doj'])
    cols[5].write(f"${record['sal']:.2f}")
    cols[6].write(record['dept'])

    # Edit and Delete icons
    if cols[7].button('📝', key=f"edit_{record['id']}", help="Edit this record"):
        st.session_state.edit_id = record['id']

    if cols[7].button('🗑️', key=f"delete_{record['id']}", help="Delete this record"):
        delete_record(record['id'])
        st.success('Employee deleted successfully!')

# Form to edit employee
if st.session_state.edit_id is not None:
    edit_id = st.session_state.edit_id
    record_to_edit = con.execute(f'SELECT * FROM emp WHERE id = {edit_id}').fetchdf().iloc[0]

    with st.form(f"update_form_{edit_id}"):
        new_firstname = st.text_input('First Name', record_to_edit['firstname'], key=f"firstname_{edit_id}")
        new_lastname = st.text_input('Last Name', record_to_edit['lastname'], key=f"lastname_{edit_id}")
        new_dob = st.date_input('Date of Birth', pd.to_datetime(record_to_edit['dob']), key=f"dob_{edit_id}")
        new_doj = st.date_input('Date of Joining', pd.to_datetime(record_to_edit['doj']), key=f"doj_{edit_id}")
        new_sal = st.number_input('Salary', value=record_to_edit['sal'], format="%.2f", key=f"sal_{edit_id}")
        new_dept = st.text_input('Department', record_to_edit['dept'], key=f"dept_{edit_id}")
        submit_button = st.form_submit_button('Update Employee')

        if submit_button:
            update_record(edit_id, (new_firstname, new_lastname, new_dob, new_doj, new_sal, new_dept))
            st.success('Employee updated successfully!')
            st.session_state.edit_id = None

st.markdown('</div>', unsafe_allow_html=True)
