import streamlit as st
import pandas as pd

# Load the data from the Excel file
data = pd.read_excel('FSSgenAI-usecases.xlsx', sheet_name='Sheet1')

# Extract the sales plays and priority areas from the data
sales_plays = data['Sales Play'].unique().tolist()
priority_areas = data['Priority Area'].unique().tolist()

# Add 'ALL' option to the sales plays and priority areas
sales_plays.insert(0, 'ALL')
priority_areas.insert(0, 'ALL')

# Define the dropdown list selectors
selected_sales_play = st.sidebar.selectbox('Select Sales Play', sales_plays)
selected_priority_area = st.sidebar.selectbox('Select Priority Area', priority_areas)

# Define the text input search
search_input = st.sidebar.text_input('Search')

# Filter the data based on the selected dropdowns and search input
filtered_data = data[
    ((data['Sales Play'] == selected_sales_play) | (selected_sales_play == 'ALL')) &
    ((data['Priority Area'] == selected_priority_area) | (selected_priority_area == 'ALL')) &
    (data['Use Case'].str.contains(search_input, case=False))  # Filter based on search input
]

# Display the filtered data in a styled table with wrapped text
st.header('Generative AI Use Cases')
if not filtered_data.empty:
    styled_table = filtered_data[['Priority Area', 'Sales Play', 'Use Case', 'Description', 'LOB', 'Additional LOB']].style \
        .set_properties(**{'background-color': 'lightblue',
                           'color': 'black',
                           'text-align': 'left',
                           'border-color': 'white',
                           'white-space': 'pre-wrap'}) \
        .highlight_max(axis=0, color='yellow') \
        .highlight_min(axis=0, color='lightgreen') \
        .set_table_styles([{'selector': 'th',
                            'props': [('background-color', 'steelblue'),
                                      ('color', 'white'),
                                      ('font-weight', 'bold'),
                                      ('text-align', 'left')]}])
    st.dataframe(styled_table)
else:
    st.write('No entries found matching the selected criteria.')

