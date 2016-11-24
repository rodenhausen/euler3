'''
Created on Nov 21, 2016

@author: Thomas
'''
import sys
from autologging import logged
import pinject
from pinject_config import Config
from pinject import copy_args_to_public_fields
from io import get_current_tap

@logged
class Run(object):
    def __init__(self):
        self.config = Config()
    
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
        history = []
        if not os.path.isfile('.history'):
            with open('.history', 'r') as historyFile:
                for command in historyFile:
                    history.append(command)
        while True:
            tap = get_current_tap()
            input = raw_input('euler2 > ')
            history.append(input)
            command = self.commandProvider.provide(tap, input)
            if command != None:
                command.run()
                if command.get_output():
                    print command.get_output()
                if command.get_execute_output():
                    pass
                    #todo
            else:
                print "Unrecognized command"
        with open('.history', 'a') as historyFile:
            for command in history:
                historyFile.write(command + "\n")