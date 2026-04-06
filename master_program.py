from pybricks.tools import hub_menu
menu_list = ["1", "2", "3", "4", "5", "6","7"]

while True:
    selected = hub_menu(*menu_list)

    if selected == "1":
        import new_run1
        menu_list = ["2", "3", "4", "5", "6", "7", "1"]
    elif selected == "2":
        import new_run2
        menu_list = ["3", "4", "5", "6", "7", "1", "2"]
    elif selected == "3":
        import new_run3
        menu_list = ["4", "5", "6", "7", "1", "2", "3"]
    elif selected == "4":
        import new_run4
        menu_list = ["5", "6", "7", "1", "2", "3", "4"]
    elif selected == "5":
        import new_run5
        menu_list = ["6", "7", "1", "2", "3", "4", "5"]
    elif selected == "6":
        import new_run6
        menu_list = ["7", "1", "2", "3", "4", "5", "6"]
    elif selected == "7":
        import new_run7
        menu_list = ["1", "2", "3", "4", "5", "6", "7"]
