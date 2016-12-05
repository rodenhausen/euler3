'''
@author: Thomas
'''
from autologging import logged
from pinject import copy_args_to_public_fields
import e3_io
#from e3_io import set_name, get_tap_from_cleantax, get_tap, store_tap, set_current_tap, get_config, get_tap_id_and_name, get_names, clear_names
from subprocess import Popen, PIPE, call
import os
import e3_parse
    
@logged
class Command(object):
    @copy_args_to_public_fields
    def __init__(self):
        self.config = e3_io.get_config()
        self.output = []
        self.executeOutput = []
        pass
    def run(self):
        self.__log.debug("run %s" % self.__class__.__name__)
    def get_output(self):
        return self.output
    def get_execute_output(self):
        return self.executeOutput
    
@logged
class MiscCommand(Command):
    @copy_args_to_public_fields
    def __init__(self):
        Command.__init__(self)
    def run(self):
        Command.run(self)
                    
class Euler2Command(Command):
    def __init__(self):
        Command.__init__(self)
    def run(self):
        Command.run(self)
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
    def is_complete(self):
        return False
    
class ModelCommand(Command):                    
    def __init__(self):
        Command.__init__(self)
    def run(self):
        Command.run(self)    
                    
@logged 
class Bye(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self):
        Command.__init__(self)
    def run(self):
        self.output.append("See you soon!")
        self.executeOutput.append("Exit")
        
@logged 
class Help(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        for commandParser in e3_parse.commandParsers:
            help = commandParser.get_help()
            if help:
                self.output.append(commandParser.get_help())
                
@logged
class NameTap(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, tap, name):
        Command.__init__(self)
    def run(self):
        Command.run(self)
        e3_io.set_name(self.name, self.tap);
        self.output.append("Tap: " + e3_io.get_tap_id_and_name(self.tap))
                
class PrintNames(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        names = e3_io.get_names()
        if names:
            self.output.append('\n'.join(names))
        else:
            self.output.append('No names recorded.')
    
class ClearNames(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        e3_io.clear_names()
        self.output.append("Names are cleared")
    
class PrintTap(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, tap):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        self.output.append(self.tap.__str__())
    
class PrintTaxonomies(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, tap):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        indices = ['']
        for x in range(1, len(self.tap.taxonomyA)):
            indices.append(str(x) + ". ")
        taxonomyALines = [x + y for x, y in zip(indices, self.tap.taxonomyA)]
        self.output.append('\n'.join(taxonomyALines))
        indices = ['']
        for x in range(1, len(self.tap.taxonomyB)):
            indices.append(str(x) + ". ")
        taxonomyBLines = [x + y for x, y in zip(indices, self.tap.taxonomyB)]
        self.output.append('\n'.join(taxonomyBLines))
            
class PrintArticulations(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, tap):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)        
        indices = ['']
        for x in range(1, len(self.tap.articulations)):
            indices.append(str(x) + ". ")
        articulationLines = [x + y for x, y in zip(indices, self.tap.articulations)]
        self.output.append('\n'.join(articulationLines))
    
@logged
class CreateProject(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, name):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        if os.path.isdir(os.path.join('projects', self.name)):
            self.output.append('A project with name ' + self.name + ' already exists')
            return
        os.makedirs(os.path.join('projects', self.name));
        with open(os.path.join('projects', self.name, ".history"), 'w') as historyFile:
            pass
        with open(os.path.join(".current_project"), 'w') as currentProjectFile:
            currentProjectFile.write(self.name)

@logged
class OpenProject(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, name):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        if not os.path.isdir(os.path.join('projects', self.name)):
            self.output.append('A project with name ' + self.name + ' does not exist')
            return
        with open(os.path.join(".current_project"), 'w') as currentProjectFile:
            currentProjectFile.write(self.name)

@logged
class PrintProjectHistory(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, commandProvider):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        name = None
        with open('.current_project') as currentProjectFile:
            name = currentProjectFile.readline()
        if not name:
            self.output.append('No project open')
            return
        with open(os.path.join('projects', name, ".history"), 'r') as historyFile:
            for i, line in enumerate(historyFile):
                line = line.rstrip()
                command = self.commandProvider.provide(line)
                if isinstance(command, ModelCommand):
                    self.output.append(str(i) + ". [Tap] " + line)
                elif isinstance(command, Euler2Command):
                    self.output.append(str(i) + ". [Reasoning] " + line)
                elif isinstance(command, MiscCommand):
                    self.output.append(str(i) + ". [Misc] " + line)
                    
@logged
class RemoveProjectHistory(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, commandProvider, index):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        name = None
        with open('.current_project') as currentProjectFile:
            name = currentProjectFile.readlines()[0]
        if not name:
            self.output.append('No project open')
            return
        lines = []
        with open(os.path.join('projects', name, ".history"), 'r') as historyFile:
            lines = historyFile.readlines()
            if self.index >= len(lines) or self.index < 0:
                self.output.append("invalid index")
            line = lines[self.index]
            newLines = list(lines)
            command = self.commandProvider.provide(line)
            if isinstance(command, ModelCommand):
                for i in range(self.index, len(lines)):
                    del newLines[self.index]
            else:
                del newLines[self.index]
        with open(os.path.join('projects', name, ".history"), 'w') as historyFile:
            historyFile.write(''.join(newLines))
    
@logged
class CloseProject(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        with open(os.path.join(".current_project"), 'w') as currentProjectFile:
            pass  
        
@logged 
class LoadTap(ModelCommand):
    @copy_args_to_public_fields
    def __init__(self, cleanTaxFile):
        ModelCommand.__init__(self)
    def run(self):
        ModelCommand.run(self)
        tap = e3_io.get_tap_from_cleantax(self.cleanTaxFile)
        e3_io.set_current_tap(tap)
        e3_io.store_tap(tap)
        self.output.append("Tap: " + e3_io.get_tap_id_and_name(tap))
    
@logged
class AddArticulation(ModelCommand):
    @copy_args_to_public_fields
    def __init__(self, tap, articulation):
        ModelCommand.__init__(self)
    def run(self):
        ModelCommand.run(self)
        self.tap.add_articulation(self.articulation)
        e3_io.set_current_tap(self.tap)
        e3_io.store_tap(self.tap)
        self.output.append("Tap: " + e3_io.get_tap_id_and_name(self.tap))

@logged
class RemoveArticulation(ModelCommand):
    @copy_args_to_public_fields
    def __init__(self, tap, articulationIndex):
        ModelCommand.__init__(self)
    def run(self):
        ModelCommand.run(self)
        try:
            self.tap.remove_articulation(self.articulationIndex)
        except Exception as e:
            #print e
            self.output.append("Could not find an articulation with the given index")
            return
        e3_io.set_current_tap(self.tap)
        e3_io.store_tap(self.tap)
        self.output.append("Tap: " + e3_io.get_tap_id_and_name(self.tap))
    
class UseTap(ModelCommand):
    @copy_args_to_public_fields
    def __init__(self, tap):
        ModelCommand.__init__(self)
    def run(self):
        ModelCommand.run(self)
        if self.tap:
            self.output.append("Tap: " + e3_io.get_tap_id_and_name(self.tap))
            
@logged
class SetCoverage(ModelCommand):
    @copy_args_to_public_fields
    def __init__(self, tap):
        ModelCommand.__init__(self)
    def run(self):
        ModelCommand.run(self)

@logged 
class SetRegions(ModelCommand):
    @copy_args_to_public_fields
    def __init__(self, tap):
        ModelCommand.__init__(self)
    def run(self):
        ModelCommand.run(self)

@logged 
class SetSiblingDisjointness(ModelCommand):
    @copy_args_to_public_fields
    def __init__(self, tap):
        ModelCommand.__init__(self)
    def run(self):
        ModelCommand.run(self)
        
class UnsetSiblingDisjointness(ModelCommand):
    @copy_args_to_public_fields
    def __init__(self, tap):
        ModelCommand.__init__(self)
    def run(self):
        ModelCommand.run(self)
    
@logged 
class GraphWorlds(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self)
    def run(self):
        Euler2Command.run(self)
        tapId = self.tap.get_id()
        cleantaxFile = os.path.join(tapId, ".cleantax")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        alignCommand = '{eulerExecutable} align {cleantax} -o {output}'.format(eulerExecutable = eulerExecutable, 
            cleantax = cleantaxFile, output = output);
        format = self.config['preferredImageFormat']
        self.run_euler("Align", alignCommand, output)
        inconsistent = False
        with open(os.path.join(output, "Align.stdout"), 'r') as aspOutputFile:
            for line in aspOutputFile:
                if line.startswith('Input is inconsistent'):
                    inconsistent = True
        
        if inconsistent:
            self.output.append("The tap is inconsistent")
            return
        showCommand = '{eulerExecutable} show -o {output} pw --{format}'.format(eulerExecutable = eulerExecutable, 
            output = output, format = format);
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
    def is_complete(self):
        return False
        
@logged 
class IsConsistent(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self)
    def run(self):
        Euler2Command.run(self)
        tapId = self.tap.get_id()
        cleantaxFile = os.path.join(tapId, ".cleantax")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        alignCommand = '{eulerExecutable} align {cleantax} -o {output} --consistency'.format(
            eulerExecutable = eulerExecutable, cleantax = cleantaxFile, output = output);
        self.run_euler("AlignConsistency", alignCommand, output)
        
        consistent = False
        with open(os.path.join(output, "AlignConsistency.stdout"), 'r') as aspOutputFile:
            for line in aspOutputFile:
                if line.startswith('Input is consistent'):
                    consistent = True
        if not consistent:
            self.output.append("no")
        else:
            self.output.append("yes")
            
@logged 
class MoreWorldsOrEqualThan(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap, thanVariable):
        Euler2Command.__init__(self)
    def run(self):
        Euler2Command.run(self)
        tapId = self.tap.get_id()
        cleantaxFile = os.path.join(tapId, ".cleantax")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        alignCommand = '{eulerExecutable} align {cleantax} -o {output} -n {thanVariable}'.format(
            eulerExecutable = eulerExecutable, cleantax = cleantaxFile, output = output, 
            thanVariable = self.thanVariable);
        self.run_euler("Align", alignCommand, output)
        
        aspOutputPath = os.path.join(tapId, "2-ASP-output", '.cleantax.pw')
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
class PrintFix(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self)
    def run(self):
        Euler2Command.run(self)
        tapId = self.tap.get_id()
        cleantaxFile = os.path.join(tapId, ".cleantax")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        repairMethod = self.config['preferredRepairMethod']
        repairCommand = '{eulerExecutable} align {cleantax} -o {output} --repair={repairMethod}'.format(eulerExecutable = eulerExecutable, 
            cleantax = cleantaxFile, output = output, repairMethod = repairMethod);
        self.run_euler("AlignRepair", repairCommand, output)
        self.output.append("Suggested repair options")
        with open(os.path.join(output, "AlignRepair.stdout"), 'r') as aspOutputFile:
            for line in aspOutputFile:
                if line.startswith('Repair option'):
                    self.output.append(line.rstrip())
                if line.startswith('Possible world'):
                    self.output = []
                    self.output.append("The tap is not inconsistent. There is nothing to fix.")
                    return
                           
@logged 
class GraphInconsistency(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self)
    def run(self):
        Euler2Command.run(self)
        tapId = self.tap.get_id()
        cleantaxFile = os.path.join(tapId, ".cleantax")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        format = self.config['preferredImageFormat']
        alignCommand = '{eulerExecutable} align {cleantax} -o {output}'.format(eulerExecutable = eulerExecutable, 
                            cleantax = cleantaxFile, output = output);                
        self.run_euler("Align", alignCommand, output)
        inconsistent = False
        with open(os.path.join(output, "Align.stdout"), 'r') as aspOutputFile:
            for line in aspOutputFile:
                if line.startswith('Input is inconsistent'):
                    inconsistent = True
        
        showCommand = '{eulerExecutable} show -o {output} inconLat --{format}'.format(eulerExecutable = eulerExecutable, 
                            output = output, format = format);
        if inconsistent:
            self.run_euler("ShowInconLat", showCommand, output)
            self.output.append("Take a look at the graph")
            self.executeOutput = []
            for filename in os.listdir(os.path.join(tapId, "6-Lattices")):
                if filename.endswith(".%s" % format):
                    self.executeOutput.append(self.config['imageViewer'].format(file = os.path.join(tapId, "6-Lattices", filename)))
        else:
            self.output.append("The tap is not inconsistent. I have nothing to show.")
            
@logged 
class PrintWorlds(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self)
    def run(self):
        Euler2Command.run(self)
        tapId = self.tap.get_id()
        cleantaxFile = os.path.join(tapId, ".cleantax")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        alignCommand = '{eulerExecutable} align {cleantax} -o {output}'.format(eulerExecutable = eulerExecutable, 
            cleantax = cleantaxFile, output = output);
        format = self.config['preferredImageFormat']
        self.run_euler("Align", alignCommand, output)
        
        inconsistent = False
        with open(os.path.join(output, "Align.stdout"), 'r') as aspOutputFile:
            for line in aspOutputFile:
                if line.startswith('Input is inconsistent'):
                    inconsistent = True
        
        if inconsistent:
            self.output.append("The tap is inconsistent")
            return
          
        aspOutputPath = os.path.join(tapId, "2-ASP-output", '.cleantax.pw')
        possibleWorlds = []
        with open(aspOutputPath, 'r') as aspOutputFile:
            currentWorld = ""
            for line in aspOutputFile:
                if len(line.strip()) == 0:
                    if len(currentWorld) > 0:
                        possibleWorlds.append(currentWorld.rstrip())
                        currentWorld = ""
                else:
                    if not len(line.strip()) == 0:
                        currentWorld += line
            if len(currentWorld) > 0:
                possibleWorlds.append(currentWorld.rstrip())
        
        maxPossibleWorldsToShow = self.config['maxPossibleWorldsToShow']
        if len(possibleWorlds) <= maxPossibleWorldsToShow:
            self.output.append("There are {count} possible worlds. I show them all to you.".format(
                count = len(possibleWorlds)))
        else:
            self.output.append("There are {count} possible worlds. I will only show {maxCount} of them to you.".format(
                count = len(possibleWorlds), maxCount = maxPossibleWorldsToShow))
        for world in possibleWorlds:
            self.output.append(world)
        
@logged 
class GraphTap(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self)
    def run(self):
        Euler2Command.run(self)
        tapId = self.tap.get_id()
        cleantaxFile = os.path.join(tapId, ".cleantax")
        eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        output = tapId
        format = self.config['preferredImageFormat']
        showCommand = '{eulerExecutable} show iv {cleantax} -o {output} --{format}'.format(eulerExecutable = eulerExecutable, 
            cleantax = cleantaxFile, output = output, format = format);
        self.run_euler("ShowIV", showCommand, output)
        
        self.output.append("Take a look at the graph")
        self.executeOutput = []
        for filename in os.listdir(os.path.join(tapId, "0-Input")):
            if filename.endswith(".%s" % format):
                self.executeOutput.append(self.config['imageViewer'].format(file = os.path.join(tapId, "0-Input", filename)))