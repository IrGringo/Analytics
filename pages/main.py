import streamlit as st


pg = st.navigation([st.Page("Home.py"),
                    st.Page("Financial_Dashboard.py"),
                    st.Page("Customer_Seasonality.py"),
                    st.Page("Customer_Behavior.py")])

pg.run()