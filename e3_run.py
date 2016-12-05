'''
Created on Nov 21, 2016

@author: Thomas
'''
import sys
from autologging import logged
import pinject
from pinject_config import Config
from pinject import copy_args_to_public_fields
import readline
import os
from subprocess import Popen, PIPE, call

@logged
class Run(object):
    def __init__(self):
        pass
    def run(self):
        pass
    
@logged
class OneShot(Run):
    @copy_args_to_public_fields
    def __init__(self, commandLineProvider):
        Run.__init__(self)
    def run(self):
        input = ' '.join(sys.argv[1:])
        commandLine = self.commandLineProvider.provide(input)
        if commandLine != None:
            pass
            #self.config.command = commandLine.commandClass 
            #self.obj_graph = pinject.new_object_graph(binding_specs=[self.config])
            #execution = self.obj_graph.provide(Execution)
            #execution.execute()
        else:
            print "Unrecognized command"
        
@logged 
class Interactive(Run):
    @copy_args_to_public_fields
    def __init__(self, commandProvider):
        Run.__init__(self)
    def run(self):
        import e3_io
        current_tap = e3_io.get_current_tap()
        if current_tap:
            print "Tap: %s" % e3_io.get_tap_id_and_name(current_tap)
        else:
            print "Tap: None"
        while True:
            input = raw_input('e3 > ')
            command = self.commandProvider.provide(input)
            if command != None:
                command.run()
                e3_io.append_project_history(input, command)
                if command.get_output():
                    for output in command.get_output():
                        print output
                if command.get_execute_output():
                    with open(os.devnull, 'w') as devnull:
                        for execute in command.get_execute_output():
                            if execute == 'Exit':
                                sys.exit()
                            else:
                                p = Popen(execute, stdout=devnull, stderr=devnull, shell=True)
            else:
                print "Unrecognized command"