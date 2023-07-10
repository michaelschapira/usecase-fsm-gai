import streamlit as st
import pandas as pd

# Load the data from the Excel file
data = pd.read_excel('FSSGenAI-usecases.xlsx', sheet_name='Sheet1')

# Extract the sales plays and priority areas from the data
sales_plays = data['Sales Play'].unique().tolist()
priority_areas = data['Priority Area'].unique().tolist()

# Add 'ALL' option to the sales plays and priority areas
sales_plays.insert(0, 'ALL')
priority_areas.insert(0, 'ALL')

# Define the dropdown list selectors
selected_sales_play = st.sidebar.selectbox('Select Sales Play', sales_plays)
selected_priority_area = st.sidebar.selectbox('Select Priority Area', priority_areas)

# Filter the data based on the selected dropdowns
filtered_data = data[
    ((data['Sales Play'] == selected_sales_play) | (selected_sales_play == 'ALL')) &
    ((data['Priority Area'] == selected_priority_area) | (selected_priority_area == 'ALL'))
]

# Display the filtered data in a table
st.header('Generative AI Use Cases')
if not filtered_data.empty:
    st.table(filtered_data[['Priority Area', 'Sales Play','Use Case', 'Description', 'LOB', 'Additional LOB']])
else:
    st.write('No entries found matching the selected criteria.')

