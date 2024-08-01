import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ydata profiling
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# ----------------CONFIG--------------
st.set_page_config(
    page_title="Credit Card Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------- Judul Dashboard
st.markdown("<h1 style='text-align: center;'> Credit Card Data Dashboard </h1>", unsafe_allow_html=True)
st.markdown("---")

# ------- Sidebar
with st.sidebar:
    st.subheader("Eligible Data")
    st.markdown("---")
    data_loaded = st.button("Start Credit Card Analysis")

if data_loaded:
    # Read Data
    conn = st.connection("gsheet", type=GSheetsConnection)
    df = conn.read(
        spreadsheet=st.secrets.gsheet_credit["spreadsheet"],
        worksheet=st.secrets.gsheet_credit["worksheet"]
    )
    
    # Summary statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Generate Profile Report
    st.subheader("Profile Report")
    pr = ProfileReport(df)
    st_profile_report(pr)

    # Plotly visualizations
    st.markdown("---")
    st.subheader("Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart of income types
        income_types = df['Income_type'].value_counts().reset_index()
        income_types.columns = ['Income Type', 'Count']
        fig1 = go.Figure(data=[
            go.Bar(name='Income Type', x=income_types['Income Type'], y=income_types['Count'])
        ])
        fig1.update_layout(title='Income Types', barmode='stack')
        st.plotly_chart(fig1)

    with col2:
        # Pie chart of education types
        education_types = df['Education_type'].value_counts().reset_index()
        education_types.columns = ['Education Type', 'Count']
        fig2 = go.Figure(data=[
            go.Pie(labels=education_types['Education Type'], values=education_types['Count'])
        ])
        fig2.update_layout(title='Education Types')
        st.plotly_chart(fig2)

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        # Mixed chart of total income over age
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])

        # Bar chart for total income
        fig3.add_trace(
            go.Bar(x=df['Age'], y=df['Total_income'], name='Total Income'),
            secondary_y=False
        )

        # Line chart for total income average (example calculation)
        avg_income = df.groupby('Age')['Total_income'].mean().reset_index()
        fig3.add_trace(
            go.Scatter(x=avg_income['Age'], y=avg_income['Total_income'], mode='lines', name='Average Income'),
            secondary_y=True
        )

        fig3.update_layout(
            title='Total Income over Age',
            xaxis_title='Age',
            yaxis_title='Total Income',
            yaxis2_title='Average Income'
        )
        st.plotly_chart(fig3)

    with col4:
        # Box plot of total income by family status
        fig4 = go.Figure(data=[
            go.Box(y=df['Total_income'], x=df['Family_status'], name='Total Income by Family Status')
        ])
        fig4.update_layout(title='Total Income by Family Status', xaxis_title='Family Status', yaxis_title='Total Income')
        st.plotly_chart(fig4)

else:
    st.info("Click the button in the left sidebar to load and visualize the data.")
