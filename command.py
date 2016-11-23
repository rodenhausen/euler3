'''
@author: Thomas
'''
from autologging import logged
from pinject import copy_args_to_public_fields
from io import set_name
from io import get_tap
from io import store_tap
from io import set_current_tap

class Execution(object):
    def __init__(self, command):
        self.command = command
    def execute(self):
        self.command.run()
    
@logged
class Command(object):
    @copy_args_to_public_fields
    def __init__(self, tap):
        pass
    def run(self):
        self.__log.debug("run %s" % self.__class__.__name__)
        self.output = None
        self.executeOutput = None
    def get_output(self):
        return self.output
    def get_execute_output(self):
        return self.executeOutput
    
@logged 
class LoadTap(Command):
    @copy_args_to_public_fields
    def __init__(self, tap, input):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        tap = get_tap(self.input)
        set_current_tap(tap)
        store_tap(tap)
        self.output = "Tap: " + tap.get_id()
        return tap
    
@logged
class AddArticulation(Command):
    @copy_args_to_public_fields
    def __init__(self, tap, articulation):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.tap.add_articulation(self.articulation)
        set_current_tap(self.tap)
        store_tap(self.tap)
        self.output = "Tap: " + self.tap.get_id()
        return self.tap

@logged
class RemoveArticulation(Command):
    @copy_args_to_public_fields
    def __init__(self, tap, articulation):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.tap.remove_articulation(self.articulation)
        set_current_tap(self.tap)
        store_tap(self.tap)
        self.output = "Tap: " + self.tap.get_id()
        return self.tap
    
@logged
class NameTap(Command):
    @copy_args_to_public_fields
    def __init__(self, tap, name):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        set_name(self.name, self.tap);
        self.output = "Tap: " + self.tap.get_id()
        return self.tap
    
class UseTap(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.output = self.tap.__str__()
        return self.tap
            
class PrintTap(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.output = self.tap.__str__()
        return self.tap
    
class PrintTaxonomies(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.output = '\n'.join(self.tap.taxonomyA)
        self.output += '\n'.join(self.tap.taxonomyB)
        return self.tap
            
class PrintArticulations(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.output = '\n'.join(self.tap.articulations)
        return self.tap               
       
@logged 
class ShowPossibleWorlds(Command):
    @copy_args_to_public_fields
    def __init__(self, tap, reasoningReasoner):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
    
@logged 
class Graph(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)