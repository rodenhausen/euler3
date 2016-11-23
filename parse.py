'''
Created on Nov 22, 2016

@author: Thomas
'''
from autologging import logged
from pinject import copy_args_to_public_fields
import re
from command import Graph
from command import ShowPossibleWorlds
from command import UseTap
from command import NameTap
from command import AddArticulation
from command import RemoveArticulation
from command import LoadTap
from command import PrintArticulations
from command import PrintTaxonomies
from command import PrintTap

@logged               
class CommandParser(object):
    @copy_args_to_public_fields
    def __init__(self, pattern):
        self.re = re.compile(pattern, re.IGNORECASE)
        pass
    def is_command(self, input):
        return self.re.match(input)
    def get_command(self, tap, input):
        pass

class LoadTapParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'load tap (.*)')
    def get_command(self, tap, input):
        match = self.is_command(input);
        if match:
            return LoadTap(tap, match.group(1))
        else:
            raise Exception('Unrecognized command line')

class AddArticulationParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'add articulation (.*)')
    def get_command(self, tap, input):
        match = self.is_command(input);
        if match:
            return AddArticulation(tap, match.group(1))
        else:
            raise Exception('Unrecognized command line')

class RemoveArticulationParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'remove articulation (.*)')
    def get_command(self, tap, input):
        match = self.is_command(input);
        if match:
            return RemoveArticulation(tap, match.group(1))
        else:
            raise Exception('Unrecognized command line')

class NameTapParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'name tap (.*)')
    def get_command(self, tap, input):
        match = self.is_command(input);
        if match:
            return NameTap(tap, match.group(1))
        else:
            raise Exception('Unrecognized command line')
        
class PrintTapParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'print tap')
    def get_command(self, tap, input):
        match = self.is_command(input);
        if match:
            return PrintTap(tap)
        else:
            raise Exception('Unrecognized command line')
    
class PrintTaxonomiesParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'print taxonomies')
    def get_command(self, tap, input):
        match = self.is_command(input);
        if match:
            return PrintTaxonomies(tap)
        else:
            raise Exception('Unrecognized command line')   
         
class PrintArticulationsParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'print articulations')
    def get_command(self, tap, input):
        match = self.is_command(input);
        if match:
            return PrintArticulations(tap)
        else:
            raise Exception('Unrecognized command line')

class ShowPossibleWorldsParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'show possible worlds')
    def get_command(self, tap, input):
        return ShowPossibleWorlds(tap)

class GraphParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'graph')
    def get_command(self, tap, input):
        return Graph(tap)
                                   
class CommandProvider(object):
    def __init__(self):
        #self.commands = Command.__subclasses__()#
        self.commandParsers = [ ShowPossibleWorldsParser(), 
                             GraphParser(), 
                             LoadTapParser(),
                             AddArticulationParser(),
                             RemoveArticulationParser(),
                             PrintArticulationsParser(),
                             PrintTapParser(),
                             PrintTaxonomiesParser(),
                             NameTapParser()
                             ]
    def provide(self, tap, input):
        for parser in self.commandParsers:
            if parser.is_command(input):
               return parser.get_command(tap, input)