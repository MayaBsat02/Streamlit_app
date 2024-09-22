import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('data.csv')

# Streamlit Page Title
st.title("Health and Covid-19 Data Visualization")

# Add a brief description
st.write("""
This page presents insights on three important datasets:
1. **Hypertension cases by town**.
2. **Covid-19 cases by top 10 towns**.
3. **Comparison of Covid-19 cases in towns with and without cardiovascular disease**.
Use the interactive features to explore the data.
""")

# Sidebar Interactivity
st.sidebar.header("Filter Options")

# Interaction Feature 1: Slider for Number of Covid-19 Cases for Clustered Bar Chart
min_cases, max_cases = int(df['Nb of Covid-19 cases'].min()), int(df['Nb of Covid-19 cases'].max())
selected_cases = st.sidebar.slider('Select Number of Covid-19 Cases', min_cases, max_cases, (min_cases, max_cases))

# Filter DataFrame for Covid-19 cases based on selected range
df_filtered_cases = df[(df['Nb of Covid-19 cases'] >= selected_cases[0]) & 
                       (df['Nb of Covid-19 cases'] <= selected_cases[1])]

# Interaction Feature 2: Checkbox for Hypertension Presence
hypertension_option = st.sidebar.radio('Filter Hypertension Cases', 
                                        ('Both', 'With Hypertension (1)', 'Without Hypertension (0)'))

# Filter for hypertension cases based on selection
if hypertension_option == 'With Hypertension (1)':
    df_filtered_cases = df_filtered_cases[df_filtered_cases['Existence of chronic diseases - Hypertension'] == 1]
elif hypertension_option == 'Without Hypertension (0)':
    df_filtered_cases = df_filtered_cases[df_filtered_cases['Existence of chronic diseases - Hypertension'] == 0]

# Interaction Feature 3: Slider for Number of Top Towns in Pie Chart
top_n = st.sidebar.slider('Number of Top Towns for Covid-19 Cases', 5, 20, 10)

# Section 1: Line Chart for Hypertension by Town
st.subheader("Hypertension Cases by Town")
fig_line = px.line(df_filtered_cases, x='Town', y='Existence of chronic diseases - Hypertension',
                   title='Hypertension Cases by Town')
st.plotly_chart(fig_line)

# Section 2: Pie Chart for Top Towns by Covid-19 Cases
df_sorted = df.sort_values(by='Nb of Covid-19 cases', ascending=False)
df_top = df_sorted.head(top_n)

st.subheader(f"Top {top_n} Towns by Number of Covid-19 Cases")
fig_top_pie = px.pie(df_top, names='Town', values='Nb of Covid-19 cases',
                     title=f'Top {top_n} Towns by Number of Covid-19 Cases')
st.plotly_chart(fig_top_pie)

# Section 3: Clustered Bar Chart for Covid-19 cases in towns with/without cardiovascular disease
st.subheader("Covid-19 Cases in Towns with and without Cardiovascular Disease")

# Filter and concatenate data based on the selected Covid-19 cases
df_with_disease = df_filtered_cases[df_filtered_cases['Existence of chronic diseases - Cardiovascular disease '] == 1]
df_without_disease = df_filtered_cases[df_filtered_cases['Existence of chronic diseases - Cardiovascular disease '] == 0]
df_combined = pd.concat([df_with_disease, df_without_disease])

# Create a clustered bar chart
fig_clustered_bar = px.bar(df_combined, x='Town', y='Nb of Covid-19 cases', 
                           color='Existence of chronic diseases - Cardiovascular disease ', 
                           barmode='group', 
                           title='Covid-19 Cases in Towns with and without Cardiovascular Disease')
st.plotly_chart(fig_clustered_bar)

# Additional insights or context
st.write("""
### Insights:
- **Hypertension Cases**: The line chart shows the distribution of hypertension cases in the selected town based on your filter.
- **Covid-19 Cases by Town**: The pie chart highlights the top towns with the highest number of Covid-19 cases.
- **Cardiovascular Disease and Covid-19**: The clustered bar chart shows how the presence of cardiovascular disease impacts the number of Covid-19 cases in various towns.
- When we filter on the top number of Covid-19 , we notice that the towns who have Hypertension Cases are the most affected by Covid and they are in fact top towns affected by Covid
""")
