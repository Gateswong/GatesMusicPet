# -*- coding: utf-8 -*-

import os
from subprocess import check_output, CalledProcessError
from shutil import copy
from collections import defaultdict


class Action(object):

    def __init__(self):
        self.action_table = {}
        self.command_table = defaultdict(list)

    def reset(self):
        self.command_table = defaultdict(list)

    def add_command(self, sequence, action, **kwargs):
        if type(sequence) != int:
            raise TypeError("sequence must be an integer.")
        self.command_table[sequence].append((action, kwargs))

    def run(self, command):
        if command[0] not in self.action_table:
            raise ValueError("Action '%s' not registed" % command[0])
        self.action_table[command[0]](**command[1])

    def run_all(self):
        for i in sorted(self.command_table.keys()):
            for command in self.command_table[i]:
                self.run(command)

    def success(self, arg, action_name):
        return {
            u"status": u"success",
            u"action": action_name,
            u"output": arg,
        }

    def arg_not_exists(self, arg, action_name):
        return {
            u"status": u"failed",
            u"reason": u"A key '%s' is needed in action '%s'." % (arg, action_name),
        }


class SystemCallActionMixin(object):

    def __init__(self):
        self.regist_actions()

    def regist_actions(self):
        self.action_table.update({
            u"system_call": self.do_system_call,
        })

    def add_system_call(self, sequence, cmd):
        self.add_command(sequence, u"system_call", {u"cmd": cmd})

    def do_system_call(self, **kwargs):
        cmd = kwargs.pop(u"cmd", None)
        if cmd is None: return self.arg_not_exists(u"cmd", u"system_call")

        try:
            p = check_output(cmd, shell=True)
        except CalledProcessError as ex:
            return {
                u"status": u"failed",
                u"reason": u"System call returns an error: %s." % ex.returncode,
                u"output": ex.output,
            }

        return self.success(p, u"system_call")


class FileActionMixin(object):

    def __init__(self):
        self.regist_actions()

    def regist_actions(self):
        self.action_table.update({
            u"copy": self.do_copy,
            u"delete": self.do_delete,
        })

    def add_copy(self, sequence, src, dst):
        self.add_command(sequence, u"copy", {u"src":src, u"dst":dst})

    def add_delete(self, sequence, target):
        self.add_command(sequence, u"delete", {u"file":target})

    def do_copy(self, **kwargs):
        src = kwargs.pop(u"src", None)
        if src is None: return self.arg_not_exists(u"src", u"copy")
        dst = kwargs.pop(u"dst", None)
        if dst is None: return self.arg_not_exists(u"dst", u"copy")

        try:
            copy(src, dst)
        except IOError as ex:
            return {
                u"status": u"failed",
                u"reason": u"Unable to copy file.",
                u"output": ex.message(),
            }

        return self.success(u'''Copy completed: "%s" --> "%s".''' % (src, dst), u"copy")

    def do_delete(self, **kwargs):
        target = kwargs.pop(u"file", None)
        if target is None: return self.arg_not_exists(u"file", u"delete")

        try:
            os.remove(target)
        except IOError as ex:
            return {
                u"status": u"failed",
                u"reason": u"Unable to delete file: %s" % target,
                u"output": ex.message(),
            }

        return self.success(u'''Delete completed: "%s".''' % target, u"delete")



