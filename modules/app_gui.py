import tkinter as tk
import threading

from tkinter import ttk
from utils import RBAC_Keys, OPICS_Keys
from .compare_data import Compare_Data


class App_GUI(tk.Tk):
    def __init__(self, compare_data: Compare_Data):
        super().__init__()

        self.compare_data = compare_data

        self.title("Nombre de la aplicación")
        self.geometry("1200x900")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.last_selected = None
        self.create_widgets()

    
    def create_frame_with_grid(
            self, parent, 
            row_position = 0, column_position = 0, 
            rows = 0, columns = 0, 
            pad_x = 10, pad_y=10,
            width = None,
            bg = None,
            bd_units = None,
            columnspan = 1,
            relief = None,
            sticky = 'nsew',
        ) -> tk.Frame:
        """
        This function creates a frame with a grid layout in a tkinter GUI, allowing customization of row
        and column positions, padding, width, and background color.
        
        :param parent: where you want to place the new frame
        :param row_position: specifies the row position where the frame will be placed within its parent 
        container when using the grid layout manager, defaults to 0 (optional). 
        :param column_position: specifies the column position where the frame will be placed within its 
        parent container, defaults to 0 (optional)
        :param rows: specifies the index of the row in the grid layout where the frame will be placed. It helps 
        in positioning the frame within the grid by indicating the row position, defaults to 0 (optional)
        :param columns: specifies the index of the column in the grid where the frame will be placed. It determines 
        the horizontal position of the frame within the grid layout, defaults to 0 (optional)
        :param pad_x: represents the amount of padding to be added on the x-axis (horizontal padding) around the 
        frame within its parent widget, defaults to 10 (optional)
        :param pad_y: is used to specify the vertical padding (in pixels) around the frame within its parent widget, 
        defaults to 10 (optional).
        :param width: provide a specific width value in pixels when calling this function, defaults to auto (optional)
        :param bg: It allows you to specify the background color of the frame that will be created, defaults to auto (optional)
        :param bd_units: defaults to auto (optional)
        :param columnspan: defaults to 1 (optional)
        :return: The function `create_frame_with_grid` returns a `tk.Frame` object that has been created
        with the specified parameters such as parent, row and column positions, number of rows and
        columns, padding, width, and background color.
        """
        frame = tk.Frame(parent, bg=bg, width=width, bd=bd_units, relief=relief)
        frame.grid(row=row_position, column=column_position, sticky=sticky, padx=pad_x, pady=pad_y, columnspan=columnspan)
        frame.rowconfigure(rows, weight=1)
        frame.columnconfigure(columns, weight=1)

        return frame

    
    def create_widgets(self) -> None:
        """
        The function creates two frames, a side menu frame and a content frame, and then calls functions
        to populate them with widgets.
        """
        self.sidemenu_frame = self.create_frame_with_grid(
            parent=self, bg="#2C3E50", width=350, pad_x=0, pad_y=0
        )

        self.content_frame = self.create_frame_with_grid(
            parent=self, column_position=1, rows=2, pad_x=50, pad_y=20
        )
        
        self.create_sidemenu()
        self.show_content()


    def show_loading_screen(self, task_function, *args):
        """
        The function `show_loading_screen` creates a loading window with a progress bar while executing
        a given task function in a separate thread.
        
        :param task_function: The `task_function` parameter in the `show_loading_screen` method is a
        function that you want to execute while showing a loading screen. This function will be called
        with the arguments `*args` that are passed to the `show_loading_screen` method
        """
        loading_window = tk.Toplevel(self)
        loading_window.title("Cargando")
        loading_window.geometry("300x200")
        loading_window.transient(self)
        loading_window.grab_set()

        loading_window.resizable(False, False)
        
        label = tk.Label(loading_window, text="Cargando datos, por favor espera...")
        label.pack(pady=10)

        progress_bar = ttk.Progressbar(loading_window, mode="indeterminate")
        progress_bar.pack(pady=10, padx=20, fill="x")

        progress_bar.start()
        
        def task_wrapper():
            try:
                task_function(*args)
            except Exception as e:
                print(f"Error en la tarea: {e}")
            finally:
                progress_bar.stop()
                loading_window.destroy()

        threading.Thread(target=task_wrapper, daemon=True).start()

    
    def on_select(self, button, action) -> None:
        """
        The function `on_select` changes the appearance of a selected button and clears the content
        frame before executing a specified action.
        
        :param button: The `button` parameter in the `on_select` method represents the button widget
        that was selected by the user. This method is typically used in GUI applications to handle the
        selection of a button or widget by the user
        :param action: The `action` parameter in the `on_select` method is a function that will be
        called after a button is selected. This function is executed to perform a specific action or
        task when a button is clicked
        """
        if hasattr(self, "last_selected") and self.last_selected:
            self.last_selected.config(bg="#34495E", fg="white")

        button.config(bg="white", fg="black")
        self.last_selected = button

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        action()
        
    
    def create_sidemenu(self) -> None:
        """
        The `create_sidemenu` function creates side menu buttons with specific actions in a tkinter GUI.
        """
        options = [
            {"text": "Diferencia entre usuarios", "action": self.users_diff_frame_with_progress}, 
            {"text": "Diferencia entre perfiles", "action": self.reports_diff_frame_with_progress}
        ]

        self.sidenav_buttons = []

        for option in options:
            button = tk.Button(
                self.sidemenu_frame, 
                text=option["text"], 
                bg="#34495E",
                fg="white",
                bd=0,
                padx=75,
                pady=10,
                font=("Arial", 12),
                anchor="w"
            )
            button.config(command=lambda b=button, o=option: self.on_select(b, o["action"]))
            button.pack(fill="x")
            self.sidenav_buttons.append(button)

    
    def create_multiselect_list(self, parent_frame: tk.Frame, items: list[str], item_key: str, title: str, button_label: str, button_action: object) -> None | tk.Listbox:
        """
        The `create_multiselect_list` function creates a multiselect list with customizable items,
        title, button label, and button action in a tkinter GUI.
        
        :param parent_frame: The `parent_frame` parameter is the tkinter Frame widget where the
        multiselect list will be placed. It serves as the container for the listbox and other widgets
        created within the `create_multiselect_list` function
        :type parent_frame: tk.Frame
        :param items: The `items` parameter in the `create_multiselect_list` function is a list of
        dictionaries where each dictionary represents an item to be displayed in the multiselect list.
        Each dictionary should have a key specified by the `item_key` parameter, which is used to
        extract the display value for the item
        :type items: list[str]
        :param item_key: The `item_key` parameter in the `create_multiselect_list` function is used to
        specify the key in each item dictionary that will be displayed in the listbox. It is used to
        extract the specific value from each item dictionary to show in the listbox
        :type item_key: str
        :param title: The `title` parameter in the `create_multiselect_list` function is a string that
        represents the title or heading of the multiselect listbox widget that will be displayed to the
        user. It is used to provide a clear indication or description of the purpose of the multiselect
        listbox
        :type title: str
        :param button_label: The `button_label` parameter in the `create_multiselect_list` function is a
        string that represents the label text for the button that will trigger a specific action when
        clicked. It is displayed on the button created within the function and can be customized to
        convey the intended action to the user
        :type button_label: str
        :param button_action: The `button_action` parameter in the `create_multiselect_list` function is
        expected to be a function or method that will be called when a button in the GUI is clicked.
        This function should take two arguments: the `listbox` widget (tk.Listbox) and the
        `index_to_object
        :type button_action: object
        :return: The `create_multiselect_list` function returns a tuple containing the `listbox` widget
        and the `index_to_object` dictionary.
        """
        frame = tk.Frame(parent_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        label = tk.Label(frame, text=title, font=("Arial", 14), anchor="w", wraplength=300)
        label.pack(fill="y", pady=(0, 5))

        if not items:
            message = tk.Label(
                parent_frame,
                text="No hay diferencias disponibles",
                font=("Arial", 12, "italic"),
                fg="#6c757d",
                pady=10
            )
            message.pack()
            return None

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        listbox = tk.Listbox(
            frame,
            selectmode=tk.MULTIPLE,
            yscrollcommand=scrollbar.set,
            bg="#F8F9Fa",
            fg="#212529",
            selectbackground="#007BFF",
            selectforeground="white",
            font=("Arial", 12),
            bd=1,
            relief="solid",
            height=20,
            width=35,
            exportselection=False
        )
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both", expand=True)

        index_to_object = {}

        for index, item in enumerate(items):
            listbox.insert(tk.END, item[item_key])
            index_to_object[index] = item

        def toggle_select_all():
            """
            The function `toggle_select_all` toggles the selection of all items in a listbox widget in Python.
            """
            if len(listbox.curselection()) == listbox.size():
                listbox.selection_clear(0, tk.END)
            else:
                listbox.selection_set(0, tk.END)

        select_all_button = tk.Button(
            parent_frame,
            text="Seleccionar/Deseleccionar todo",
            command=toggle_select_all,
            font=("Arial", 12),
            bg="#3498D8",
            fg="white"
        )
        select_all_button.pack(pady=10)


        tk.Button(
            parent_frame,
            text=button_label,
            command=lambda: button_action(listbox, index_to_object),
            font=("Arial", 12),
            bg="#2ECC71",
            fg="white"
        ).pack(pady=20)
        
        return listbox, index_to_object
    

    def create_description_frame(self, title, description) -> None:
        """
        The function `create_description_frame` creates a frame with a title and description labels in a
        tkinter GUI.
        
        :param title: The `title` parameter is a string that represents the title of the description
        frame. It will be displayed as a bold label at the top of the frame
        :param description: The `create_description_frame` method creates a frame with a title and
        description labels using the provided `title` and `description` parameters. The `title`
        parameter is used to set the text of the title label with a bold font style, while the
        `description` parameter is used to set the
        """
        description_frame = self.create_frame_with_grid(
            parent=self.content_frame, pad_y=20, rows=1
        )
        
        title = tk.Label(
            description_frame,
            text=title,
            font=("Arial", 14, "bold"),
            pady=10
        )
        title.grid(row=0, column=0)

        description = tk.Label(
            description_frame,
            text=description,
            font=("Arial", 10, "italic"),
            wraplength=650
        )
        description.grid(row=1, column=0)


    def create_actions_frame(self, conditional, action) -> None:
        """
        The function `create_actions_frame` creates a frame with a label or button based on a
        conditional statement.
        
        :param conditional: The `conditional` parameter in the `create_actions_frame` method is a
        boolean value that determines whether there are actions available for a particular section. If
        `conditional` is `True`, it means there are actions available and a button will be displayed to
        perform the specified `action`. If `conditional`
        :param action: The `action` parameter in the `create_actions_frame` method is a function that
        will be executed when the "Aprobar todos los cambios" button is clicked. This function should be
        defined elsewhere in your code and should contain the logic for approving the changes
        """
        actions_frame = self.create_frame_with_grid(
            parent=self.content_frame, bg="#F0F0F0", row_position=2, columnspan=2
        )

        if not conditional:
            tk.Label(
                actions_frame,
                text="No hay acciones disponibles para esta sección",
                font=("Arial", 12, "italic"),
                fg="#6c757d",
                pady=10
            ).grid(row=0, column=0)
        else:
            tk.Button(
                actions_frame,
                text="Aprobar todos los cambios",
                command=action,
                font=("Arial", 12),
                bg="#2ECC71",
                fg="white"
            ).grid(row=0, column=0)

    
    def create_users_diff_frame(self, rbac_header, opics_header, rbac_data, opics_data) -> None:
        """
        The function `create_users_diff_frame` generates a user interface to display and manage the
        differences between user data from RBAC and OPICS systems.
        
        :param rbac_header: The `rbac_header` parameter in the `create_users_diff_frame` function is a
        string that represents the header or title for the RBAC (Role-Based Access Control) section in
        the user differences report between RBAC and OPICS. It is used to label and provide context for
        the RBAC
        :param opics_header: The `opics_header` parameter in the `create_users_diff_frame` function is a
        string that represents the title or header for the list of users from the OPICS data. It is used
        to label or identify the section where the OPICS users will be displayed in the user interface
        :param rbac_data: The `rbac_data` parameter in the `create_users_diff_frame` function likely
        contains a list of user data from the RBAC system. This data could include information such as
        user names, roles, permissions, or any other relevant user details stored in the RBAC system
        :param opics_data: The `opics_data` parameter in the `create_users_diff_frame` function likely
        contains data related to users from the OPICS system. This data is used to populate a listbox in
        the user interface where users can be selected for further processing
        """
        self.create_description_frame(
            title="Diferencias de usuarios reportados entre RBAC y OPICS",
            description="A continuación se listan las diferencias encontradas entre los usuarios que se encuentran en la versión actual del Excel RBAC vs los usuarios que se encuentran en el último reporte RUGAR de OPICS"
        )

        diff_frame = self.create_frame_with_grid(
            parent=self.content_frame, row_position=1, columns=1, pad_y=0
        )

        rbac_frame = self.create_frame_with_grid(
            parent=diff_frame, bg="#F0F0F0"
        )
        rbac_listbox, index_to_object_rbac = self.create_multiselect_list(
            parent_frame=rbac_frame, 
            items=rbac_data, 
            item_key=RBAC_Keys.USER,
            title=rbac_header,
            button_label="Eliminar usuarios seleccionados de RBAC",
            button_action=self.process_rbac_users_diff
        )

        opics_frame = self.create_frame_with_grid(
            parent=diff_frame, bg="#F0F0F0", column_position=1
        )
        opics_listbox, index_to_object_opics = self.create_multiselect_list(
            parent_frame=opics_frame, 
            items=opics_data, 
            item_key=OPICS_Keys.USER,
            title=opics_header,
            button_label="Añadir usuarios seleccionados en RBAC",
            button_action=self.process_opics_users_diff
        )

        self.create_actions_frame(
            conditional= len(rbac_data) or len(opics_data),
            action=lambda: self.process_user_diff_selection(rbac_listbox, index_to_object_rbac, opics_listbox, index_to_object_opics)
        )


    def users_diff_frame_with_progress(self) -> None:
        """
        The function `users_diff_frame_with_progress` compares user data between two sources and
        displays the differences with a loading screen.
        """
        def user_diff_frame():
            [opics_not_in_rbac, rbac_not_in_opics] = self.compare_data.compare_users_in_reports()

            self.create_users_diff_frame(
                rbac_header = "Usuarios que están en RBAC pero no en OPICS",
                opics_header = "Usuarios que están en OPICS pero no en RBAC",
                rbac_data = rbac_not_in_opics,
                opics_data = opics_not_in_rbac
            )

        self.show_loading_screen(user_diff_frame)


    def process_user_diff_selection(self, rbac_listbox, index_to_object_rbac, opics_listbox, index_to_object_opics):
            rbac_selected = [index_to_object_rbac.get(i) for i in rbac_listbox.curselection()]
            opics_selected = [index_to_object_opics.get(i) for i in opics_listbox.curselection()]

            print("Seleccionados de RBAC", rbac_selected)
            print("Seleccionados de OPICS", opics_selected)

            for i in reversed(rbac_listbox.curselection()):
                rbac_listbox.delete(i)

            for i in reversed(opics_listbox.curselection()):
                opics_listbox.delete(i)
    

    def process_opics_users_diff(self, listbox, index_to_object):
        selected = [index_to_object.get(i) for i in listbox.curselection()]
        
        for i in reversed(listbox.curselection()):
            listbox.delete(i)


    def process_rbac_users_diff(self, listbox, index_to_object):
        selected = [index_to_object.get(i) for i in listbox.curselection()]
        print("Seleccionados de RBAC", selected)

        for i in reversed(listbox.curselection()):
            listbox.delete(i)

    
    def create_reports_diff_frame(self, reports_diff):
        """
        The function `create_reports_diff_frame` generates a frame displaying differences between
        reported data in RBAC and OPICS.
        
        :param reports_diff: The `reports_diff` parameter seems to be a list of objects representing
        differences in reported data between RBAC and OPICS. Each object in the list likely contains
        information about a specific difference found between the two systems
        """
        selected_objects = []

        self.create_description_frame(
            title="Diferencias de datos reportados entre RBAC y OPICS",
            description="A continuación se listan las diferencias encontradas entre los usuarios que se encuentran en la versión actual del Excel RBAC pero presentan diferencias con respecto al último reporte RUGAR de OPICS"
        )

        self.configure_content_frame_rows()

        diff_frame = self.create_diff_frame()

        canvas, scrollable_frame = self.create_scrollable_canvas(diff_frame)

        self.configure_mouse_wheel_scroll(canvas)

        for i, obj in enumerate(reports_diff):
            self.create_report_item(scrollable_frame, obj, i, selected_objects)

        self.create_diff_profiles_actions(len(reports_diff))
        

    def configure_content_frame_rows(self) -> None:
        """
        This function configures the row weights of a content frame in a Python program.
        """
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=8)
        self.content_frame.rowconfigure(2, weight=1)


    def create_diff_frame(self) -> tk.Frame:
        """
        The function `create_diff_frame` returns a Tkinter Frame created with a specific grid layout
        within a parent frame.
        :return: A Tkinter Frame object is being returned.
        """
        return self.create_frame_with_grid(
            parent=self.content_frame, row_position=1, pad_y=0
        )


    def create_scrollable_canvas(self, diff_frame) -> tuple[tk.Canvas, tk.Frame]:
        """
        This function creates a scrollable canvas with a vertical scrollbar inside a given frame.
        
        :param diff_frame: The `diff_frame` parameter in the `create_scrollable_canvas` method is a
        tkinter Frame widget where the scrollable canvas will be placed. This frame will contain the
        canvas and scrollbar for creating a scrollable area within the frame
        :return: The function `create_scrollable_canvas` returns a tuple containing a `tk.Canvas` object
        and a `tk.Frame` object.
        """
        canvas = tk.Canvas(diff_frame)

        scrollbar = tk.Scrollbar(diff_frame, orient=tk.VERTICAL, command=canvas.yview)

        scrollable_frame = self.create_frame_with_grid(parent=canvas)
        scrollable_frame.update_idletasks()
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0,0), window=scrollable_frame, anchor="nw", width=diff_frame.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        return canvas, scrollable_frame


    def configure_mouse_wheel_scroll(self, canvas) -> None:
        """
        The function `configure_mouse_wheel_scroll` binds mouse wheel and button events to scroll a
        canvas vertically.
        
        :param canvas: The `canvas` parameter in the `configure_mouse_wheel_scroll` function is expected
        to be a tkinter Canvas widget. This function sets up mouse wheel scrolling behavior for the
        given canvas widget
        """
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    
    def toggle_selection(self, index, icon_label, selected_objects) -> None:
        """
        The function `toggle_selection` toggles the selection of an object based on its index in a list
        and updates the icon label accordingly.
        
        :param index: The `index` parameter represents the index of an object that you want to toggle
        the selection for in a list of selected objects
        :param icon_label: The `icon_label` parameter seems to be a reference to a GUI element that
        displays an icon or text representing the selection state of an object. In this case, it appears
        to be a label element that displays either a white square "⬜" or a check mark "✅" based
        :param selected_objects: The `selected_objects` parameter is a list that stores the indices of
        objects that have been selected. When an object is selected, its index is added to this list,
        and when it is deselected, its index is removed from the list
        """
        if index in selected_objects:
            selected_objects.remove(index)
            icon_label.config(text="🔲")
        else:
            selected_objects.append(index)
            icon_label.config(text="✅")


    def create_report_item(self, scrollable_frame, obj, i, selected_objects):
        """
        The function `create_report_item` generates a report item with user information and actions for
        selecting the item.
        
        :param scrollable_frame: The `scrollable_frame` parameter is the frame where the report item
        will be displayed. It is a container that allows for scrolling if the content exceeds the
        visible area. In your `create_report_item` method, you are creating various elements within this
        `scrollable_frame` to display information about a
        :param obj: The `create_report_item` method you provided seems to be creating a report item with
        user information and buttons for selection. It also includes a commented-out section for
        displaying groups information
        :param i: The `i` parameter in the `create_report_item` method is used as the row position for
        placing the item within the scrollable frame. It helps in positioning the item correctly within
        the grid layout of the report
        :param selected_objects: The `create_report_item` method seems to be creating a report item with
        various labels and buttons for a given object. The `selected_objects` parameter is likely a list
        or dictionary that stores information about the objects that have been selected in the report
        """
        item_frame = self.create_frame_with_grid(
            parent=scrollable_frame, bd_units=1, pad_y=5,
            row_position=i, column_position=0, columns=1, relief="solid"
        )

        actions_frame = self.create_frame_with_grid(
            parent=item_frame, column_position=1, rows=1
        )

        icon_label = tk.Label(actions_frame, text="🔲", font=("Arial", 16))
        icon_label.grid(row=0, column=0, padx=10)

        button = tk.Button(actions_frame, text="Seleccionar", command=lambda i=i, lbl=icon_label: self.toggle_selection(i, lbl, selected_objects))
        button.grid(row=1, column=0, padx=10)

        user_info_frame = self.create_frame_with_grid(
            parent=item_frame, rows=4, column_position=0
        )

        user = f"Usuario: {obj['opics_user']}"
        user_label = tk.Label(user_info_frame, text=user, anchor="w")
        user_label.grid(row=0, column=0, sticky="w")

        profile = f"Perfil: {obj['rbac_profile']}"
        profile_label = tk.Label(user_info_frame, text=profile, anchor="w")
        profile_label.grid(row=1, column=0, sticky="w")

        # rbac_groups = f"Grupos que están en RBAC pero no en OPICS: {obj['rbac_groups_not_in_opics_groups']}"
        # rbac_groups_label = tk.Label(user_info_frame, text=rbac_groups, anchor="w")
        # rbac_groups_label.grid(row=2, column=0, sticky="w")

        # opics_groups = f"Grupos que están en OPICS pero no en RBAC: {obj["opics_groups_not_in_rbac_groups"]}"
        # opics_groups_label = tk.Label(user_info_frame, text=opics_groups, anchor="w")
        # opics_groups_label.grid(row=3, column=0, sticky="w")

        groups_frame = self.create_frame_with_grid(
            parent=user_info_frame, row_position=4, columns=1
        )

        self.populate_groups(obj["opics_groups"], obj["rbac_groups"], groups_frame)


    def populate_groups(self, opics_groups, rbac_groups, groups_frame):
        """
        The function `populate_groups` creates label frames for OPICS and RBAC groups and populates them
        with group labels.
        
        :param opics_groups: It looks like you were about to provide some information about the
        `opics_groups` parameter in the `populate_groups` method. Could you please provide more details
        or complete the sentence so that I can assist you further?
        :param rbac_groups: The `rbac_groups` parameter in your `populate_groups` method likely refers
        to a list of RBAC (Role-Based Access Control) groups. RBAC is a method of restricting network
        access based on roles assigned to users. In your code, you are creating label frames for both
        OPICS groups
        :param groups_frame: The `groups_frame` parameter is a tkinter Frame widget where you want to
        populate groups of OPICS and RBAC. In the provided code snippet, two LabelFrames
        (`opics_label_frame` and `rbac_label_frame`) are created within the `groups_frame` to display
        the groups of OP
        """
        opics_label_frame = tk.LabelFrame(
            groups_frame, text="Grupos de OPICS"
        )
        opics_label_frame.grid(row=0, column=0, padx=10, sticky="n")

        rbac_label_frame = tk.LabelFrame(
            groups_frame, text="Grupos de RBAC"
        )
        rbac_label_frame.grid(row=0, column=1, padx=10, sticky="n")
    
        max_rows = max(len(opics_groups), len(rbac_groups))

        for index in range(max_rows):
            self.create_group_label(opics_groups, rbac_groups, opics_label_frame, rbac_label_frame, index)


    def create_group_label(self, opics_groups, rbac_groups, opics_label_frame, rbac_label_frame, index):
        """
        This function creates labels for groups from two different lists and assigns background colors
        based on their presence in each other's list.
        
        :param opics_groups: The `opics_groups` parameter seems to be a list containing group names
        related to OPICS. The function `create_group_label` takes these group names along with RBAC
        group names and creates labels for each group in two different frames (`opics_label_frame` and
        `rbac_label_frame`)
        :param rbac_groups: The `rbac_groups` parameter seems to be a list of RBAC (Role-Based Access
        Control) groups. The function `create_group_label` takes these RBAC groups and creates labels
        for them in a graphical user interface (GUI) using Tkinter. The labels are displayed in a
        specific frame
        :param opics_label_frame: The `opics_label_frame` parameter is a frame in a Tkinter GUI where
        labels for OPICS groups will be displayed. The `create_group_label` function creates a label for
        an OPICS group and places it within the `opics_label_frame`. The label's text is set based on
        :param rbac_label_frame: The `rbac_label_frame` parameter is a frame in a Tkinter GUI
        application where labels for RBAC (Role-Based Access Control) groups are displayed. The function
        `create_group_label` creates a label for an RBAC group based on the provided RBAC groups list
        and index. The label
        :param index: The `index` parameter in the `create_group_label` function is used to determine
        the position of the label within the grid layout. It is used to access the corresponding group
        name from the `opics_groups` and `rbac_groups` lists based on the index value. If the index is
        """
        opics_text = opics_groups[index] if index < len(opics_groups) else ""
        opics_label = tk.Label(
            opics_label_frame, text=opics_text,
            bg="white" if opics_text in rbac_groups else "lightblue",
            anchor="w",
            width=30
        )
        opics_label.grid(row=index, column=0, sticky="w", padx=5, pady=5)

        rbac_text = rbac_groups[index] if index < len(rbac_groups) else ""
        rbac_label = tk.Label(
            rbac_label_frame, text=rbac_text,
            bg="white" if rbac_text in opics_groups else "lightcoral",
            anchor="w",
            width=30
        )
        rbac_label.grid(row=index, column=0, sticky="w", padx=5, pady=5)


    def create_diff_profiles_actions(self, n_diff):
        """
        The function creates a frame with labels displaying information about the number of different
        profiles found and a recommendation for manual review.
        
        :param n_diff: The `n_diff` parameter in the `create_diff_profiles_actions` method represents
        the number of profiles that have differences. This parameter is used to display a message
        informing the user about the number of profiles with differences found in the application
        """
        actions_frame = tk.Frame(self.content_frame, height=100)
        actions_frame.grid(row=2, column=0)

        n_diff_label = tk.Label(
            actions_frame,
            text=f"Se encontraron '{n_diff}' perfiles con diferencias",
            font=("Arial", 12, "bold"),
            pady=10
        )
        n_diff_label.grid(row=0, column=0)

        description = tk.Label(
            actions_frame,
            text="Se recomienda realizar una revisión manual para decidir que acciones tomar",
            font=("Arial", 10, "italic"),
            wraplength=650
        )
        description.grid(row=1, column=0)


    def reports_diff_frame_with_progress(self):
        """
        This function generates a difference report frame with progress indication.
        """
        def reports_diff_frame():
            self.create_reports_diff_frame(
                reports_diff = self.compare_data.compare_users_groups()
            )
        
        self.show_loading_screen(reports_diff_frame)

    
    def show_content(self):
        pass