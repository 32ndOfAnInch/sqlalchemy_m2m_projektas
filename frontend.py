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
          [sg.Button("Nustatymai", key="-atleisti-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Button("Show General Accounting", key="-SHOW_G_ACC-", button_color="#7a223f", pad=10, size=(25, 1), font=20)],
          [sg.Text("", pad=(10, 90))],
          [sg.Text("", pad=(10, 90))],
          [sg.Button("Exit program", key="-EXIT-", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20)]]

user_list = []
user_list_headings = ['ID', 'First Name', 'Last Name']
darbuotojai_list = []
headings = ['ID', 'Vartotojas', 'Tipas', 'Suma', 'Paskirtis', 'Komentaras', 'Data']
headings_vart = ['ID', 'Vardas', 'Pavarde']

layout_user_table = [[sg.Table(values=darbuotojai_list, headings=headings,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=11,
                    key='-TABLE-',
                    row_height=32,
                    enable_events=True,
                    alternating_row_color="#460c1f",
                    background_color="#271d20",
                    font=20,
                    selected_row_colors="white on black"
                    )],
            [sg.Text('ID', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-ID-', pad=(0, 10), font=20, disabled=True),
             sg.Button("Irasyti islaidas", key="-irasyti-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Suma', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-VARDAS-', pad=(0, 10), font=20), 
             sg.Button("Irasyti pajamas", key="-redaguoti-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Paskirtis', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-PAVARDE-', pad=(0, 10), font=20),
             sg.Button("Istrinti irasa", key="-redaguoti-", button_color="#23277b", pad=10, size=(25, 1), font=20)],
            [sg.Text('Komentaras', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-GIMIMAS-', pad=(0, 10), font=20)],
            [sg.Text('Data', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-PAREIGOS-', pad=(0, 10), font=20)],
            [sg.Button("Isvalyti laukus", key="-CLEAR-", button_color="#23277b", pad=(10, 10), size=(25, 1), font=20)],
            [sg.Button("Uzdaryti lentele", key="-close-", button_color="#23277b", pad=10, size=(25, 1), font=20)]
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
            [sg.Button("Select User", key="-SELECT_USER_FROM_LIST-", button_color="#23277b", pad=10, size=(25, 1), font=20),
             sg.Button("Cancel", key="-CLOSE-", button_color="#23277b", pad=10, size=(25, 1), font=20)]
]

layout_new_user = [[sg.Text('First Name', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-NEW_F_NAME-', pad=(0, 10), font=20)],
            [sg.Text('Last Name', size=10, font=20), sg.Input(default_text="", enable_events=True, key='-NEW_L_NAME-', pad=(0, 10), font=20)],
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
    window["-SELECT_USER_LAYOUT-"].update(visible=False)
    window["-USER_TABLE_LAYOUT-"].update(visible=False)
    window["-DELETE_USER_LAYOUT-"].update(visible=False)

def refresh_user_table():
    user_list = bke.query_user(session)
    window['-USER_LIST_TABLE-'].update(values=user_list)

def refresh_delete_table():
    user_list = bke.query_user(session)
    window['-USER_DELETE_TABLE-'].update(values=user_list)

# isvalyti laukelius
# def clear_inputs():
#     window['-ID-'].update(value="")
#     window['-VARDAS-'].update(value="")
#     window['-PAVARDE-'].update(value="")
#     window['-GIMIMAS-'].update(value="")
#     window['-PAREIGOS-'].update(value="")
#     window['-ATLYGINIMAS-'].update(value="")

layout = [[sg.Col(layout_left, p=0, key="_LEFT_SIDE_LAYOUT_"), 
           sg.Col(layout_user_table, p=0, visible=False, key="-USER_TABLE_LAYOUT-"), 
           sg.Col(layout_select_user, p=0, visible=False, key="-SELECT_USER_LAYOUT-"),
           sg.Col(layout_new_user, p=0, visible=False, key="-NEW_USER_LAYOUT-"),
           sg.Col(layout_delete_user, p=0, visible=False, key="-DELETE_USER_LAYOUT-")]]

window = sg.Window("Home Accounting", layout, size=(1000, 780))

while True:
    event, values = window.read()

    if event == "-USER_LIST_TABLE-":
        try:
            row_value = values['-USER_LIST_TABLE-'][0]
            values = bke.select_user_list(session, row_value)
            window['-USER_LIST_ID-'].update(value=values[0])
            window['-USER_LIST_F_NAME-'].update(value=values[1])
            window['-USER_LIST_L_NAME-'].update(value=values[2])
        except:
            pass

    if event == "-SELECT_USER-":
        close_all_right_windows()
        window["-SELECT_USER_LAYOUT-"].update(visible=True)
        user_list = bke.query_user(session)
        window['-USER_LIST_TABLE-'].update(values=user_list)

    if event == "-SELECT_USER_FROM_LIST-":
        select_user_id = window['-USER_LIST_ID-'].get()
        print(select_user_id)

    if event == "-NEW_USER-":
        close_all_right_windows()
        window["-NEW_USER_LAYOUT-"].update(visible=True)
        #
        # window["-COL3-"].update(visible=False)
        # window["-COL2-"].update(visible=True)
        # window['-TABLE-'].update(values=darbuotojai_list)

    if event == "-CREATE_USER-":
        first_name = window['-NEW_F_NAME-'].get()
        last_name = window['-NEW_L_NAME-'].get()
        bke.create_user(first_name, last_name)
        window["-NEW_USER_LAYOUT-"].update(visible=False)

    # if event == "-USER_DELETE_TABLE-":
    #     row_value = values['-USER_DELETE_TABLE-'][0]
    #     values_ = bke.select_user_list(session, row_value)

    if event == "-DELETE_USER-":
        close_all_right_windows()
        window["-DELETE_USER_LAYOUT-"].update(visible=True)
        user_list = bke.query_user(session)
        window['-USER_DELETE_TABLE-'].update(values=user_list)

    if event == "-DELETE_USER_FROM_LIST-":
        try:
            del_id = window['-DELETE_ID-'].get()
            bke.delete_user(session, del_id)
            refresh_delete_table()
            sg.popup_notify(f"User (ID: {del_id}) and their records are successfully deleted from list")
        except:
            pass
    # if event == "-USER_LIST_TABLE-":
    #     row_value = values['-USER_LIST_TABLE-'][0]
    #     values_ = bke.select_user_list(session, row_value)
 
    if event == "-CLOSE-":
        close_all_right_windows()

    if event == "-CLOSE2-":
        close_all_right_windows()

    if event == "-CLOSE3-":
        close_all_right_windows()

    if event == "-TABLE-":
        pass
    

    if event == "-irasyti-":
        pass

    if event == "-redaguoti-":
        pass

    if event == "-CLEAR-":
        pass
        # isvalyti laukelius
        #clear_inputs()

    if event == sg.WINDOW_CLOSED or event == "-EXIT-":
        break

window.close()

