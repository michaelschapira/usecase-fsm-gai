import streamlit as st
import pandas as pd
import numpy as np
import smtplib

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

# Define the text input search
search_input = st.sidebar.text_input('Search')

# Filter the data based on the selected priority area, FM capability, and search input
filtered_data = data[
    ((data['Priority Area'] == selected_priority_area) | (selected_priority_area == 'ALL')) &
    ((data['FM Capability'] == selected_fm_capability) | (selected_fm_capability == 'ALL'))
]

# Perform search across all columns
if search_input:
    search_results = filtered_data.apply(lambda row: row.astype(str).str.contains(search_input, case=False).any(), axis=1)
    filtered_data = filtered_data[search_results]

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

# Add a button to send email
st.sidebar.markdown('Send Email to cgorham@ibm.com and Trinh.Le@ibm.com with additional use case ideas, assets and to designate yourself a primary contact.')



