import copy
import logging
import os
import time
import typing
from dataclasses import dataclass
from typing import Dict, Callable
import remi
from remi import GenericDialog
from remi.gui import Container, Button, Label, HBox, decorate_set_on_listener, decorate_event, Widget

import NodeCore

log = logging.getLogger(__name__)
class _Menu:
    menubar = None
    def __init__(self):
        self.menu_entry: Dict[str, remi.gui.MenuItem] = {}
        self.create_menubar()

    def create_menubar(self):
        if self.menubar is not None: return self.menubar
        self.menu = remi.gui.Menu(width="100%", height="30px")

        self.menubar = remi.gui.MenuBar(width="100%", height="30px")
        self.menubar.css_border_width = "0px"
        # menubar.css_background_color = 'rgb(0,0,0,0.0)'
        self.menubar.append(self.menu)
        return self.menubar

    def create_menu_item(self, name: str):
        item = remi.gui.MenuItem(f"{name}", width=150, height=30)
        return item

    def create(self, path, name: str):
        if path in self.menu_entry:
            node = self.menu_entry[path]
        else:
            node = self.create_menu_item(name)
            self.menu_entry[path] = node
        return node

    def get_parent(self, path):
        return "/".join(path.split("/")[:-1])

    def rm_menu_item(self, path_in:str):
        log.info(f"rm_menu_item:{path_in}")

        path=path_in.replace('/'," ->/").replace(" ->/", '/',1)
        if path in self.menu_entry:
            node = self.menu_entry[path]
            parent = self.menu_entry[self.get_parent(path)]
            log.info(f"Removing{path}")
            # Special case subcontainer is the real child for menu in remi :-/
            parent.sub_container.remove_child(node)
            if len(parent.sub_container.children)==0:
                # Remove submeny if no children
                remove_parent = "/".join(path_in.split('/')[:-1]) + " ->"
                self.rm_menu_item(remove_parent)


    def wait_for_server_start(self):
        while True:
            try:
                parent = self.menu
                break
            except:
                time.sleep(0.5)
                continue


    def add_menu_item(self, path, callback: Callable[[dict], None]=None):
        parent = self.menu
        elements = path.split("/")[1:]
        path = ""
        for node_name in elements:
            # Add submeny if there is more elements after this
            if node_name != elements[-1]:
                node_name += " ->"
            path = path + f"/{node_name}"
            node = self.create(path, node_name)
            parent.append(node)
            parent = node
        parent.onclick.do(callback)



menu = _Menu()


class TransparentContainer(remi.gui.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.css_background_color = "transparent"
        self.css_align_content = "center"


def start_www(port: int = 8079):
    log.info("start_www")
    remi.start(
        MyApp,
        debug=True,
        address="0.0.0.0",
        port=port,
        start_browser=False,
        multiple_instance=False,
    )


class MyApp(remi.App):
    user_container: remi.gui.Container
    self_saved = None
    last_level = None
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(__file__), "res")
        super(MyApp, self).__init__(*args, static_file_path={"res": res_path})


    def main(self):
        MyApp.self_saved = self
        MyApp.self_saved.last_level = 1
        log.info(f"saved_self.saved")
        self.root_container = TransparentContainer( width="100%",  height="100%", margin="0px auto", style={"display": "block", "overflow": "hidden"}  )
        self.root_container.css_background_color = "rgb(0,0,0,0.0)"
        menubar = menu.create_menubar()
        self.main_container: remi.gui.Container = TransparentContainer( width="100%",  height="100%", margin="0px auto", style={"display": "block", "overflow": "hidden"}  )
        self.empty_space = TransparentContainer()
        self.empty_space.style.update({'display': 'block', 'overflow': 'auto', 'margin': '5px'})
        self.user_container: remi.gui.Container = TransparentContainer( width="100%",  height="100%", margin="0px auto", style={"display": "block", "overflow": "hidden"}  )
        self.dialog_container: remi.gui.Container = TransparentContainer()
        self.dialog_container2: remi.gui.Container = TransparentContainer()

        self.root_container.append(menubar)
        self.root_container.append(self.empty_space)
        self.root_container.append(self.main_container)

        self.main_container.append(self.user_container)
        self.user_container.append(remi.gui.Button(text='UserDataButton'))
        log.info(f"Root container constructed",)
        return self.root_container

    def hide(self):
        self.main_container.empty()

    @classmethod
    def show_view(cls, view):
        if MyApp.self_saved is not None:
            cls.self_saved.user_container.empty()
            cls.self_saved.user_container.append(view.get_view())

    @classmethod
    def show_dialog(cls, dialog: remi.gui.Container, level: int=1):
        if MyApp.self_saved is not None:
            MyApp.self_saved.last_level=level
            if level==1:
                cls.self_saved.main_container.empty()
                cls.self_saved.dialog_container.empty()
                cls.self_saved.main_container.append(cls.self_saved.dialog_container)
                cls.self_saved.dialog_container.append(dialog)
            else:
                cls.self_saved.main_container.empty()
                cls.self_saved.dialog_container2.empty()
                cls.self_saved.main_container.append(cls.self_saved.dialog_container2)
                cls.self_saved.dialog_container2.append(dialog)


    @classmethod
    def close_dialog(cls):
        if MyApp.self_saved.last_level==1:
            cls.self_saved.main_container.empty()
            cls.self_saved.dialog_container.empty()
            cls.self_saved.main_container.append(cls.self_saved.user_container)
        else:
            cls.self_saved.main_container.empty()
            cls.self_saved.dialog_container2.empty()
            cls.self_saved.main_container.append(cls.self_saved.dialog_container)
            MyApp.self_saved.last_level = 1


class ModGenericDialog(remi.gui.GenericDialog):
    def __init__(self, title='', message='', *args, **kwargs):
        """
        Args:
            title (str): The title of the dialog.
            message (str): The message description.
            kwargs: See Container.__init__()
        """
        super(GenericDialog, self).__init__(*args, **kwargs)
        self.set_layout_orientation(Container.LAYOUT_VERTICAL)
        self.style.update({'display': 'block', 'overflow': 'auto', 'margin': '0px auto'})

        if len(title) > 0:
            t = Label(title)
            t.add_class('DialogTitle')
            self.append(t, "title")

        m = remi.gui.TextInput(single_line=False, height=250)
        m.text = message
        m.css_margin = '5px'
        self.append(m, "message")

        self.container = Container()
        self.container.style.update({'display': 'block', 'overflow': 'auto', 'margin': '5px'})
        self.container.set_layout_orientation(Container.LAYOUT_VERTICAL)
        self.conf = Button('Ok')
        self.conf.set_size(100, 30)
        self.conf.css_margin = '3px'
        self.cancel = Button('Cancel')
        self.cancel.set_size(100, 30)
        self.cancel.css_margin = '3px'
        hlay = Container(height=35)
        hlay.css_display = 'block'
        hlay.style['overflow'] = 'visible'
        hlay.append(self.conf, "confirm_button")
        hlay.append(self.cancel, "cancel_button")
        self.conf.style['float'] = 'right'
        self.cancel.style['float'] = 'right'

        self.append(self.container, "central_container")
        self.append(hlay, "buttons_container")

        self.conf.onclick.connect(self.confirm_dialog)
        self.cancel.onclick.connect(self.cancel_dialog)

        self.inputs = {}

        self._base_app_instance = None
        self._old_root_widget = None

    def add_field_with_label(self, key, label_description, field):
        """
        Adds a field to the dialog together with a descriptive label and a unique identifier.

        Note: You can access to the fields content calling the function GenericDialog.get_field(key).

        Args:
            key (str): The unique identifier for the field.
            label_description (str): The string content of the description label.
            field (Widget): The instance of the field Widget. It can be for example a TextInput or maybe
            a custom widget.
        """
        self.inputs[key] = field
        label = Label(label_description)
        label.css_margin = '0px 5px'
        label.style['min-width'] = '30%'
        container = HBox()
        container.style.update({'justify-content': 'space-between', 'overflow': 'auto', 'padding': '3px'})
        container.append(label, key='lbl' + key)
        container.append(self.inputs[key], key=key)
        self.container.append(container, key=key)

    def add_field(self, key, field):
        """
        Adds a field to the dialog with a unique identifier.

        Note: You can access to the fields content calling the function GenericDialog.get_field(key).

        Args:
            key (str): The unique identifier for the field.
            field (Widget): The widget to be added to the dialog, TextInput or any Widget for example.
        """
        self.inputs[key] = field
        container = HBox()
        container.style.update({'justify-content': 'space-between', 'overflow': 'auto', 'padding': '3px'})
        container.append(self.inputs[key], key=key)
        self.container.append(container, key=key)

    def get_field(self, key):
        """
        Args:
            key (str): The unique string identifier of the required field.

        Returns:
            Widget field instance added previously with methods GenericDialog.add_field or
            GenericDialog.add_field_with_label.
        """
        return self.inputs[key]

    @decorate_set_on_listener("(self,emitter)")
    @decorate_event
    def confirm_dialog(self, emitter):
        """Event generated by the OK button click.
        """
        self.hide()
        return ()

    @decorate_set_on_listener("(self,emitter)")
    @decorate_event
    def cancel_dialog(self, emitter):
        """Event generated by the Cancel button click."""
        self.hide()
        return ()

    def show(self, base_app_instance):
        self._base_app_instance = base_app_instance
        self._old_root_widget = self._base_app_instance.root
        self._base_app_instance.set_root_widget(self)

    def hide(self):
        Dialog.close()
        pass

class ModFileSelectionDialog(remi.gui.FileSelectionDialog):
    def __init__(self,**kwargs):
        super().__init__(multiple_selection=False, selection_folder='.',
                 allow_file_selection=True, allow_folder_selection=False,**kwargs)
        self.view = remi.gui.Button('View')
        self.view.set_size(100, 30)
        self.view.css_margin = '3px'
        self.get_child("buttons_container").append(self.view, "view_button")


    def hide(self):
        Dialog.close()
        pass

class ModStartDialog(remi.gui.GenericDialog):
    def __init__(self, title='', message='', *args, **kwargs):
        super().__init__(title, message, *args, **kwargs)
        self.view = remi.gui.Button('View')
        self.view.set_size(100, 30)
        self.view.css_margin = '3px'
        hlay = self.get_child("buttons_container")
        hlay.empty()
        hlay.append(self.view, "view_button")

        button_width=90
        button_width_small=70
        self.conf = remi.gui.Button("Start")
        self.conf.set_size(button_width, 30)
        self.conf.css_margin = '3px'

        self.view = remi.gui.Button('View')
        self.view.set_size(button_width, 30)
        self.view.css_margin = '3px'



        self.cancel = remi.gui.Button('Close')
        self.cancel.set_size(button_width_small, 30)
        self.cancel.css_margin = '3px'

        self.view = remi.gui.Button('View')
        self.view.set_size(button_width_small, 30)
        self.view.css_margin = '3px'

        self.code = remi.gui.Button('Code')
        self.code.set_size(button_width_small, 30)
        self.code.css_margin = '3px'

        self.help = remi.gui.Button('Help')
        self.help.set_size(button_width_small, 30)
        self.help.css_margin = '3px'

        self.kill = remi.gui.Button('Kill')
        self.kill.set_size(button_width_small, 30)
        self.kill.css_margin = '3px'


        hlay.append(self.conf, "confirm_button")
        hlay.append(self.code, "code_button")
        hlay.append(self.view, "view_button")
        hlay.append(self.help, "help_button")
        hlay.append(self.kill, "kill_button")
        hlay.append(self.cancel, "cancel_button")
        self.conf.style['float'] = 'right'
        self.cancel.style['float'] = 'right'
        self.view.style['float'] = 'right'




    def hide(self):
        Dialog.close()


class Dialog:
    class File:
        @classmethod
        def show(cls, title: str='Title', ok_callback: Callable[[str], None]=None, view_callback: Callable[[str], None]=None):
            d = ModFileSelectionDialog(title=title, width='500px')
            d.confirm_dialog.do(lambda x: ok_callback(d.fileFolderNavigator.get_selection_list()[0]))
            d.view.onclick.connect(lambda x: view_callback(d.fileFolderNavigator.get_selection_list()[0]))

            MyApp.show_dialog(d)
            pass

    class Popup:
        @classmethod
        def show(cls, title: str='Title', message: str = 'No message', level: int=1, ok_callback=None):
            d = ModGenericDialog(title=title, message=message, width='500px')
            d.conf.onclick.connect( lambda x: [ok_callback(x), Dialog.close()] )
            MyApp.show_dialog(d, level=level)

    class Start:
        textinput = None
        @classmethod
        def show(cls, title: str='Title', args: {}=None, predefined_args:[] = None, start_callback: Callable[[dict], None]=None, view_callback: Callable[[str], None]=None, code_callback: Callable[[str], None]=None, help_callback: Callable[[str], None]=None, kill_callback: Callable[[str], None]=None):
            d = ModStartDialog(title=title, message="", width='600px')
            #d.attributes['title'] = "QWERTY\n123\n" # Hints
            d.view.onclick.connect(lambda x: view_callback(title))
            d.conf.onclick.connect(lambda x: start_callback({text: cls.textinput[text].get_value() for text in cls.textinput}))
            d.cancel.onclick.connect(lambda x: Dialog.close())
            d.kill.onclick.connect(lambda x: kill_callback(title))
            d.help.onclick.connect(lambda x: help_callback(title))
            d.code.onclick.connect(lambda x: code_callback(title))

            if predefined_args is not None:
                name='Predefined'
                predefined_args.update({'default': args})
                l = [x for x in predefined_args]
                dropdown = remi.gui.DropDown.new_from_list(l, width=200, height=20, margin='10px')
                dropdown.set_value('default')
                dropdown.onchange.do(lambda _,selected: cls.update_arg_values(predefined_args[selected]))

                container = remi.gui.HBox()
                container.style.update({'justify-content': 'space-between', 'overflow': 'auto', 'padding': '3px'})
                button = remi.gui.Button(text='...', width=30)
                #button.onclick.do(button_callback)
                container.append(dropdown)
                space = remi.gui.HBox()
                space.style.update({'display': 'block', 'overflow': 'auto', 'margin': '5px'})
                container.append(space)
                container.append(button)
                d.add_field_with_label(name, name, container)

            # Create args in gui
            cls.textinput = {}
            for name, value in args.items():
                if  isinstance(value, dict):
                    cls.textinput[name] = SelectTextbox(choice_dict=value, width=200, height=20)
                else:
                    cls.textinput[name] = remi.gui.TextInput(width=200, height=20)
                cls.textinput[name].set_value(str(value))
                cls.textinput[name].attributes['title'] = "QWERTY\n123\n" # Hints

                container = remi.gui.HBox()
                container.style.update({'justify-content': 'space-between', 'overflow': 'auto', 'padding': '3px'})
                button = remi.gui.Button(text='...', width=30)
                #button.onclick.do(button_callback)
                container.append(cls.textinput[name])
                space = remi.gui.HBox()
                space.style.update({'display': 'block', 'overflow': 'auto', 'margin': '5px'})
                container.append(space)
                container.append(button)

                d.add_field_with_label(name, name, container)
            MyApp.show_dialog(d)

        @classmethod
        def update_arg_values(cls, args):
            for name, value  in args.items():
                try:
                    cls.textinput[name].set_value(value)
                except:
                    pass


    @classmethod
    def close(cls):
        MyApp.close_dialog()

class TextInputReadonly(remi.gui.TextInput):
    def __init__(self, *args, **kwargs):
        self.buffer = ""
        super(TextInputReadonly, self).__init__(*args, **kwargs)
        self.type = 'textarea readonly'
        self.ondblclick.do(self.dblclick)

    def dblclick(self, x):
        self.empty()
        self.buffer=''
        super(TextInputReadonly, self).set_text('')

    def set_text(self, text):
        if text[0:3] == "CLR":
            self.buffer = ''
            text=text[3:]
        self.buffer = self.buffer + text
        super(TextInputReadonly, self).set_text(self.buffer)


@dataclass
class SelectEnum:
    value: int = 0
    enum: typing.Type = None
    def get_ui(self):
        return MavicMaxGui.Selectbox(choice_dict={i.name: i.value for i in self.enum})
    def get(self):
        return self.value
    def set(self, value):
        self.value = value


class Slider(remi.gui.Slider):
    def __init__(self, *args, **kwargs):
        super(Slider, self).__init__(*args, **kwargs,  width=80, style={'text-align': 'right'})
        #self.attributes[Widget.EVENT_ONINPUT] = "this.nextElementSibling.value = this.value"
        self.onchange.do(lambda x,y: print("QWERTY", x,y))
    def get_text(self):
        return float(self.get_value())
    def set_text(self, text):
        super(Slider, self).set_value(text)


class SelectTextbox(remi.gui.DropDown):
    def __init__(self, choice_dict:dict, *args, **kwargs):
        super(SelectTextbox, self).__init__(*args, **kwargs)
        for text,key in choice_dict.items():
            self.append(text, key)
    def get_text(self):
        return str(self.get_value())
    def set_text(self, text):
        super(SelectTextbox, self).set_value(text)


@dataclass
class FloatMaxMinStep:
    value: float = 0.0
    min: float = 0.0
    max: float = 10.0
    step: float = 0.1

    def get_ui(self):
        return MavicMaxGui.Slider(default_value=0.0, min=self.min, max=self.max, step=self.step)
    def get(self):
        return self.value
    def set(self, value):
        self.value = value


class Selectbox(remi.gui.DropDown):
    def __init__(self, choice_dict:dict, *args, **kwargs):
        super(Selectbox, self).__init__(*args, **kwargs,  width=80, single_line=True, style={'text-align': 'right'})
        for text,key in choice_dict.items():
            self.append(text, key)

    def get_text(self):
        return self.get_key()

    def set_text(self, text):
        if type(text)==type({}):
            self.empty()
            for text, key in text.items():
                self.append(text, key)
        if super(Selectbox, self).get_key()==text: return
        super(Selectbox, self).set_value(text)


class Field():
    def __init__(self, text, value, type_, on_change_callback=None, meta_type=None):
        self.type = type_
        self.h_box = remi.gui.HBox(width='170')
        self.h_box.css_background_color = 'transparent'
        self.h_box.style['justify-content'] = 'space-between'
        self.h_box.style['align-items'] = 'flex-start'
        #lbl_value = remi.gui.Label(width=40, single_line=True, style={'text-align': 'right'})
        if meta_type:
            self.input = meta_type
            self.label = remi.gui.Label(text=text, style={'text-align': 'right'})
            self.h_box.append(self.label)
            self.input.onchange.do(lambda x, y: on_change_callback(text, self.input.get_text()))
            self.type = type_  # TODO Fulhack altid string

        elif type_==NodeCore.Event: #Button FIXME should be a type from NODE!!
            self.input = remi.gui.Button(text, margin='2px')
            self.input.onclick.do(lambda x:value.notify())
            self.label = remi.gui.Label(text=text, style={'text-align': 'right'})
            '''        if callable(type_): # Button
                        self.input = remi.gui.Button(text, margin='2px')
                        self.input.onclick.do(lambda x: value())
                        self.label = remi.gui.Label(text=text, style={'text-align': 'right'})
            '''
        elif type_ == type({}):  # Select box
            self.input = SelectTextbox(choice_dict=value, width=80, single_line=True, style={'text-align': 'right'})
            self.label = remi.gui.Label(text=text, style={'text-align': 'right'})
            self.h_box.append(self.label)
            self.input.onchange.do(lambda x, y: on_change_callback(text, y))
            self.type = type("")  # TODO Fulhack alltid string
        else:
            self.input = remi.gui.TextInput(width=80, single_line=True, style={'text-align': 'right'})
            self.input.set_text(str(value))
            self.label = remi.gui.Label(text=text, style={'text-align': 'right'})
            self.h_box.append(self.label)
            self.input.onchange.do(lambda x,y: on_change_callback(text,y))
        self.h_box.append(self.input)
        self.hbox = self.h_box

    def get_gui_widget(self):
        return self.hbox

    def set_value(self, value):
        try:
            if self.type==type(value):
                value=round(value,12)
        except:
            pass
        if type(self.input)==remi.gui.TextInput:
            self.input.set_text(str(value))
        elif type(self.input)==MavicMaxGui.Selectbox:
            self.input.set_text(value)
        else:
            self.input.set_text(value)


    def get_value(self) -> str:
        return self.input.get_text()


class View:
    #TODO
    # Bryt ut gui delen o lägg resten i app eller node, ev callback i node
    def __init__(self, gui_items_input: dict, gui_items_output: dict):
        self.input_fields: typing.Union[typing.Dict[Field, Field], {}] = {}
        self.output_fields: typing.Union[typing.Dict[Field, Field], {}] = {}
        self.changed_fields_from_gui={}
        hbox = remi.gui.HBox(width='100%')
        hbox.style['justify-content'] = 'space-between'
        hbox.style['align-items'] = 'flex-start'
        hbox.css_background_color = 'transparent'
        self.last_updated_input_fields={}
        self.last_updated_output_fields={}

        self.main_container = hbox

        self.input_container = self.create_fields(gui_items_input, self.input_fields)
        self.output_container = self.create_fields(gui_items_output, self.output_fields)

        self.info_field = TextInputReadonly(width=800, single_line=False, style={'font-size': '60%', 'text-align': 'left'}, height=600)
        #self.info_field = remi.gui.TextInput(width=600, single_line=False, style={'text-align': 'left'})
        self.info_field.css_background_color = 'transparent'
        self.info_field_text="INIT\n"
        self.info_field.set_text(self.info_field_text)


        self.main_container.append(self.input_container)
        #self.main_container.append(remi.gui.Button("QWERTY", margin='2px', width=400))
        self.main_container.append(self.info_field)
        self.main_container.append(self.output_container)

    def get_meta_data(self, field_name, all_items):
        meta_field_name = '_'+field_name
        if meta_field_name in all_items:
            return all_items[meta_field_name]
        return None

    def create_fields(self, gui_items, field_map):
        fields_container = remi.gui.Container()
        fields_container.css_background_color = 'transparent'
        fields_container.css_align_content = 'center'
        for field_name, value in gui_items.items():
            try:value=value.get()
            except: pass
            if field_name.startswith('_'):continue
            self.create_field(field_map, field_name, fields_container, value, self.save_change_field_from_gui, meta_type=self.get_meta_data(field_name, gui_items))
        return fields_container

    def save_change_field_from_gui(self, fieldname:str, value):
        self.changed_fields_from_gui.update({fieldname:value})
        print(f'{self.changed_fields_from_gui=}')

    def create_field(self, field_map, field_name, fields_container, value,on_change_callback=None, meta_type=None):
        log.info(f'{field_name=}')
        if field_name in field_map: return # Already exist, dont create another one
        w = Field(text=field_name, value=value, type_=type(value),on_change_callback=on_change_callback, meta_type=meta_type)
        widget = w.get_gui_widget()
        fields_container.append(widget)
        field_map.update({field_name: w})

    def get_view(self):
        return self.main_container

    def update_info_field(self, message:str):
        self.info_field.set_text(message)

    def update_output_fields(self, fields: dict):
        diff = self.diff_dict(fields, self.last_updated_output_fields)
        for field_name, value in diff.items():
            try:
                field = self.output_fields[field_name]
                field.set_value(field.type(value))
            except: #New dynamic field, create it now!
                log.exception("New field?")
                self.create_field(self.output_fields, field_name, self.output_container, value)
        self.last_updated_output_fields = copy.deepcopy(fields)

    def diff_dict(self, new: dict, old: dict):
        diff = {}
        for i in new:
            if type(new[i])==NodeCore.Event:
                continue
            if i not in old or new[i] != old[i]: diff.update({i: new[i]})
        return diff

    def update_input_fields(self, fields: dict):
        diff = self.diff_dict(fields, self.last_updated_input_fields)
        self.last_updated_input_fields = copy.deepcopy(fields)
        for field_name, value in diff.items():
            field = self.input_fields[field_name]
            try:
                field.set_value(value)
            except:
                log.exception('Todo wrong type when dict selectbox')


    def get_input_fields(self) -> typing.Dict[str, str]:
        input_field_values_dict = {}
        for field_name in self.input_fields:
            field = self.input_fields[field_name]
            value = "valueerror"
            try:
                value = field.type(field.get_value())
            except:
                value = field.get_value()
                pass
                #value = field.type(field.get_value())
            input_field_values_dict.update({field_name: value})
        return input_field_values_dict

    def get_changed_fields(self) -> typing.Dict[str, str]:
        input_field_values_dict = {}
        for field_name in self.changed_fields_from_gui:
            field = self.input_fields[field_name]
            value = "valueerror"
            try:
                value = field.type(field.get_value())
            except:
                value = field.get_value()
                pass
                #value = field.type(field.get_value())
            input_field_values_dict.update({field_name: value})
        self.changed_fields_from_gui={}
        return input_field_values_dict


class Select:
    def __init__(self, value, list_of_strings:[str]):
        self.list_of_strings = list_of_strings
        self.value = value

    def set(self, x):
        self.value = x

    def __repr__(self):
        return self.value
