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
    @copy_args_to_public_fields
    def __init__(self, tap):
        Command.__init__(self)
        self.alignCommand = '{eulerExecutable} align {cleantaxFile} -o {outputDir}'
        self.alignConsistencyCommand = '{eulerExecutable} align {cleantaxFile} -o {outputDir} --consistency'
        self.alignMaxNCommand = '{eulerExecutable} align {cleantaxFile} -o {outputDir} -n {maxN}'
        self.alignRepairCommand = '{eulerExecutable} align {cleantaxFile} -o {outputDir} --repair={repairMethod}'
        self.showIVCommand = '{eulerExecutable} show iv {cleantaxFile} -o {outputDir} --{imageFormat}';
        self.showPWCommand = '{eulerExecutable} show -o {outputDir} pw --{imageFormat}'
        self.showInconLatCommand = '{eulerExecutable} show -o {outputDir} inconLat --{imageFormat}'
        self.eulerXPath = self.config['eulerXPath']
        self.imageViewer = self.config['imageViewer']
        self.maxPossibleWorldsToShow = self.config['maxPossibleWorldsToShow']
        self.preferredImageFormat = self.config['preferredImageFormat']
        self.preferredRepairMethod = self.config['preferredRepairMethod']
        self.defaultIsCoverage = self.config['defaultIsCoverage']
        self.defaultIsSiblingDisjointness = self.config['defaultIsSiblingDisjointness']
        self.defaultRegions = self.config['defaultRegions']
        self.eulerExecutable = os.path.join(self.config['eulerXPath'], "src-el", "euler2")
        self.tapId = self.tap.get_id()
        self.cleantaxFile = e3_io.get_cleantax_file(self.tap)
        self.outputDir = e3_io.get_tap_dir(self.tapId)
        self.name = self.__class__.__name__
        self.e2InputDir = e3_io.get_0_input_dir(self.tap)
        self.e2AspOutputDir = e3_io.get_2_asp_output_dir(self.tap)
        self.e2PWsDir = e3_io.get_4_pws_dir(self.tap)
        self.e2LatticesDir = e3_io.get_6_lattices_dir(self.tap)
        self.isConsistent = True
        if not hasattr(self, 'maxN'):
            self.maxN = None
    def run(self):
        Command.run(self)
    def run_euler(self, command):
        # add parameters to the commanad that are relevant to avoid re-runs
        # by at the same time keeping the file name minimal
        command = command.format(eulerExecutable = '{eulerExecutable}', 
                cleantaxFile = '{cleantaxFile}', outputDir = '{outputDir}', imageFormat = '{imageFormat}', 
                maxN = self.maxN)
        stdoutFile = os.path.join(self.outputDir, '%s.stdout' % command)
        stderrFile = os.path.join(self.outputDir, '%s.stderr' % command)
        returnCodeFile = os.path.join(self.outputDir, '%s.returncode' % command)
        if os.path.isfile(stdoutFile):
            return
        # add remaining parameters
        command = command.format(eulerExecutable = self.eulerExecutable, 
                cleantaxFile = self.cleantaxFile, outputDir = self.outputDir, imageFormat = self.preferredImageFormat, 
                maxN = self.maxN);
        with open(stdoutFile, 'w+') as out:
            with open(stderrFile, 'w+') as err:
                with open(returnCodeFile, 'w+') as rc:
                    print command
                    p = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
                    stdout, stderr = p.communicate()
                    print stdout
                    print stderr
                    if "Input is inconsistent" in stdout:
                        self.isConsistent = False
                    out.write(stdout)
                    err.write(stderr)
                    rc.write('%s' % p.returncode)
    def is_consistent(self):
        return self.isConsistent
    def get_possible_worlds(self):
        possibleWorlds = []
        with open(os.path.join(self.e2AspOutputDir, '.cleantax.pw'), 'r') as f:
            currentWorld = ""
            for line in f:
                if len(line.strip()) == 0:
                    if len(currentWorld) > 0:
                        possibleWorlds.append(currentWorld.rstrip())
                        currentWorld = ""
                else:
                    if not len(line.strip()) == 0:
                        currentWorld += line
            if len(currentWorld) > 0:
                possibleWorlds.append(currentWorld.rstrip())
        return possibleWorlds
    
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
        if e3_io.exists_project(self.name):
            self.output.append('A project with name ' + self.name + ' already exists')
            return
        e3_io.create_project(self.name)
        e3_io.set_history(self.name, "")
        e3_io.set_current_project(self.name)

@logged
class OpenProject(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, name):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        if not e3_io.exists_project(self.name):
            self.output.append('A project with name ' + self.name + ' does not exist')
            return
        e3_io.set_current_project(self.name)

@logged
class PrintProjectHistory(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, commandProvider):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        name = e3_io.get_current_project()
        if not name:
            self.output.append('No project open')
            return
        if not e3_io.exists_project(name):
            self.output.append('Project has been removed')
            return
        with open(e3_io.get_history_file(name), 'r') as historyFile:
            for i, line in enumerate(historyFile):
                line = line.rstrip()
                uuidPart = line.split(' ', 1)[0]
                commandPart = line.split(' ', 1)[1]
                command = self.commandProvider.provide(commandPart)
                if isinstance(command, ModelCommand):
                    self.output.append(str(i) + ". [Tap] " + commandPart + " (" + uuidPart + ")")
                elif isinstance(command, Euler2Command):
                    self.output.append(str(i) + ". [Reasoning] " + commandPart + " (" + uuidPart + ")")
                elif isinstance(command, MiscCommand):
                    self.output.append(str(i) + ". [Misc] " + commandPart + " (" + uuidPart + ")")
                    
@logged
class RemoveProjectHistory(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, commandProvider, index):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        name = e3_io.get_current_project()
        if not name:
            self.output.append('No project open')
            return
        if not e3_io.exists_project(name):
            self.output.append('Project has been removed')
            return
        lines = []
        with open(e3_io.get_project_history(name), 'r') as historyFile:
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
        e3_io.set_history(name, ''.join(newLines))
    
@logged
class CloseProject(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        e3_io.set_current_project(None) 
    
@logged
class ClearProjects(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        e3_io.clear_projects()
        e3_io.set_current_project(None) 
    
@logged
class RemoveProject(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self, name):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        if e3_io.get_current_project() == self.name:
            e3_io.set_current_project(None)
        e3_io.remove_project(self.name)
        
@logged
class PrintProjects(MiscCommand):
    @copy_args_to_public_fields
    def __init__(self):
        MiscCommand.__init__(self)
    def run(self):
        MiscCommand.run(self)
        projects = e3_io.get_projects()
        if projects:
            print '\n'.join(projects)
        
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
        e3_io.set_current_tap(self.tap)
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
        Euler2Command.__init__(self, tap)
    def run(self):
        Euler2Command.run(self)
        self.run_euler(self.alignCommand)
        if not self.is_consistent():
            self.output.append("The tap is inconsistent")
            return
        
        self.run_euler(self.showPWCommand)
        possibleWorldsCount = len(self.get_possible_worlds())
        if possibleWorldsCount <= self.maxPossibleWorldsToShow:
            self.output.append("There are {count} possible worlds. I show them all to you.".format(
                count = possibleWorldsCount))
        else:
            self.output.append("There are {count} possible worlds. I will only show {maxCount} of them to you.".format(
                count = possibleWorldsCount, maxCount = self.maxPossibleWorldsToShow))
        
        self.executeOutput = []
        openCount = 0
        for filename in os.listdir(self.e2PWsDir):
            if filename.endswith(".%s" % self.preferredImageFormat) and openCount < self.maxPossibleWorldsToShow:
                openCount += 1
                self.executeOutput.append(self.imageViewer.format(file = os.path.join(self.e2PWsDir, filename)))
                
@logged 
class IsConsistent(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self, tap)
    def run(self):
        Euler2Command.run(self)
        self.run_euler(self.alignConsistencyCommand)
        
        if self.is_consistent():
            self.output.append("yes")
        else:
            self.output.append("no")
    
@logged 
class MoreWorldsOrEqualThan(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap, maxN):
        Euler2Command.__init__(self, tap)
    def run(self):
        Euler2Command.run(self)
        self.run_euler(self.alignMaxNCommand)
               
        possibleWorldsCount = len(self.get_possible_worlds())
        if possibleWorldsCount < self.maxN:
            self.output.append("There are < {maxN} possible worlds. There are {count}.".format(
                maxN = self.maxN, count = possibleWorldsCount))
        else:
            self.output.append("There are >= {maxN} possible worlds.".format(
                maxN = self.maxN))
            
@logged 
class PrintFix(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self, tap)
    def run(self):
        Euler2Command.run(self)
        self.run_euler(self.alignRepairCommand)
        
        if self.is_consistent():
            self.output.append("The tap is not inconsistent. I have nothing to show.")
            return
        
        self.output.append("Suggested repair options")
        
        with open(os.path.join(self.outputDir, self.name + "-AlignRepair.stdout"), 'r') as stdoutFile:
            for line in stdoutFile:
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
        Euler2Command.__init__(self, tap)
    def run(self):
        Euler2Command.run(self)             
        self.run_euler(self.alignCommand)
        if self.is_consistent():
            self.output.append("The tap is not inconsistent. I have nothing to show.")
            return
        
        self.run_euler(self.showInconLatCommand)
        self.output.append("Take a look at the graph")
        self.executeOutput = []
        for filename in os.listdir(self.e2LatticesDir):
            if filename.endswith(".%s" % self.preferredImageFormat):
                self.executeOutput.append(self.imageViewer.format(file = os.path.join(self.e2LatticesDir, filename))) 
            
@logged 
class PrintWorlds(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self, tap)
    def run(self):
        Euler2Command.run(self)
        self.run_euler(self.alignCommand)        
        if not self.is_consistent():
            self.output.append("The tap is inconsistent")
            return
        
        possibleWorlds = self.get_possible_worlds()
        if len(possibleWorlds) <= self.maxPossibleWorldsToShow:
            self.output.append("There are {count} possible worlds. I show them all to you.".format(
                count = len(possibleWorlds)))
        else:
            self.output.append("There are {count} possible worlds. I will only show {maxCount} of them to you.".format(
                count = len(possibleWorlds), maxCount = self.maxPossibleWorldsToShow))
        for world in possibleWorlds:
            self.output.append(world)
      
@logged 
class GraphTap(Euler2Command):
    @copy_args_to_public_fields
    def __init__(self, tap):
        Euler2Command.__init__(self, tap)
    def run(self):
        Euler2Command.run(self)
        self.run_euler(self.showIVCommand)
        self.output.append("Take a look at the graph")
        self.executeOutput = []
        for filename in os.listdir(self.e2InputDir):
            if filename.endswith(".%s" % self.preferredImageFormat):
                self.executeOutput.append(self.imageViewer.format(file = os.path.join(self.e2InputDir, filename)))