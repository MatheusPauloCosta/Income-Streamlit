import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

from scipy.stats import mstats

sns.set(context='talk', style='ticks')

st.set_page_config(
     page_title="Income Prediction",
     page_icon=":?:",
     layout="wide",
)

st.write('# Exploratory Analysis of Income Prediction')

st.write('## Business Understanding')

st.write("Examine how income interacts with other factors like property and vehicle ownership to identify customer profiles with high potential for a credit limit increase.")

#read data
renda = pd.read_csv('./input/previsao_de_renda.csv')
renda.drop('Unnamed: 0', axis=1, inplace=True)
#outliers with winsorization

colunas_renomeadas = {
    'data_ref': 'reference_date',
    'id_cliente': 'client_id',
    'sexo': 'gender',
    'posse_de_veiculo': 'vehicle_ownership',
    'posse_de_imovel': 'property_ownership',
    'qtd_filhos': 'number_of_children',
    'tipo_renda': 'income_type',
    'educacao': 'education',
    'estado_civil': 'marital_status',
    'tipo_residencia': 'residence_type',
    'idade': 'age',
    'tempo_emprego': 'employment_duration',
    'qt_pessoas_residencia': 'number_of_household_members',
    'renda': 'income'
}

data = {
    "Column Name": [
        "reference_date", "client_id", "gender", "vehicle_ownership", 
        "property_ownership", "number_of_children", "income_type", 
        "education", "marital_status", "residence_type", "age", 
        "employment_duration", "number_of_household_members", "income"
    ],
    "Description": [
        "The reference date for the information or transactions.",
        "Unique identifier of the client.",
        "Client's gender (M for male, F for female).",
        "Indicates whether the client owns a vehicle (1 for yes, 0 for no).",
        "Indicates whether the client owns a property (1 for yes, 0 for no).",
        "Number of children the client has.",
        "Client's income type (e.g., salaried, self-employed, etc.).",
        "Client's education level (e.g., high school, college degree, etc.).",
        "Client's marital status (e.g., single, married, etc.).",
        "Client's residence type (e.g., rented, owned, etc.).",
        "Client's age.",
        "Client's current employment duration (in years).",
        "Number of people living in the client's household.",
        "Client's monthly income."
    ]
}


df = pd.DataFrame(data)

# Showing the desscription
st.write("### Client Dataset - Column Descriptions")
st.dataframe(df)

# Renaming the columns
renda.rename(columns=colunas_renomeadas, inplace=True)

# Winsorizing the 'income' column
renda['income'] = mstats.winsorize(renda['income'], limits=[0, 0.05])

# Filling missing values with mean for 'employment_duration'
renda['employment_duration'].fillna(renda['employment_duration'].mean(), inplace=True)

option = st.selectbox(
     'Select what you want see:',
     ('Data','Show graphs over time', 'Show Bivariate Graphs', 'Show custom graphs'))

if option == 'Data':
     st.dataframe(renda)

if option == 'Show graphs over time':
     # Plots
     fig, ax = plt.subplots(6, 1, figsize=(20, 80))
     renda[['property_ownership', 'income']].plot(kind='hist', ax=ax[0])
     st.write('## Graphs Over Time')
     sns.lineplot(x='reference_date', y='income', hue='vehicle_ownership', data=renda, ax=ax[1])
     ax[1].tick_params(axis='x', rotation=45)
     sns.lineplot(x='reference_date', y='income', hue='income_type', data=renda, ax=ax[2])
     ax[2].tick_params(axis='x', rotation=45)
     sns.lineplot(x='reference_date', y='income', hue='education', data=renda, ax=ax[3])
     ax[3].tick_params(axis='x', rotation=45)
     sns.lineplot(x='reference_date', y='income', hue='marital_status', data=renda, ax=ax[4])
     ax[4].tick_params(axis='x', rotation=45)
     sns.lineplot(x='reference_date', y='income', hue='residence_type', data=renda, ax=ax[5])
     ax[5].tick_params(axis='x', rotation=45)
     sns.despine()

     plt.subplots_adjust(hspace=0.9)
     st.pyplot(plt)

elif option == 'Show Bivariate Graphs':
     st.write('## Bivariate Graphs')
     fig, ax = plt.subplots(7, 1, figsize=(10, 50))
     sns.barplot(x='property_ownership', y='income', data=renda, ax=ax[0])
     ax[0].tick_params(axis='x', rotation=45) 

     sns.barplot(x='vehicle_ownership', y='income', data=renda, ax=ax[1])
     ax[1].tick_params(axis='x', rotation=45) 

     sns.barplot(x='number_of_children', y='income', data=renda, ax=ax[2])
     ax[2].tick_params(axis='x', rotation=45) 

     sns.barplot(x='income_type', y='income', data=renda, ax=ax[3])
     ax[3].tick_params(axis='x', rotation=45) 

     sns.barplot(x='education', y='income', data=renda, ax=ax[4])
     ax[4].tick_params(axis='x', rotation=45) 

     sns.barplot(x='marital_status', y='income', data=renda, ax=ax[5])
     ax[5].tick_params(axis='x', rotation=45)  

     sns.barplot(x='residence_type', y='income', data=renda, ax=ax[6])
     ax[6].tick_params(axis='x', rotation=45) 
     sns.despine()
     plt.subplots_adjust(hspace=0.9)
     st.pyplot(plt)

elif option == 'Show custom graphs':
     # Define the available columns for plotting
     columns = [
     "reference_date", "client_id", "gender", "vehicle_ownership", 
     "property_ownership", "number_of_children", "income_type", 
     "education", "marital_status", "residence_type", "age", 
     "employment_duration", "number_of_household_members", "income"
     ]


     st.write("## Create Your Custom Graph")

     # Dropdown to select columns for the graph
     x_axis = st.selectbox("Select the X-axis column", columns)
     y_axis = st.selectbox("Select the Y-axis column", columns)
     graph_type = st.selectbox("Select the graph type", ["Scatter Plot", "Bar Plot", "Line Plot"])

     # Option to rotate X-axis labels
     rotation_angle = st.slider("Adjust X-axis label rotation", min_value=0, max_value=90, value=45)

     # Optional category (hue)
     hue = st.selectbox("Select a category for grouping (optional)", [None] + columns)

     # Button to generate graph
     if st.button("Generate Graph"):
          fig, ax = plt.subplots()  # Create a new figure and axis for each graph

          # Generate the graph based on user selection
          if graph_type == "Scatter Plot":
               sns.scatterplot(data=renda, x=x_axis, y=y_axis, hue=hue, ax=ax)
          elif graph_type == "Bar Plot":
               sns.barplot(data=renda, x=x_axis, y=y_axis, hue=hue, ax=ax)
          elif graph_type == "Line Plot":
               sns.lineplot(data=renda, x=x_axis, y=y_axis, hue=hue, ax=ax)

          # Adjust rotation of X-axis labels
          ax.tick_params(axis='x', rotation=rotation_angle)

          # Display the graph
          st.pyplot(fig)