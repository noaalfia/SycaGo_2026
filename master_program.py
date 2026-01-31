from pybricks.tools import hub_menu
menu_list = ["1", "2", "3", "4", "5"]

while True:
    selected = hub_menu(*menu_list)

    if selected == "1":
        import run1
        menu_list = ["2", "3", "4", "5", "1"]
    elif selected == "2":
        import run2
        menu_list = ["3", "4", "5", "1", "2"]
    elif selected == "3":
        import run3
        menu_list = ["4", "5", "1", "2", "3"]
    elif selected == "4":
        import run4
        menu_list = ["5", "1", "2", "3", "4"]
    elif selected == "5":
        import run5
        menu_list = ["1", "2", "3", "4", "5"]
