from __future__ import annotations
import csv
import dataclasses
import inspect
import logging
import shutil
import threading
import time
from abc import ABC, abstractmethod
from io import StringIO
from pathlib import Path
from pprint import pprint
from typing import Callable, Any
import config
import NodeCore #Must be here, due to automatic test
log = logging.getLogger(__name__)

#External dependencies
LOGDIR = Path(__file__).parent.joinpath('log')
def foo(a): pass
node_created_callback = foo
node_deleted_callback = foo

class P:
    def __init__(self, value):
        super().__init__()
        self._value = value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class Runtime():
    def __init__(self):
        pass

    def sleep(self):
        pass

    def sleep_until_next_execution(self):
        pass

    def wait(self, lambda_expression):
        while not lambda_expression():
            self.sleep_until_next_execution()

def filter_private(l, startswith='_'):
    return filter(lambda x: not x.startswith(startswith), l)

class Csv:
    def __init__(self, plugin:Node, in_file: Path, out_dir: Path):
        print(f"Input:{out_dir.as_posix()}")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = Path(out_dir.joinpath(f'{plugin.plugin_name}.csv'))
        print(f'Output:{out_file.as_posix()}')
        out_file.touch()
        self.out_file = None
        self.in_file = None
        self.in_vars = ['input.' + x for x in filter_private(plugin.input.__dict__)]
        self.out_vars = ['output.' + x for x in filter_private(plugin.output.__dict__)]
        self.plugin = plugin
        if in_file:
            self.in_file = in_file
            self.in_dict: {} = list(csv.DictReader(open(in_file)))
        if out_file:
            self.out_file = out_file
            column_names = ['clock_tick']+self.in_vars+self.out_vars+['log']+[self.plugin.node_name_path]
            self.out_writer_file = open(self.out_file, 'w', newline='')
            self.out_writer = csv.DictWriter(self.out_writer_file, fieldnames=column_names, quoting = csv.QUOTE_NONNUMERIC)
            self.out_writer.writeheader()
        self.d = {}


    def str_to_nbr(self, string):
        try:    return float(string)
        except:  return string

    def _fetch_input_from_dict(self, columns: {}):
        in_name: str
        for in_name, value  in columns.items():
            if in_name.startswith('input'):
                self.plugin.input.__getattribute__(in_name.split('.')[1]) # Fails if attribut doesn't exists. Doesn't do anything, just for fail
                #self.plugin.__setattr__(in_name, self.str_to_nbr(value))
                if value=='': continue
                if str(value).startswith('.'):
                    exec(f'self.plugin.{in_name}{value}') #Event
                else:
                    try:
                        exec(f'self.plugin.{in_name}.set({value})')
                    except:
                        exec(f'self.plugin.{in_name}={value}')

    def _compare_output_with_dict(self, row: {}) -> dict:
        out_name: str
        diff = {}
        for out_name, expected  in row.items():
            if out_name.startswith('output.'):
                try:
                    real = eval(f'self.plugin.{out_name}.get()')
                except:
                    real = eval(f'self.plugin.{out_name}')
                if isinstance(real, InOutClass): real = str(real)
                try:
                    if eval(str(expected)) != eval(str(real)):
                        diff.update({out_name: {'real':real, 'expected':expected}})
                except:
                    if expected != real:
                        diff.update({out_name: {'real':real, 'expected':expected}})
        return diff

    def save_output_to_file(self, clock_tick):
        def type_to_string(obj):
            LAMBDA = lambda: 0
            if isinstance(obj, type(LAMBDA)):
                return inspect.getsource(obj).replace('\n', '').split('=')[1]
            return obj

        if self.out_file:
            self.plugin.output.log = self.plugin.log_buffer.getvalue().replace('\n', '   ')
            self.plugin.log_buffer.truncate(0)
            self.plugin.log_buffer.seek(0)
            self.d = {}
            self.d.update({'clock_tick': clock_tick})
            for in_var in self.in_vars:
                try:
                    self.d.update({in_var: type_to_string(eval(f'self.plugin.{in_var}.get()'))}) #Class type
                except:
                    self.d.update({in_var: type_to_string(eval(f'self.plugin.{in_var}'))}) # Built in type
            for out_var in self.out_vars:
                try:
                    self.d.update({out_var: eval(f'self.plugin.{out_var}.get()')})
                except:
                    self.d.update({out_var: eval(f'self.plugin.{out_var}')})

            #d.update({'log': "qwerty"})
            self.out_writer.writerow(self.d)

    def run_test_with_validation_data(self, verif_dict: {} = None) -> []:
        log.info(f"{self.plugin.node_name_path} running test")
        all_diff=[]
        for clock_tick, columns in enumerate(verif_dict):
            log.info(f'\rclock_tick:{clock_tick}', end='')
            Node.clock_tick = clock_tick
            self._fetch_input_from_dict(columns)
            diff = {}
            self.plugin.execute_node()
            diff.update(self.check_missing_inputoutput_columns(columns))
            diff.update(self._compare_output_with_dict(columns))
            if diff:
                diff.update({'clock_tick': clock_tick})
                all_diff.append(diff)
                log.info(f" Diff ({clock_tick}):", diff)
        log.info('')
        if all_diff or len(verif_dict)<10:
            log.info(f'FAILED:{len(all_diff)} rows')
        else:
            log.info(f"SUCCESS {len(verif_dict)} rows")
        return all_diff

    def check_missing_inputoutput_columns(self, columns) -> dict:
        diff={}
        declared_columns = set.union(set([member for member in self.plugin.input.__annotations__]), set([member for member in self.plugin.output.__annotations__]))
        declared_columns = set(filter_private(declared_columns))
        testadata_columns = set([member.split('.')[1] for member in columns if member.startswith('input') or member.startswith('output')])
        missing_columns = declared_columns - testadata_columns
        if missing_columns: diff.update({'missing_columns': missing_columns})
        return diff

    def __del__(self):
        self.out_writer_file.close()
        pass

    def create_validation_data_file(self) -> None:
        for clock_tick in range(0,10):
            log.info(f'\rclock_tick:{clock_tick}', end='')
            Node.clock_tick = clock_tick
            self.plugin.execute_node()
        log.info(f'\n')


class InOutClass:
    def __init__(self, *args, **kwargs):
        pass
class Event(InOutClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callbacks = []
        self.last_value = ""

    def notify(self, *args, **kwargs):
        self.last_value = args
        for callback in self.callbacks:
            callback(*args, **kwargs)

    def register(self, callback):
        self.callbacks.append(callback)
        return callback

    def __repr__(self):
        if self.last_value == "": return ""
        ret = f'.notify{str(self.last_value)}'
        #self.last_value = ""
        return ret

class InputBase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class OutputBase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Node(ABC):
    _execution_list: list[Node]
    _all_plugins: list[Node] = []
    __names = []
    clock_tick: int = 0
    running: bool
    plugin_name:str
    blocking:bool = False


    def __init__(self, input, output, parent:Node, plugin_name:str=None, csv_in: Path=None, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        self._connections = []
        self.debug = {}
        self._execution_list = []
        self.parent = parent
        self.input = input
        self.output = output
        self.plugin_name = plugin_name
        self.node_name_path = self.get_unique_name(plugin_name)
        self.log = logging.getLogger(self.node_name_path)
        self.output.log = ""
        self.csv = Csv(self, csv_in, LOGDIR.joinpath(self.node_name_path))
        self.running = False
        self.timeout = 0.05
        self.run_in_threads = False
        self.log_buffer = StringIO()
        #handler = logging.StreamHandler(self.log_buffer)
        #handler.setFormatter(logging.Formatter('Line:%(lineno)s-%(message)s'))
        #self.log.addHandler(handler)
        #node_created_callback(self.node_name_path)

    def __del__(self):
        log.info(f'__del__ {self.node_name_path}')
        node_deleted_callback(self.node_name_path)

    def get_unique_name(self, plugin_name):
        name = self.__class__.__name__ if plugin_name is None else plugin_name
        if name in Node.__names:
            name_orig = name
            i=0
            while name in Node.__names:
                i=i+1
                name = name_orig + f'_{i}'
        Node.__names.append(name)
        if self.parent is not None:
            name = f'{self.parent.node_name_path}/{name}'
        return name

    def run_thread(self):
        self.output.log = "" # Create one in case we timeout
        self.running = True
        self.run()
        self.running = False
        self.csv.save_output_to_file(Node.clock_tick)
        self.run_post()
        self.blocking=False

    def update_input_fields_from_dict(self, fields_dict:{}):
        for field_name,  value in fields_dict.items():
            try:
                getattr(self.input, field_name).set(value) #class
            except:
                self.input.__setattr__(field_name,value) #builtin



    def execute_node(self):
        if self.running:
            return
        if self.run_in_threads:
            t = threading.Thread(target=self.run_thread)
            t.start()
            t.join(timeout=self.timeout)
            if t.is_alive() and not self.blocking:
                #log.info(f"WARNING: {self.node_name_path} didn't complete")
                self.blocking = True
        else:
            self.run_thread()


    @abstractmethod
    def run(self):
        pass

    def run_post(self):
        pass

    def main_loop(self):
        pass

    def connect_external_inputs(self):
        pass

def plugin_name(file_name:str):
    return Path(file_name).name.split('.')[0]


class General(Node):
    def __init__(self, init=None, run=None, run_post=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run_function,self.run_post_function = run, run_post
        if init:
            init(self.input, self.output, self.log)

    def run(self):
        if self.run_function:
            self.run_function(self.input, self.output, self.log)

    def run_post(self):
        if self.run_post_function:
            self.run_post_function(self.input, self.output, self.log)


def test_node_with_csv(module_name: str, csv_dir_path: Path):
    exec(f'import {module_name}')
    csv_name = f"{module_name.split('.')[-1]}.csv"
    csv_file = Path(f'{csv_dir_path}/{csv_name}')
    log.info(f'test_node_with_csv({module_name}) with data from:{csv_file}')
    dut: NodeCore.Node = eval(f'{module_name}.create_node()')

    try:
        validation_data = list(csv.DictReader(open(csv_file)))
    except FileNotFoundError:
        log.info(f"Generating new file")
        dut.csv.create_validation_data_file()
        diff={'input file not found. Generated new in': f'{dut.csv.out_file.as_posix()}'}
        return diff
    diff = dut.csv.run_test_with_validation_data(validation_data)
    return diff


def get_all_nodes_in_dir(dir_path: Path) -> [Path]:
    p = Path(dir_path).glob('**/*.py')
    list_of_nodes = []
    for pathname in p:
        name = pathname.name
        #log.info(name)
        if name.endswith('.py') and not name.startswith('__'):
            relative_path_to_import = pathname.absolute().relative_to(config.test_settings.root_dir)
            list_of_nodes.append(relative_path_to_import.as_posix().replace('/','.').replace('.py', ''))
    return list_of_nodes

def test_nodes_in_dir(modules_dir: Path, csv_dir_path: Path, exclude:[str]):
    diff_all = {}
    list_of_nodes = get_all_nodes_in_dir(Path(modules_dir))
    if len(list_of_nodes)==0: diff_all.update({'no nodes tested': modules_dir})
    for node_name in list_of_nodes:
        print(f"Test node:{node_name} with data in {csv_dir_path}")
        if node_name in exclude:
            print("Excluded from test")
            continue
        diff = test_node_with_csv(node_name, csv_dir_path=csv_dir_path)
        if diff:
            diff_all.update({node_name: diff})
    return diff_all

def run_self_test(modules_dir: Path=Path('./nodes'), csv_dir_path:Path=Path('./csv_testdata'),  repeat: int=2, exclude:[str]=[]):
    shutil.rmtree(config.test_settings.csv_dir_test, ignore_errors=True)
    for repeating in range(repeat):
        diff = test_nodes_in_dir(modules_dir=modules_dir, csv_dir_path=csv_dir_path, exclude=exclude)
        if diff:
            pprint(diff)
            log.info("WARNING: ERROR detected")
            return 1
        log.info("ALL TESTS PASSED")
    return 0

def run_from_main(node_file: str, import_base='NodeCore.test_nodes.nodes.', csv_dir_path=Path('../csv_testdata')):
    from pathlib import Path
    localname = Path(node_file).name.replace('.py', '')
    diff = NodeCore.test_node_with_csv(import_base + localname, csv_dir_path=csv_dir_path)
    log.info("Diff", diff)

