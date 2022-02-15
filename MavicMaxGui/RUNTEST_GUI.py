import time
from enum import Enum

import remi.gui

import MavicMaxGui
import _thread

import glob
def scan_for_plugins(base_dir: str="/mavicmax/git/MavicMaxScripts/scripts/") -> [str]:
    l = glob.glob(f'{base_dir}**/*.py', recursive=True)
    ll= sorted(filter(lambda x: not '__' in x,l))
    lll = [x.replace(base_dir, "") for x in ll]
    return lll

class TestEnum(Enum):
    AA=1
    BB=2
    CC=3
    DD=4
    EE=5
    FF=6
    GG=7


def run():
    def add_plugin1():
        parameters ={"par1________________A": "1", "par2": "2"}
        predefined_args = {"last_time": {"par1": "11111", "par2": "222222"}, "highspeed": {"par1": "QWER", "par2": "ASDF", "par3": "qqqqq"}}
        MavicMaxGui.Dialog.Start.show(title="start",
                                      args=parameters,
                                      predefined_args=predefined_args,
                                      start_callback=lambda items: print(f"OK:{items}"),
                                      view_callback=lambda file: print(f"View:{file}"),
                                      help_callback=lambda :MavicMaxGui.Dialog.Popup.show("Help", message="Help text\nDo nothing", level=2, ok_callback=lambda x:print("callback")))
    def add_plugin2():
        parameters ={"_par1": "_1", "_par2": "_2", "select1": {"Normal":"1", "Sport":"2"}}
        predefined_args = {"_last_time": {"select1":"Sport", "_par1": "_11111", "_par2": "_222222"}, "_highspeed": {"select1":"Normal", "_par1": "_QWER", "_par2": "_ASDF", "_par3": "_qqqqq"}}
        MavicMaxGui.Dialog.Start.show(title="start",
                                      args=parameters,
                                      predefined_args=predefined_args,
                                      start_callback=lambda items: print(f"OK:{items}"),
                                      view_callback=lambda file: print(f"View:{file}"))

    def create_menu():
        for i in scan_for_plugins():
            MavicMaxGui.menu.add_menu_item("/start/"+i, lambda x, i=i: MavicMaxGui.Dialog.Popup.show(f"Opened from menu:{i}", message=x.text, ok_callback=lambda x:print("callback")))

        MavicMaxGui.menu.add_menu_item("/other/qq/File", lambda x: MavicMaxGui.Dialog.File.show("Pick file",
                                                                                                lambda file: print(f"OK:{file}"),
                                                                                                lambda file: print(f"View:{file}")))
        MavicMaxGui.menu.add_menu_item("/other/qq/Popup", lambda x: MavicMaxGui.Dialog.Popup.show("Opened from menu", message=x.text, ok_callback=lambda x:print("callback")))

        MavicMaxGui.menu.add_menu_item("/Q/DialogPlugin1", lambda _: add_plugin1() )
        MavicMaxGui.menu.add_menu_item("/Q/DialogPlugin2_withchoice", lambda _: add_plugin2() )

        MavicMaxGui.menu.add_menu_item("/other/qq/PopupLevel2/PopupLevel2_1", lambda x: MavicMaxGui.Dialog.Popup.show("Opened from menu2_1", message=x.text+'_2', level=2, ok_callback=lambda x:print("callback")))
        MavicMaxGui.menu.add_menu_item("/other/qq/PopupLevel2/PopupLevel2_2", lambda x: MavicMaxGui.Dialog.Popup.show("Opened from menu2_2", message=x.text+'_2', level=2, ok_callback=lambda x:print("callback")))
        MavicMaxGui.menu.add_menu_item("/other/qq/PopupLevel2/PopupLevel2_3", lambda x: print("QQQQ"))
        MavicMaxGui.menu.add_menu_item("/other/qq/PopupLevel2", lambda x: print("WWWW"))

        MavicMaxGui.menu.add_menu_item("/other/qq/PopupLevel2/PopupLevel2_1/A/B/C", lambda x: MavicMaxGui.Dialog.Popup.show("C", message=x.text+'_C', level=2, ok_callback=lambda x:print("callback")))
        menu_name='shouldnt_be_here'
        MavicMaxGui.menu.add_menu_item(f"/other/qqq/www/{menu_name}1")
        MavicMaxGui.menu.add_menu_item(f"/other/qqq/www/{menu_name}2")
        #MavicMaxGui.menu.add_menu_item(f"/other/qqq/www/{menu_name}3")
        MavicMaxGui.menu.add_menu_item(f"/other/qqq")
        MavicMaxGui.menu.rm_menu_item(f"/other/qqq/www/{menu_name}2")
        MavicMaxGui.menu.rm_menu_item(f"/other/qqq/www/{menu_name}1")
        MavicMaxGui.menu.rm_menu_item(f"/other/qqq")

        def test_view():
            # fields = o.__dict__
            print("ENUM", TestEnum.__dict__)
            selectbox=MavicMaxGui.SelectTextbox(choice_dict={"QNormal": "1", "QSport": "2", "QSport2": "3", "QSport3": "4"}, width=80, single_line=True, style={'text-align': 'right'})
            slider = MavicMaxGui.Slider = MavicMaxGui.Slider(default_value=0, min=0, max=10, step=1)
            view = MavicMaxGui.View(
                gui_items_input={"zero": lambda: view.update_output_fields({"speed": 0, "height": 0, "radius": 0}),
                                 "select1": 'aaa',
                                 "_select1": selectbox,
                                 'enum':{"Normal":"1", "Sport":"2", "Sport2":"3", "Sport3":"4"},
                                 "s": 2.43, "height": 2.34, "radius": 5000, "msg": "Takeoff",
                                 "slider": 5,
                                 "_slider": slider,
                                 '_should_not_be_seen':"hide me"},
                gui_items_output={"speed": 2.43, "height": 4.34, "radius": 5011,  "selected": "5011"})
            MavicMaxGui.MyApp.show_view(view)
            view.update_output_fields({"speed": 999 , "radius": 777, "new_value": 123})
            for i in range(0, 25):
                all_inputs = view.get_input_fields()
                selected = {'selected':all_inputs['select1']}
                view.update_output_fields(selected)
                time.sleep(0.05)
                view.update_output_fields({"speed": 999 - i, "height": 888 - i, "radius": 777 - i})
                view.update_info_field(f'speed:{999-i}\n')
                view.update_output_fields({f"new_value_{i+3}": i})
                print("Read changed values", view.get_changed_fields())
                time.sleep(0.1)
            #print("Read inout values", view.get_input_fields())
            view.update_output_fields({"new_value_27": 99})
            view.update_output_fields({"new_value_3": 3})

            # Change selectbox content
            '''
            view.update_input_fields({"select1": {"QQNormal2": "1",
                                                  "QQSport2": "2",
                                                  }})
                                                  '''
            # view.update_input_fields({"select2": {"QQNormal4": "1", "QQSport4": "2"}})
            selectbox.append("KUKUKU")

        MavicMaxGui.menu.add_menu_item(f"/views/testview", callback=lambda x:_thread.start_new_thread(test_view, ()))





    port = 8078
    _thread.start_new_thread( create_menu, () )
    _thread.start_new_thread(MavicMaxGui.start_www, (port, ))
    time.sleep(2)

    # Need connect from browser
    #MavicMaxGui.Dialog.Popup.show("Welcome", message='MavicMax started<br>\r\nNew line', ok_callback=lambda x: print("callback"))
    time.sleep(20)


if __name__ == "__main__":
    run()

