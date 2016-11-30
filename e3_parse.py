'''
Created on Nov 22, 2016

@author: Thomas
'''
from autologging import logged
from pinject import copy_args_to_public_fields
import re
from e3_io import get_config, get_tap_from_id_or_name
from e3_command import GraphTap, GraphWorlds, UseTap, NameTap, AddArticulation, RemoveArticulation, LoadTap, PrintArticulations, PrintTaxonomies, PrintTap
from e3_command import MoreWorldsOrEqualThan, IsConsistent, PrintWorlds, GraphInconsistency, PrintFix, PrintNames, ClearNames

@logged               
class CommandParser(object):
    @copy_args_to_public_fields
    def __init__(self, pattern):
        self.re = re.compile(pattern, re.IGNORECASE)
        self.config = get_config()
        pass
    def is_command(self, input):
        return self.re.match(input)
    def get_command(self, current_tap, input):
        pass

class LoadTapParser(CommandParser):
    def __init__(self):
        #example:
        #load tap abstract.txt
        CommandParser.__init__(self, '^load tap (\S*)$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            return LoadTap(match.group(1))
        else:
            raise Exception('Unrecognized command line')

class AddArticulationParser(CommandParser):
    def __init__(self):
        #example: 
        #add articulation [1.A equals 2.B]
        #add articulation [1.A equals 2.B] 2312842819299391
        #add articulation [1.A equals 2.B] my_tap_name
        CommandParser.__init__(self, '^add articulation (\[.*\])( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(2) and match.group(3):
                tap = get_tap_from_id_or_name(match.group(3))  
            if tap:          
                return AddArticulation(tap, match.group(1))
            else:
                raise Exception('Tap %s not found' % match.group(3))
        else:
            raise Exception('Unrecognized command line')

class RemoveArticulationParser(CommandParser):
    def __init__(self):
        #example: 
        #remove articulation 1
        #remove articulation 1 2312842819299391
        #remove articulation 1 my_tap_name
        CommandParser.__init__(self, '^remove articulation (\d+)( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(2) and match.group(3):
                tap = get_tap_from_id_or_name(match.group(3))
            if tap:
                return RemoveArticulation(tap, match.group(1))
            else:
                raise Exception('Tap %s not found' % match.group(3))
        else:
            raise Exception('Unrecognized command line')

class NameTapParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^name tap (\S*)( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input);
        if match:
            tap = current_tap
            if match.group(2) and match.group(3):
                tap = get_tap_from_id_or_name(match.group(3))
            if tap:
                return NameTap(tap, match.group(1))
            else:
                raise Exception('Tap %s not found' % match.group(3))
        else:
            raise Exception('Unrecognized command line')

class PrintNamesParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^print names$')
    def get_command(self, current_tap, input):
        match = self.is_command(input);
        if match:
            return PrintNames()
        else:
            raise Exception('Unrecognized command line')

class ClearNamesParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^clear names$')
    def get_command(self, current_tap, input):
        match = self.is_command(input);
        if match:
            return ClearNames()
        else:
            raise Exception('Unrecognized command line')


class UseTapParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^use tap (\S+)$')
    def get_command(self, current_tap, input):
        match = self.is_command(input);
        if match:
            tap = get_tap_from_id_or_name(match.group(1))
            if tap:
                return UseTap(tap)
            else:
                raise Exception('Tap %s not found' % match.group(1))
        else:
            raise Exception('Unrecognized command line')
        
class PrintTapParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^print tap( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return PrintTap(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')
    
class PrintTaxonomiesParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^print taxonomies( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return PrintTaxonomies(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')   
         
class PrintArticulationsParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^print articulations( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)    
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return PrintArticulations(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')

class MoreWorldsOrEqualThanParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^>= (\d+) worlds( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(2) and match.group(3):
                tap = get_tap_from_id_or_name(match.group(3))
            if tap:
                return MoreWorldsOrEqualThan(tap, int(match.group(1)))
            else:
                raise Exception('Tap %s not found' % match.group(3))
        else:
            raise Exception('Unrecognized command line')

class GraphWorldsParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^graph worlds( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return GraphWorlds(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')

class GraphTapParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^graph tap( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return GraphTap(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')
        
class IsConsistentParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^is consistent( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return IsConsistent(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')
                             
class PrintWorldsParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^print worlds( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return PrintWorlds(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')
                       
class GraphInconsistencyParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^graph inconsistency( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return GraphInconsistency(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')   
    
class PrintFixParser(CommandParser):
    def __init__(self):
        CommandParser.__init__(self, '^print fix( (\S*))?$')
    def get_command(self, current_tap, input):
        match = self.is_command(input)
        if match:
            tap = current_tap
            if match.group(1) and match.group(2):
                tap = get_tap_from_id_or_name(match.group(2))
            if tap:
                return PrintFix(tap)
            else:
                raise Exception('Tap %s not found' % match.group(2))
        else:
            raise Exception('Unrecognized command line')
                                                              
class CommandProvider(object):
    def __init__(self):
        #self.commands = Command.__subclasses__()#
        self.commandParsers = [ GraphWorldsParser(), 
                             GraphTapParser(), 
                             UseTapParser(), 
                             LoadTapParser(),
                             PrintNamesParser(),
                             ClearNamesParser(),
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
    def provide(self, current_tap, input):
        for parser in self.commandParsers:
            if parser.is_command(input):
               return parser.get_command(current_tap, input)