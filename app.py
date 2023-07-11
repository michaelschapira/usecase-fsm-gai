import streamlit as st
import pandas as pd
import numpy as np
import smtplib
import base64
import io 

def get_table_download_link(df):
    # Create an in-memory Excel file stream
    excel_file = io.BytesIO()

    # Save the DataFrame to the Excel file
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    # Seek to the beginning of the stream
    excel_file.seek(0)

    # Create a base64 encoded string from the Excel data
    b64 = base64.b64encode(excel_file.read()).decode()

    # Generate a download link with the base64 data
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="table.xlsx">Download XLSX</a>'
    return href

# Load the data from the Excel file
data = pd.read_excel('FSSgenAI-usecases-app.xlsx', sheet_name='Sheet1')

# Extract the priority areas and FM capabilities from the data
priority_areas = data['Priority Area'].unique().tolist()
fm_capabilities = data['FM Capability'].unique().tolist()

# Add 'ALL' option to the priority areas and FM capabilities dropdowns
priority_areas.insert(0, 'ALL')
fm_capabilities.insert(0, 'ALL')

# Define the dropdown list selectors
selected_priority_area = st.sidebar.selectbox('Select Priority Area', priority_areas)
selected_fm_capability = st.sidebar.selectbox('Select FM Capability', fm_capabilities)

filtered_data = data[
    ((data['Priority Area'] == selected_priority_area) | (selected_priority_area == 'ALL')) &
    ((data['FM Capability'] == selected_fm_capability) | (selected_fm_capability == 'ALL'))
]

# Define the text input search
#search_input = st.sidebar.text_input('Search')

search_terms = st.sidebar.text_input("Search (separate terms with commas):").strip().split(",")
if search_terms:
    for term in search_terms:
        search_results = filtered_data.apply(lambda x: x.astype(str).str.contains(term.strip(), case=False)).any(axis=1)
        filtered_data = filtered_data[search_results]

# Perform search across all columns
#if search_input:
#    search_results = filtered_data.apply(lambda row: row.astype(str).str.contains(search_input, case=False).any(), axis=1)
#    filtered_data = filtered_data[search_results]

# Display the filtered data in a styled table with a neutral color scheme
st.header('Generative AI Use Cases')
if not filtered_data.empty:
    # Reset index to remove the default index count
    filtered_data.reset_index(drop=True, inplace=True)
else:
    st.write('No entries found matching the selected criteria.')

def apply_background_color(row):
    return ['background-color: #f2f2f2' if row.name % 2 != 0 else '' for _ in row]

styled_table = filtered_data.style \
    .set_properties(**{'background-color': 'white',
                       'color': 'black',
                       'text-align': 'left',
                       'border-color': 'white',
                       'white-space': 'pre-wrap'}) \
    .set_table_styles([{'selector': 'th',
                        'props': [('background-color', '#003e63'),
                                  ('color', 'white'),
                                  ('font-weight', 'bold'),
                                  ('text-align', 'left')]}]) \
    .apply(apply_background_color, axis=1)

# Display the styled table
st.dataframe(styled_table)

# Add a button to download the table in XLSX format
if len(filtered_data) > 0:
    st.sidebar.markdown("<h3 style='text-align: center;'>Download Table</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(get_table_download_link(filtered_data), unsafe_allow_html=True)


# Add a button to send email
st.sidebar.markdown('Send Email to cgorham@ibm.com and Trinh.Le@ibm.com with additional use case ideas, assets and to designate yourself a primary contact.')



