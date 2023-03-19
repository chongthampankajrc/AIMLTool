import os

import streamlit as st
import pandas as pd
import numpy as np
st.markdown("<h3 style='text-align: center; color: Blue;'>Welcome to Data Engineering Tool! 👋</h3>", unsafe_allow_html=True)

temp_df = pd.DataFrame()
msg = ""
@st.cache_data  # 👈 Add the caching decorator
def load_data(path):
    df = pd.read_csv(path)
    return df

# st. set_page_config(layout="wide")
col1, col2 = st.columns(2)

st.sidebar.success("Generate the script!")

file1 = col1.file_uploader("Select left data")
file2 = col2.file_uploader("Select right data")
if file1:
    productivity_df = pd.read_csv(file1)
    col1.dataframe(productivity_df, width=600, height=200)

if file2:
    team_df = pd.read_csv(file2)
    # col2.markdown("##### Team Description")
    col2.dataframe(team_df, width=600, height=200)


if file1 and file2 is not None:
    add_selectbox = st.selectbox(
        'Select Operation',
        ('', 'JOIN', 'LEFT JOIN', 'AVERAGE', 'MERGE', 'AGGREGATE'))

    table1_columns = col1.selectbox('Select Column', tuple(['Select Column'] + list(productivity_df.columns)))
    table2_columns = col2.selectbox('Select Column', tuple(['Select Column'] + list(team_df.columns)))
    if add_selectbox == 'MERGE':
        msg = ""
        temp_df = pd.merge(productivity_df, team_df, left_on=table1_columns, right_on=table2_columns)
        # temp_df.to_csv('destination.csv', index=False)
    elif add_selectbox == 'JOIN':
        msg = 'Ops! This is not applicable for now'
    elif add_selectbox == 'RIGHT JOIN':
        msg = ""
        temp_df = pd.merge(productivity_df, team_df, how='right', )
    elif add_selectbox == 'AGGREGATE':
        msg = ""
        apply_table = st.selectbox(
            'Select Table',
            ('', 'Left', 'Right'))
        if apply_table == 'Left':
            group_by = st.selectbox(
                'Group By',
                tuple(list(productivity_df.columns)))
            apply_column = st.selectbox(
                'Column of',
                tuple(list(productivity_df.columns)))
            show_table = st.selectbox(
                'Aggregate on',
                ('', 'Right'))
            if show_table == 'Right':
                temp_df = team_df
                temp_df['Average'] = list(productivity_df.groupby(group_by)[apply_column].mean())
            elif show_table == 'Left':
                temp_df = productivity_df
                temp_df['Average'] = list(team_df.groupby(group_by)[apply_column].mean())
        elif apply_table == 'Right':
            group_by = st.selectbox(
                'Group By',
                tuple(list(team_df.columns)))
            apply_column = st.selectbox(
                'Column of',
                tuple(list(team_df.columns)))
            show_table = st.selectbox(
                'Aggregate on',
                ('', 'Left'))
            if show_table == 'Right':
                temp_df = team_df
                temp_df['Average'] = list(productivity_df.groupby(group_by)[apply_column].mean())
            elif show_table == 'Left':
                temp_df = productivity_df
                temp_df['Average'] = list(team_df.groupby(group_by)[apply_column].mean())

    agree = st.checkbox('Render')
    if agree:
        if len(msg) > 0:
            st.write(msg)
        else:
            st.dataframe(temp_df)
    if st.button("Generate"):
        if not os.path.exists('codegen'):
            os.makedirs('codegen')
        with open('codegen\\script.py', 'w') as f:
            f.write("import pandas as pd")
            f.write("\n")
            f.write('file1=r"{}\{}"'.format(os.getcwd(), file1.name))
            f.write("\n")
            f.write('file2=r"{}\{}"'.format(os.getcwd(), file2.name))
            f.write("\n")
            f.write("file1_column='{}'".format(table1_columns))
            f.write("\n")
            f.write("file2_column='{}'".format(table2_columns))
            f.write("\n")
            f.write(f"operation='{add_selectbox}'")
            f.write("\n")
            if add_selectbox == 'MERGE':
                f.write("if operation == 'MERGE':")
                f.write("\n")
                f.write("  left_table_df = pd.read_csv(file1)")
                f.write("\n")
                f.write("  right_table_df = pd.read_csv(file2)")
                f.write("\n")
                f.write("  temp_df = pd.merge(left_table_df, right_table_df, left_on=file1_column, right_on=file2_column)")
                f.write("\n")
                f.write("  temp_df.to_csv('destination.csv', index=False)")
                f.write("\n")
                f.write("  print('MERGE file [destination.csv] is generated ')")
        st.write("Script has successfully Generated!")
