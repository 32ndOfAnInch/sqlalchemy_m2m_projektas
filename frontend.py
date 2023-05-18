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


# tables work horribly on pysimplegui, spreadsheets needed to be used instead
layout_left = [[sg.Button("Select User", key="-SELECT_USER-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
          [sg.Button("New User", key="-NEW_USER-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Delete User", key="-DELETE_USER-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Edit User Info", key="-EDIT_USER-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Show General Accounting", key="-SHOW_G_ACC-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Settings", key="-SETTINGS-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Text("", pad=(10, 80))],
          [sg.Text("", pad=(10, 80))],
          [sg.Button("Exit program", key="-EXIT-", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20)]]

user_list = []
user_items_list = []
general_items_list = []
user_list_headings = ['ID', 'First Name', 'Last Name', "Username"]
headings_user = ['ID', 'Type', 'Amount', 'Category', 'Comment', 'Data']
headings_general = ['ID', 'User Name', 'Type', 'Amount', 'Category', 'Comment', 'Data']


layout_user_table = [[sg.Table(values=user_items_list, headings=headings_user,
                    auto_size_columns=False,
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
            [sg.Text('ID', size=10, font=20, text_color="#b7b5b7"), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_ID-', pad=(0, 2), font=20, disabled=True)],
            [sg.Button("Edit Record", key="-CLEAR-", button_color="#23277b", pad=5, size=(25, 1), font=20),
             sg.Button("Delete Record", key="-DELETE_RECORD-", button_color="#23277b", pad=5, size=(25, 1), font=20)],
            [
             sg.Button("Add New Earnings Record", key="-NEW_EARNING_RECORD-", button_color="#23277b", pad=(5, 25), size=(25, 1), font=20),
             sg.Button("Add New Expenses Record", key="-NEW_EXPENSES_RECORD-", button_color="#23277b", pad=(5, 25), size=(25, 1), font=20)],
            [sg.Button("Close Table", key="-CLOSE_USER_ITEMS_TABLE-", button_color="#23277b", pad=5, size=(25, 1), font=20)]
    ]

layout_user_earnings = [[sg.Text('Create earnings record', font=36)],
            [sg.Text('Amount', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_AMOUNT_EARNINGS-', pad=(0, 2), font=20)],
            [sg.Text('Category', size=10, font=20), sg.Combo(values=bke.populate_earnings_category_combo(), enable_events=True, key='-USER_TABLE_CATEGORY_EARNINGS-', pad=(0, 2), font=20)],
            [sg.Text('Comment', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_COMMENT_EARNINGS-', pad=(0, 2), font=20)],
            [
             sg.Button("Add New Record", key="-INSERT_EARNINGS_RECORD-", button_color="#23277b", pad=5, size=(25, 1), font=20)]
    ]

layout_user_spendings = [[sg.Text('Create expenses record', font=36)],
            [sg.Text('Amount', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_AMOUNT_SPENDINGS-', pad=(0, 2), font=20)],
            [sg.Text('Category', size=10, font=20), sg.Combo(values=bke.populate_expenses_category_combo(), enable_events=True, key='-USER_TABLE_CATEGORY_SPENDINGS-', pad=(0, 2), font=20)],
            [sg.Text('Comment', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-USER_TABLE_COMMENT_SPENDINGS-', pad=(0, 2), font=20)],
            [
             sg.Button("Add New Record", key="-INSERT_EXPENSES_RECORD-", button_color="#23277b", pad=5, size=(25, 1), font=20)]
    ]

layout_general_table = [[sg.Table(values=user_items_list, headings=headings_general,
                    auto_size_columns=False,
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
            [sg.Button("Close", key="-CLOSE5-", button_color="#23277b", pad=10, size=(25, 1), font=20)]
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

layout_edit_user = [[sg.Table(values=user_list, headings=user_list_headings,
                    auto_size_columns=False,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=5,
                    key='-USER_EDIT_TABLE-',
                    row_height=40,
                    enable_events=True,
                    alternating_row_color="#460c1f",
                    background_color="#271d20",
                    font=20,
                    selected_row_colors="white on black"
                    )],
            [sg.Text('User ID', size=10, font=20, text_color="#b7b5b7"), sg.Input(default_text="", enable_events=True, key='-USER_EDIT_ID-', pad=(0, 10), font=20, text_color="#555555", disabled=True)],
            [sg.Text('First Name', size=10, font=20), sg.Input(default_text="", key='-USER_EDIT_F_NAME-', pad=(0, 10), font=20)],
            [sg.Text('Last Name', size=10, font=20), sg.Input(default_text="", key='-USER_EDIT_L_NAME-', pad=(0, 10), font=20)],
            [sg.Text('User Name', size=10, font=20), sg.Input(default_text="", key='-USER_EDIT_USER_NAME-', pad=(0, 10), font=20)],
            [sg.Button("Edit User", key="-EDIT_USER_FROM_LIST-", button_color="#23277b", pad=10, size=(25, 1), font=20),
             sg.Button("Cancel", key="-CLOSE4-", button_color="#23277b", pad=10, size=(25, 1), font=20)]
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

layout = [[sg.Col(layout_left, p=0, key="_LEFT_SIDE_LAYOUT_"), 
           sg.Col(layout_user_table, p=0, visible=False, key="-USER_TABLE_LAYOUT-"),
           sg.Col(layout_general_table, p=0, visible=False, key="-GENERAL_TABLE_LAYOUT-"), 
           sg.Col(layout_select_user, p=0, visible=False, key="-SELECT_USER_LAYOUT-"),
           sg.Col(layout_edit_user, p=0, visible=False, key="-EDIT_USER_LAYOUT-"),
           sg.Col(layout_new_user, p=0, visible=False, key="-NEW_USER_LAYOUT-"),
           sg.Col(layout_user_earnings, p=0, visible=False, key="-INSERT_EARNINGS_LAYOUT-"),
           sg.Col(layout_user_spendings, p=0, visible=False, key="-INSERT_SPENDINGS_LAYOUT-"),
           sg.Col(layout_delete_user, p=0, visible=False, key="-DELETE_USER_LAYOUT-")]]

window = sg.Window("Home Accounting", layout, size=(1280, 720))



## Functions with GUI

def close_all_right_windows():
    window["-NEW_USER_LAYOUT-"].update(visible=False)
    window["-GENERAL_TABLE_LAYOUT-"].update(visible=False)
    window["-SELECT_USER_LAYOUT-"].update(visible=False)
    window["-EDIT_USER_LAYOUT-"].update(visible=False)
    window["-USER_TABLE_LAYOUT-"].update(visible=False)
    window["-DELETE_USER_LAYOUT-"].update(visible=False)
    

def refresh_user_table():
    user_list = bke.query_user(session)
    window['-USER_EDIT_TABLE-'].update(values=user_list)

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

def update_user_items_table():
    window["-USER_TABLE_LAYOUT-"].update(visible=True)
    user_items_list = bke.query_user_items(session, saved_user_id)
    window["-USER_ITEMS_TABLE-"].update(values=user_items_list)

while True:
    event, values = window.read()

    if event == "-NEW_USER-":
        close_all_right_windows()
        #clear_layout_user_table_inputs()
        window["-NEW_USER_LAYOUT-"].update(visible=True)

    if event == "-CREATE_USER-":
        first_name = window['-NEW_F_NAME-'].get()
        last_name = window['-NEW_L_NAME-'].get()
        user_name = window['-NEW_USER_NAME-'].get()
        bke.create_user(first_name, last_name, user_name)
        window["-NEW_USER_LAYOUT-"].update(visible=False)


    if event == "-DELETE_USER-":
        close_all_right_windows()
        #clear_layout_user_table_inputs()
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
        #clear_layout_user_table_inputs()
        window["-SELECT_USER_LAYOUT-"].update(visible=True)
        user_list = bke.query_user(session)
        window['-USER_LIST_TABLE-'].update(values=user_list)

    if event == "-SELECT_USER_FROM_LIST-":
        select_user_id = window['-USER_LIST_ID-'].get()
        saved_user_id = select_user_id
        close_all_right_windows()
        update_user_items_table()

    if event == "-USER_EDIT_TABLE-":
        try:
            row_value = values['-USER_EDIT_TABLE-'][0]
            values = bke.select_from_user_list_table(session, row_value)
            window['-USER_EDIT_ID-'].update(value=values[0])
            window['-USER_EDIT_F_NAME-'].update(value=values[1])
            window['-USER_EDIT_L_NAME-'].update(value=values[2])
            window['-USER_EDIT_USER_NAME-'].update(value=values[3])
        except Exception as e:
            print(e)
            pass

    if event == "-EDIT_USER-":
        close_all_right_windows()
        window["-EDIT_USER_LAYOUT-"].update(visible=True)
        user_list = bke.query_user(session)
        window['-USER_EDIT_TABLE-'].update(values=user_list)

    if event == "-EDIT_USER_FROM_LIST-":
        edit_user_from_id = window['-USER_EDIT_ID-'].get()
        edit_user_f_name = window['-USER_EDIT_F_NAME-'].get()
        edit_user_l_name = window['-USER_EDIT_L_NAME-'].get()
        edit_user_name = window['-USER_EDIT_USER_NAME-'].get()
        bke.edit_user(edit_user_from_id, edit_user_f_name, edit_user_l_name, edit_user_name)
        refresh_user_table()
 
    if event == "-CLOSE-":
        close_all_right_windows()

    if event == "-CLOSE2-":
        close_all_right_windows()

    if event == "-CLOSE3-":
        close_all_right_windows()

    if event == "-CLOSE4-":
        close_all_right_windows()

    if event == "-CLOSE5-":
        close_all_right_windows()

    if event == "-USER_ITEMS_TABLE-":
        try:
            row_value = values['-USER_ITEMS_TABLE-'][0]
            values_user_table = bke.select_from_user_listings_table(session, row_value, saved_user_id)
            window['-USER_TABLE_ID-'].update(value=values_user_table[0])
        except IndexError:
            pass
    

    if event == "-NEW_EARNING_RECORD-":
        close_all_right_windows()
        window["-INSERT_EARNINGS_LAYOUT-"].update(visible=True)

    if event == "-INSERT_EARNINGS_RECORD-":
        earnings_amount = window['-USER_TABLE_AMOUNT_EARNINGS-'].get()
        earnings_category_id = window['-USER_TABLE_CATEGORY_EARNINGS-'].get()[0]
        earnings_comment = window['-USER_TABLE_COMMENT_EARNINGS-'].get()
        earnings_type_id = 1 # mechanically declaring, 1 for earnings, it is temporary
        bke.insert_earnings_record(saved_user_id, earnings_type_id, earnings_amount, earnings_category_id, earnings_comment)
        window["-INSERT_EARNINGS_LAYOUT-"].update(visible=False)
        update_user_items_table()

    if event == "-NEW_EXPENSES_RECORD-":
        close_all_right_windows()
        window["-INSERT_SPENDINGS_LAYOUT-"].update(visible=True)

    if event == "-INSERT_EXPENSES_RECORD-":
        spendings_amount = window['-USER_TABLE_AMOUNT_SPENDINGS-'].get()
        spendings_category_id = window['-USER_TABLE_CATEGORY_SPENDINGS-'].get()[0]
        spendings_comment = window['-USER_TABLE_COMMENT_SPENDINGS-'].get()
        spendings_type_id = 2 # mechanically declaring, 2 for expenses(spendings), it is temporary
        bke.insert_spendings_record(saved_user_id, spendings_type_id, spendings_amount, spendings_category_id, spendings_comment)
        window["-INSERT_SPENDINGS_LAYOUT-"].update(visible=False)
        update_user_items_table()

    if event == "-CLOSE_USER_ITEMS_TABLE-":
        close_all_right_windows()

    if event == "-SHOW_G_ACC-":
        close_all_right_windows()
        window["-GENERAL_TABLE_LAYOUT-"].update(visible=True)
        general_items_list = bke.query_all_items(session)
        window["-GENERAL_ITEMS_TABLE-"].update(values=general_items_list)


    if event == "-DELETE_RECORD-":
        delete_item_id = window['-USER_TABLE_ID-'].get()
        bke.delete_item(delete_item_id)
        update_user_items_table()


    if event == "-CLEAR-":
        pass
        # isvalyti laukelius
        #clear_inputs()

    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        break

window.close()

