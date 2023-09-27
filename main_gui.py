#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import functools
from shutil import copyfile
import tkinter
from tkinter import END, Button, Label, Text, Tk, INSERT
from tkinter import ttk

g_window = Tk()
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))


class AutoIcon:
    def __init__(self, name, _type=0, default=None, explain=None):
        if not explain:
            explain = name
        self.name = name
        self.label = Label(g_window, text=explain)
        if _type == 0:
            self.icon = Text(g_window, height=1, width=32)
            self.icon.insert(INSERT, "" if default is None else default)
        elif _type == 1:
            self.icon = ttk.Combobox(g_window)
            self.icon['value'] = default
        elif _type == 2:
            self.icon = ttk.Checkbutton(g_window)

    def grid(self, row):
        self.label.grid(row=row, column=0)
        self.icon.grid(row=row, column=1)

    def get_dict(self):
        if isinstance(self.icon, Text):
            return {self.name: self.icon.get(1.0, END).strip('\n')}
        elif isinstance(self.icon, ttk.Combobox):
            return {self.name: self.icon.get()}


class SleepyDogGUI:
    def __init__(self, init_window_name):
        self.window = init_window_name
        self.arg_list = []
        self._row = 0
        self.icon_list = [AutoIcon("API_TYPE", _type=1, default=("同步", "异步")),
                          AutoIcon("EUREKA_HOST_NAME", explain="注册中心host名称(小写)"),
                          AutoIcon("EUREKA_APP_NAME", explain="注册中心app名称(大写)"),
                          AutoIcon("APOLLO_ID", explain="Apollo id"),
                          AutoIcon("APOLLO_NAMESPACE", default='datawork-common'),
                          AutoIcon("APP_URL", default='/aidata/example', explain="url,只写后缀"),
                          AutoIcon("APOLLO_TOPIC", _type=1, default=("speech", "image", "text", "other")),
                          AutoIcon("BIZ_TYPE", _type=1, default=("datawork-speech", "datawork-image",
                                                                 "datawork-text", "datawork-other"))]

        self._init()

    def _init(self):
        self.window.title("sleepy dog: 繁琐的事情交给我,你去睡觉")
        self.button_gen = Button(self.window, text='生成', command=self.generate)
        self.button_gen.grid(row=0, column=2)

        for item in self.icon_list:
            item.grid(self._row)
            self._row += 1

        Label(self.window, text="name").grid(row=self._row, column=0)
        Label(self.window, text="type").grid(row=self._row, column=1)
        Label(self.window, text="required").grid(row=self._row, column=2)
        # Label(self.window, text="choices").grid(row=self._row, column=3)
        Label(self.window, text="default").grid(row=self._row, column=3)
        self.button_add_arg = Button(self.window, text="+", command=self.add_arg)
        self.button_add_arg.grid(row=self._row, column=4)
        self._row += 1

    def add_arg(self):
        tmp = [Text(self.window, height=1, width=32)]
        type_box = ttk.Combobox(self.window)
        type_box['value'] = ('str', 'int', 'float', 'dict', 'list', 'url')
        type_box.set('str')
        tmp.append(type_box)
        tmp.append(ttk.Checkbutton(self.window))
        tmp.append(Text(self.window, height=1, width=32))
        # tmp.append(Text(self.window, height=1, width=32))
        tmp.append(Button(self.window, text='-', command=functools.partial(self.remove_arg, len(self.arg_list))))
        for col, item in enumerate(tmp):
            item.grid(row=self._row, column=col)
        self.arg_list.append(tmp)
        self._row += 1

    def remove_arg(self, idx):
        for item in self.arg_list[idx]:
            item.grid_forget()

    def get_var(self):
        ret = {}
        for item in self.icon_list:
            ret.update(item.get_dict())
        arg = []
        for item in self.arg_list:
            if item[0].grid_info():
                arg.append({
                    "name": item[0].get(1.0, END).strip('\n'),
                    "type": item[1].get(),
                    "required": 'selected' in item[2].state(),
                    # "choices": item[3].get(1.0, END).strip('\n'),
                    "default": item[3].get(1.0, END).strip('\n'),
                })
        return ret, arg

    def _make_config(self, build_sleepy_dog, config):
        text = ""
        for name, value in config.items():
            text += "    %s = os.environ.get('%s') or '%s'\n" % (name, name, value)
        text = text.replace('同步', '0').replace('异步', '1')
        # print(text)
        with open(os.path.join(BASE_FOLDER, 'sleepy_dog', 'c_config.py'), 'r') as f:
            content = f.read()
        with open(os.path.join(build_sleepy_dog, 'c_config.py'), 'w') as f:
            for line in content.split('\n'):
                f.write(line + '\n')
                if "@config" in line:
                    f.write(text)

    def _make_app(self, folder, arg):
        text = ""
        for item in arg:
            if not item['name']:
                continue
            text += "parser.add_arguments('%s', required=%s, default=%s, type=%s)\n" % (item['name'],
                     str(item['required']),
                     "'%s'" % item['default'] if item['type'] in ('str', 'url') else item['default'],
                     item['type'])
        text = text.replace("default='',", "")
        # print(text)

        with open(os.path.join(BASE_FOLDER, 'sleepy_dog', 'flask_app.py'), 'r') as f:
            content = f.read()
        with open(os.path.join(folder, 'flask_app.py'), 'w') as f:
            for line in content.split('\n'):
                f.write(line + '\n')
                if "@arg_parse" in line:
                    f.write(text)

    def _copy_file(self, config, arg):
        build_folder = os.path.join(BASE_FOLDER, "build")
        build_sleepy_dog = os.path.join(build_folder, "sleepy_dog")
        if not os.path.exists(build_folder):
            os.mkdir(build_folder)
        if not os.path.exists(build_sleepy_dog):
            os.mkdir(build_sleepy_dog)
        sleepy_dog = os.path.join(BASE_FOLDER, 'sleepy_dog')
        for name in os.listdir(sleepy_dog):
            if name.endswith('.py'):
                copyfile(os.path.join(sleepy_dog, name), os.path.join(build_sleepy_dog, name))

        self._make_config(build_sleepy_dog, config)
        self._make_app(build_folder, arg)

    def generate(self):
        config, arg = self.get_var()
        # print(config, arg)
        self._copy_file(config, arg)


def gui_start():
    SleepyDogGUI(g_window)
    g_window.mainloop()


gui_start()
