'''
@author: Thomas
'''
from autologging import logged
from pinject import copy_args_to_public_fields
from e3_io import set_name
from e3_io import get_tap
from e3_io import store_tap
from e3_io import set_current_tap
from subprocess import Popen, PIPE, call
import os
from e3_io import get_config

class Execution(object):
    def __init__(self, command):
        self.command = command
    def execute(self):
        self.command.run()
    
@logged
class Command(object):
    @copy_args_to_public_fields
    def __init__(self, tap):
        self.config = get_config()
        pass
    def run(self):
        self.__log.debug("run %s" % self.__class__.__name__)
        self.output = []
        self.executeOutput = []
    def get_output(self):
        return self.output
    def get_execute_output(self):
        return self.executeOutput
    def run_euler(self, label, command, output):
        with open(os.path.join(output, '%s.stdout' % label), 'w+') as out:
            with open(os.path.join(output, '%s.stderr' % label), 'w+') as err:
                with open(os.path.join(output, '%s.returncode' % label), 'w+') as rc:
                    p = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
                    stdout, stderr = p.communicate()
                    #print stdout
                    #print stderr
                    out.write(stdout)
                    err.write(stderr)
                    rc.write('%s' % p.returncode)
    
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
        self.output.append("Tap: " + tap.get_id())
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
        self.output.append("Tap: " + self.tap.get_id())
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
        self.output.append("Tap: " + self.tap.get_id())
        return self.tap
    
@logged
class NameTap(Command):
    @copy_args_to_public_fields
    def __init__(self, tap, name):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        set_name(self.name, self.tap);
        self.output.append("Tap: " + self.tap.get_id())
        return self.tap
    
class UseTap(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.output.append(self.tap.__str__())
        return self.tap
            
class PrintTap(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.output.append(self.tap.__str__())
        return self.tap
    
class PrintTaxonomies(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.output.append('\n'.join(self.tap.taxonomyA))
        self.output.append('\n'.join(self.tap.taxonomyB))
        return self.tap
            
class PrintArticulations(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        self.output.append('\n'.join(self.tap.articulations))
        return self.tap                  
       
@logged 
class ShowPossibleWorlds(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        tapId = self.tap.get_id()
        tapFile = os.path.join(tapId, ".tap")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        alignCommand = '{eulerExecutable} align {tap} -o {output}'.format(eulerExecutable = eulerExecutable, 
            tap = tapFile, output = output);
        format = self.config['preferredImageFormat']
        showCommand = '{eulerExecutable} show -o {output} pw --{format}'.format(eulerExecutable = eulerExecutable, 
            output = output, format = format);
        self.run_euler("Align", alignCommand, output)
        self.run_euler("ShowPW", showCommand, output)
        
        
        maxPossibleWorldsToShow = self.config['maxPossibleWorldsToShow']
        possibleWorldsPath = os.path.join(tapId, "4-PWs")
        possibleWorldsCount = len([f for f in os.listdir(possibleWorldsPath) if f.endswith('.%s' % format) 
                                   and os.path.isfile(os.path.join(possibleWorldsPath, f))])
        if possibleWorldsCount <= maxPossibleWorldsToShow:
            self.output.append("There are {count} possible worlds. I show them all to you.".format(
                count = possibleWorldsCount))
        else:
            self.output.append("There are {count} possible worlds. I will only show {maxCount} of them to you.".format(
                count = possibleWorldsCount, maxCount = maxPossibleWorldsToShow))
        
        self.executeOutput = []
        openCount = 0
        for filename in os.listdir(os.path.join(tapId, "4-PWs")):
            if filename.endswith(".%s" % format) and openCount < maxPossibleWorldsToShow:
                openCount += 1
                self.executeOutput.append(self.config['imageViewer'].format(file = os.path.join(tapId, "4-PWs", filename)))
        
@logged 
class MoreWorldsOrEqualThan(Command):
    @copy_args_to_public_fields
    def __init__(self, tap, thanVariable):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        tapId = self.tap.get_id()
        tapFile = os.path.join(tapId, ".tap")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        alignCommand = '{eulerExecutable} align {tap} -o {output} -n {thanVariable}'.format(
            eulerExecutable = eulerExecutable, tap = tapFile, output = output, 
            thanVariable = self.thanVariable);
        self.run_euler("Align", alignCommand, output)
        
        aspOutputPath = os.path.join(tapId, "2-ASP-output", '.tap.pw')
        possibleWorldsCount = 0
        with open(aspOutputPath, 'r') as aspOutputFile:
            for line in aspOutputFile:
                if line.startswith('Possible world '):
                    possibleWorldsCount += 1
        if possibleWorldsCount < self.thanVariable:
            self.output.append("There are < {thanVariable} possible worlds. There are {count}.".format(
                thanVariable = self.thanVariable, count = possibleWorldsCount))
        else:
            self.output.append("There are >= {thanVariable} possible worlds.".format(
                thanVariable = self.thanVariable))
            
@logged 
class Graph(Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self, tap)
    def run(self):
        Command.run(self)
        tapId = self.tap.get_id()
        tapFile = os.path.join(tapId, ".tap")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        format = self.config['preferredImageFormat']
        showCommand = '{eulerExecutable} show iv {tap} -o {output} --{format}'.format(eulerExecutable = eulerExecutable, 
            tap = tapFile, output = output, format = format);
        self.run_euler("ShowIV", showCommand, output)
        
        self.output.append("Take a look at the graph")
        self.executeOutput = []
        for filename in os.listdir(os.path.join(tapId, "0-Input")):
            if filename.endswith(".%s" % format):
                self.executeOutput.append(self.config['imageViewer'].format(file = os.path.join(tapId, "0-Input", filename)))