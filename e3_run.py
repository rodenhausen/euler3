'''
Created on Nov 21, 2016

@author: Thomas
'''
import sys
from autologging import logged
import pinject
from pinject_config import Config
from pinject import copy_args_to_public_fields
from e3_io import get_current_tap, get_tap_id_and_name
import readline
import os
from e3_io import get_config
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
        current_tap = get_current_tap()
        if current_tap:
            print "Tap: %s" % get_tap_id_and_name(current_tap)
        else:
            print "Tap: None"
        while True:
            current_tap = get_current_tap()
            input = raw_input('euler2 > ')
            command = self.commandProvider.provide(current_tap, input)
            if command != None:
                command.run()
                if command.get_output():
                    for output in command.get_output():
                        print output
                if command.get_execute_output():
                    with open(os.devnull, 'w') as devnull:
                        for execute in command.get_execute_output():
                            p = Popen(execute, stdout=devnull, stderr=devnull, shell=True)
            else:
                print "Unrecognized command"