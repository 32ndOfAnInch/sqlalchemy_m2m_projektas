# libraries

import PySimpleGUI as sg
from datetime import datetime
from typing import Any
from sqlalchemy import create_engine, Integer, String, Float, DateTime, Table, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Session, relationship
import backend as bke

# creating db and declaring session
engine = create_engine('sqlite:///home_accounting.db')
session = sessionmaker(bind=engine)()

# declarative base
class Base(DeclarativeBase):
    pass


# jei iseis padaryti dali funkcionalumo meniu eiluteje virsuje, pvz ten idet exit
layout_left = [[sg.Button("Select User", key="-SELECT_USER-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
          [sg.Button("New User", key="-NEW_USER-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Delete User", key="-DELETE_USER-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Edit User Info", key="-EDIT_USER-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Show General Accounting", key="-SHOW_G_ACC-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Text("", pad=(10, 90))],
          [sg.Text("", pad=(10, 90))],
          [sg.Button("Exit program", key="-EXIT-", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20)]]

user_list = []
user_items_list = []
general_items_list = []
user_list_headings = ['ID', 'First Name', 'Last Name', "Username"]
headings_user = ['ID', 'TipasVeliau', 'Amount', 'PaskirtisVeliau', 'Comment', 'Data']
headings_general = ['ID', 'User Name', 'TipasVeliau', 'Amount', 'PaskirtisVeliau', 'Comment', 'Data']


layout_user_table = [[sg.Table(values=user_items_list, headings=headings_user,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=11,
                    key='-USER_ITEMS_TABLE-',
                    row_height=32,
                    enable_events=True,
                    alternating_row_color="#460c1f",
                    background_color="#271d20",
                    font=20,
                    selected_row_colors="white on black"
                    )],
            [sg.Text('ID', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_ID-', pad=(0, 10), font=20, disabled=True),
             sg.Text('Type', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_TYPE-', pad=(0, 10), font=20, disabled=True)],
            [sg.Text('Amount', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_AMOUNT-', pad=(0, 10), font=20), 
             sg.Button("Irasyti pajamas", key="-redaguoti-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Category', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_CATEGORY-', pad=(0, 10), font=20),
             sg.Button("Istrinti irasa", key="-redaguoti-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Comment', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_COMMENT-', pad=(0, 10), font=20)],
            [sg.Text('Date', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_DATE-', pad=(0, 10), font=20)],
            [sg.Button("Isvalyti laukus", key="-CLEAR-", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20)],
            [sg.Button("Uzdaryti lentele", key="-close-", button_color="#23277b", pad=10, size=(25, 1), font=20),
             sg.Button("Create a Record", key="-NEW_RECORD-", button_color="#23277b", pad=10, size=(25, 1), font=20)]
    ]

layout_general_table = [[sg.Table(values=user_items_list, headings=headings_general,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=11,
                    key='-GENERAL_ITEMS_TABLE-',
                    row_height=32,
                    enable_events=True,
                    alternating_row_color="#460c1f",
                    background_color="#271d20",
                    font=20,
                    selected_row_colors="white on black"
                    )],
            [sg.Text('ID', size=10, font=20), sg.Input(default_text="", enable_events=True, key='', pad=(0, 10), font=20, disabled=True),
             sg.Text('Type', size=10, font=20), sg.Input(default_text="", enable_events=True, key='', pad=(0, 10), font=20, disabled=True)],
            [sg.Text('Amount', size=10, font=20), sg.Input(default_text="", enable_events=True, key='', pad=(0, 10), font=20), 
             sg.Button("Irasyti pajamas", key="", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Category', size=10, font=20), sg.Input(default_text="", enable_events=True, key='', pad=(0, 10), font=20),
             sg.Button("Istrinti irasa", key="", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Comment', size=10, font=20), sg.Input(default_text="", enable_events=True, key='', pad=(0, 10), font=20)],
            [sg.Text('Date', size=10, font=20), sg.Input(default_text="", enable_events=True, key='', pad=(0, 10), font=20)],
            [sg.Button("Isvalyti laukus", key="", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20)],
            [sg.Button("Uzdaryti lentele", key="", button_color="#23277b", pad=10, size=(25, 1), font=20),
             sg.Button("Create a Record", key="", button_color="#23277b", pad=10, size=(25, 1), font=20)]
    ]

layout_select_user = [[sg.Table(values=user_list, headings=user_list_headings,
                    auto_size_columns=False,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=5,
                    key='-USER_LIST_TABLE-',
                    row_height=40,
                    enable_events=True,
                    alternating_row_color="#460c1f",
                    background_color="#271d20",
                    font=20,
                    selected_row_colors="white on black"
                    )],
            [sg.Text('User ID', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_LIST_ID-', pad=(0, 10), font=20, disabled=True)],
            [sg.Text('First Name', size=10, font=20), sg.Input(default_text="", key='-USER_LIST_F_NAME-', pad=(0, 10), font=20, disabled=True)],
            [sg.Text('Last Name', size=10, font=20), sg.Input(default_text="", key='-USER_LIST_L_NAME-', pad=(0, 10), font=20, disabled=True)],
            [sg.Text('User Name', size=10, font=20), sg.Input(default_text="", key='-USER_LIST_USER_NAME-', pad=(0, 10), font=20, disabled=True)],
            [sg.Button("Select User", key="-SELECT_USER_FROM_LIST-", button_color="#23277b", pad=10, size=(25, 1), font=20),
             sg.Button("Cancel", key="-CLOSE-", button_color="#23277b", pad=10, size=(25, 1), font=20)]
]

layout_new_user = [[sg.Text('First Name', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-NEW_F_NAME-', pad=(0, 10), font=20)],
            [sg.Text('Last Name', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-NEW_L_NAME-', pad=(0, 10), font=20)],
            [sg.Text('User Name', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-NEW_USER_NAME-', pad=(0, 10), font=20)],
            [sg.Button("Create User", key="-CREATE_USER-", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20),
             sg.Button("Cancel", key="-CLOSE2-", button_color="#23277b", pad=10, size=(25, 1), font=20)]
]

layout_delete_user = [[sg.Table(values=user_list, headings=user_list_headings,
                    auto_size_columns=False,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=5,
                    key='-USER_DELETE_TABLE-',
                    row_height=40,
                    enable_events=True,
                    alternating_row_color="#460c1f",
                    background_color="#271d20",
                    font=20,
                    selected_row_colors="white on black"
                    )],
                    [sg.Text('ID', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-DELETE_ID-', pad=(0, 10), font=20)],
                    [sg.Button("Delete User", key="-DELETE_USER_FROM_LIST-", button_color="#23277b", pad=10, size=(25, 1), font=20),
                    sg.Button("Cancel", key="-CLOSE3-", button_color="#23277b", pad=10, size=(25, 1), font=20)]
]


def close_all_right_windows():
    window["-NEW_USER_LAYOUT-"].update(visible=False)
    window["-GENERAL_TABLE_LAYOUT-"].update(visible=False)
    window["-SELECT_USER_LAYOUT-"].update(visible=False)
    window["-USER_TABLE_LAYOUT-"].update(visible=False)
    window["-DELETE_USER_LAYOUT-"].update(visible=False)
    

def refresh_user_table():
    user_list = bke.query_user(session)
    window['-USER_LIST_TABLE-'].update(values=user_list)

def refresh_delete_table():
    user_list = bke.query_user(session)
    window['-USER_DELETE_TABLE-'].update(values=user_list)

def refresh_listings_table():
    user_items_list = bke.query_user_items(session, saved_user_id)
    window['-USER_ITEMS_TABLE-'].update(values=user_items_list)

def clear_layout_user_table_inputs():
    window['-USER_TABLE_ID-'].update(value="")
    window['-USER_TABLE_TYPE-'].update(value="")
    window['-USER_TABLE_AMOUNT-'].update(value="")
    window['-USER_TABLE_CATEGORY-'].update(value="")
    window['-USER_TABLE_COMMENT-'].update(value="")
    window['-USER_TABLE_DATE-'].update(value="")


layout = [[sg.Col(layout_left, p=0, key="_LEFT_SIDE_LAYOUT_"), 
           sg.Col(layout_user_table, p=0, visible=False, key="-USER_TABLE_LAYOUT-"),
           sg.Col(layout_general_table, p=0, visible=False, key="-GENERAL_TABLE_LAYOUT-"), 
           sg.Col(layout_select_user, p=0, visible=False, key="-SELECT_USER_LAYOUT-"),
           sg.Col(layout_new_user, p=0, visible=False, key="-NEW_USER_LAYOUT-"),
           sg.Col(layout_delete_user, p=0, visible=False, key="-DELETE_USER_LAYOUT-")]]

window = sg.Window("Home Accounting", layout, size=(1280, 720))

while True:
    event, values = window.read()

    if event == "-NEW_USER-":
        close_all_right_windows()
        clear_layout_user_table_inputs()
        window["-NEW_USER_LAYOUT-"].update(visible=True)

    if event == "-CREATE_USER-":
        first_name = window['-NEW_F_NAME-'].get()
        last_name = window['-NEW_L_NAME-'].get()
        user_name = window['-NEW_USER_NAME-'].get()
        bke.create_user(first_name, last_name, user_name)
        window["-NEW_USER_LAYOUT-"].update(visible=False)


    if event == "-DELETE_USER-":
        close_all_right_windows()
        clear_layout_user_table_inputs()
        window["-DELETE_USER_LAYOUT-"].update(visible=True)
        user_list = bke.query_user(session)
        window['-USER_DELETE_TABLE-'].update(values=user_list)

    if event == "-DELETE_USER_FROM_LIST-":
        try:
            del_id = window['-DELETE_ID-'].get()
            bke.delete_user(session, del_id)
            refresh_delete_table()
            sg.popup_notify(f"User (ID: {del_id}) and their records are successfully deleted from list")
        except Exception as e:
            print(e)
            pass


    if event == "-USER_LIST_TABLE-":
        try:
            row_value = values['-USER_LIST_TABLE-'][0]
            values = bke.select_from_user_list_table(session, row_value)
            window['-USER_LIST_ID-'].update(value=values[0])
            window['-USER_LIST_F_NAME-'].update(value=values[1])
            window['-USER_LIST_L_NAME-'].update(value=values[2])
            window['-USER_LIST_USER_NAME-'].update(value=values[3])
        except Exception as e:
            print(e)
            pass

    if event == "-SELECT_USER-":
        close_all_right_windows()
        clear_layout_user_table_inputs()
        window["-SELECT_USER_LAYOUT-"].update(visible=True)
        user_list = bke.query_user(session)
        window['-USER_LIST_TABLE-'].update(values=user_list)

    if event == "-SELECT_USER_FROM_LIST-":
        select_user_id = window['-USER_LIST_ID-'].get()
        saved_user_id = select_user_id
        close_all_right_windows()
        window["-USER_TABLE_LAYOUT-"].update(visible=True)
        user_items_list = bke.query_user_items(session, saved_user_id)
        window["-USER_ITEMS_TABLE-"].update(values=user_items_list)
 
    if event == "-CLOSE-":
        close_all_right_windows()

    if event == "-CLOSE2-":
        close_all_right_windows()

    if event == "-CLOSE3-":
        close_all_right_windows()

    if event == "-USER_ITEMS_TABLE-":
        try:
            row_value = values['-USER_ITEMS_TABLE-'][0]
            values_user_table = bke.select_from_user_listings_table(session, row_value, saved_user_id)
            window['-USER_TABLE_ID-'].update(value=values_user_table[0])
            window['-USER_TABLE_TYPE-'].update(value="PLACEHOLDER")
            window['-USER_TABLE_AMOUNT-'].update(value=values_user_table[1])
            window['-USER_TABLE_CATEGORY-'].update(value="PLACEHOLDER")
            window['-USER_TABLE_COMMENT-'].update(value=values_user_table[2])
            window['-USER_TABLE_DATE-'].update(value=values_user_table[3])
        except IndexError:
            pass
    

    if event == "-NEW_RECORD-":
        amount = window['-USER_TABLE_AMOUNT-'].get()
        comment = window['-USER_TABLE_COMMENT-'].get()
        bke.insert_new_record(amount, comment, saved_user_id)
        refresh_listings_table()
        clear_layout_user_table_inputs()

    if event == "-SHOW_G_ACC-":
        close_all_right_windows()
        window["-GENERAL_TABLE_LAYOUT-"].update(visible=True)
        general_items_list = bke.query_all_items(session)
        window["-GENERAL_ITEMS_TABLE-"].update(values=general_items_list)


    if event == "-CLEAR-":
        pass
        # isvalyti laukelius
        #clear_inputs()

    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        break

window.close()

