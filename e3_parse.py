'''
Created on Nov 22, 2016

@author: Thomas
'''
from autologging import logged
from pinject import copy_args_to_public_fields
import re
from e3_io import get_config
from e3_command import Graph
from e3_command import GraphWorlds
from e3_command import UseTap
from e3_command import NameTap
from e3_command import AddArticulation
from e3_command import RemoveArticulation
from e3_command import LoadTap
from e3_command import PrintArticulations
from e3_command import PrintTaxonomies
from e3_command import PrintTap
from e3_command import MoreWorldsOrEqualThan
from e3_command import IsConsistent
from e3_command import PrintWorlds
from e3_command import GraphInconsistency
from e3_command import PrintFix

@logged               
class CommandParser(object):
    @copy_args_to_public_fields
    def __init__(self, pattern):
        self.re = re.compile(pattern, re.IGNORECASE)
        self.config = get_config()
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

class MoreWorldsOrEqualThanParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '>= (.*) worlds')
    def get_command(self, tap, input):
        match = self.is_command(input);
        if match:
            return MoreWorldsOrEqualThan(tap, int(match.group(1)))
        else:
            raise Exception('Unrecognized command line')    

class GraphWorldsParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'graph worlds')
    def get_command(self, tap, input):
        return GraphWorlds(tap)

class GraphParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'graph$')
    def get_command(self, tap, input):
        return Graph(tap)
        
class IsConsistentParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'is consistent')
    def get_command(self, tap, input):
        return IsConsistent(tap)
                             
class PrintWorldsParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'print worlds')
    def get_command(self, tap, input):
        return PrintWorlds(tap)
                       
class GraphInconsistencyParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'graph inconsistency')
    def get_command(self, tap, input):
        return GraphInconsistency(tap)     
    
class PrintFixParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, 'print fix')
    def get_command(self, tap, input):
        return PrintFix(tap)    
                                                              
class CommandProvider(object):
    def __init__(self):
        #self.commands = Command.__subclasses__()#
        self.commandParsers = [ GraphWorldsParser(), 
                             GraphParser(), 
                             LoadTapParser(),
                             AddArticulationParser(),
                             RemoveArticulationParser(),
                             PrintArticulationsParser(),
                             PrintTapParser(),
                             PrintTaxonomiesParser(),
                             NameTapParser(),
                             MoreWorldsOrEqualThanParser(),
                             IsConsistentParser(),
                             PrintWorldsParser(),
                             GraphInconsistencyParser(),
                             PrintFixParser()
                             ]
    def provide(self, tap, input):
        for parser in self.commandParsers:
            if parser.is_command(input):
               return parser.get_command(tap, input)