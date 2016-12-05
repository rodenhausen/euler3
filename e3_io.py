'''
Created on Nov 22, 2016

@author: Thomas
'''
import yaml
import os.path
import e3_model
import e3_command

def get_config():
    if not os.path.isfile('.config'):
        raise Exception(".config file not found")
    with open('.config', 'r') as f:
        return yaml.safe_load(f)

def set_name(name, tap):
    if not os.path.isfile('.names'):
        with open('.names', "w+") as namesFile:
            pass
    names = { }
    with open('.names', 'r+') as namesFile:
            doc = yaml.load(namesFile)
            if doc:
                for key, value in doc.iteritems():
                    names[key] = value
            names[name] = tap.get_id()
            yaml.dump(names, namesFile, default_flow_style=False)

def get_names():
    names = []
    if os.path.isfile('.names'):
        with open('.names', 'r') as namesFile:
            doc = yaml.load(namesFile)
            if doc:
                for key, value in doc.items():
                    names.append(key + " = " + value)
    return names       

def clear_names():
    with open('.names', 'w'): pass

def get_tap_id_and_name(tap):
    name = get_tap_name(tap.get_id())
    if name:
        return name + " = " + tap.get_id()
    else:
        return tap.get_id()

def get_current_tap():
    if not os.path.isfile('.current_tap'):
        return None
    with open('.current_tap', 'r') as currentTapFile:
        return get_tap(os.path.join(currentTapFile.readline()))
        
def set_current_tap(tap):
    with open('.current_tap', 'w') as currentTapfile:
        currentTapfile.write(tap.get_id())

def store_tap(tap):
    tapFile = os.path.join(tap.get_id(), ".tap")
    if not os.path.isdir(tap.get_id()):
        os.mkdir(tap.get_id())
    with open(tapFile, 'w') as f:
        f.write(str(tap.isCoverage) + '\n')
        f.write(str(tap.isSiblingDisjointness) + '\n')
        f.write(tap.regions + '\n')
        f.write('\n')
        for line in tap.taxonomyA:
            f.write(line + '\n')
        f.write('\n')
        for line in tap.taxonomyB:
            f.write(line + '\n')
        f.write('\n')
        for line in tap.articulations:
            f.write(line + '\n')
    store_tap_to_cleantax(tap)

def store_tap_to_cleantax(tap):
    tapFile = os.path.join(tap.get_id(), ".cleantax")
    if not os.path.isdir(tap.get_id()):
        os.mkdir(tap.get_id())
    with open(tapFile, 'w') as f:        
        for line in tap.taxonomyA:
            f.write(line + '\n')
        f.write('\n')
        for line in tap.taxonomyB:
            f.write(line + '\n')
        f.write('\n')
        for line in tap.articulations:
            f.write(line + '\n')
          
def get_tap(tapId):
    tapFile = os.path.join(tapId, ".tap")
    config = get_config()
    if not os.path.isfile(tapFile):
        return None
    with open(tapFile, 'r') as f:
        isCoverage = config['defaultIsCoverage']
        isSiblingDisjointness = config['defaultIsSiblingDisjointness']
        regions = config['defaultRegions']
        taxonomyA = []
        taxonomyB = []
        articulations = []
        taxonomyAComplete = False
        taxonomyBComplete = False
        for i, line in enumerate(f):
            if i == 0:
                isCoverage = line.rstrip() == 'True'
            elif i == 1:
                isSiblingDisjointness = line.rstrip() == 'True'
            elif i == 2:
                regions = line.rstrip()
            elif i >= 4:
                if len(line.strip()) == 0:
                    if not taxonomyAComplete:
                        taxonomyAComplete = True
                    elif not taxonomyBComplete:
                        taxonomyBComplete = True 
                else:
                    line = line.rstrip()
                    if not taxonomyAComplete:
                        taxonomyA.append(line)
                    elif not taxonomyBComplete:
                        taxonomyB.append(line)
                    else: articulations.append(line)
    return e3_model.Tap(isCoverage, isSiblingDisjointness, regions, taxonomyA, taxonomyB, articulations)
      
def get_tap_from_cleantax(cleanTaxFile):
    config = get_config()
    if not os.path.isfile(cleanTaxFile):
        return None
    with open(cleanTaxFile, 'r') as f:
        lines = f.readlines()
        
        taxonomyA = []
        taxonomyB = []
        articulations = []
        taxonomyAComplete = False
        taxonomyBComplete = False
        for line in lines:
            if len(line.strip()) == 0:
                if not taxonomyAComplete:
                    taxonomyAComplete = True
                elif not taxonomyBComplete:
                    taxonomyBComplete = True 
            else:
                line = line.rstrip()
                if not taxonomyAComplete:
                    taxonomyA.append(line)
                elif not taxonomyBComplete:
                    taxonomyB.append(line)
                else: articulations.append(line)
    return e3_model.Tap(config['defaultIsCoverage'], config['defaultIsSiblingDisjointness'], config['defaultRegions'], taxonomyA, taxonomyB, articulations)

def get_tap_from_name(name):
    id = get_tap_id(name)
    if id:
        return get_tap(id)
    return None

def get_tap_from_id_or_name(name_or_id):
    tap = get_tap_from_name(name_or_id)
    if not tap:
        tap = get_tap(name_or_id)
    if not tap:
        return None
    else:
        return tap

def get_tap_id(name):
    if os.path.isfile('.names'):
        with open('.names', 'r') as namesFile:
            doc = yaml.load(namesFile)
            if doc:
                if doc[name]:
                    return doc[name]
    return None

def get_tap_name(id):
    if os.path.isfile('.names'):
        with open('.names', 'r') as namesFile:
            doc = yaml.load(namesFile)
            if doc:
                for key, value in doc.items():
                    if value == id:
                        return key
    return None

def append_project_history(input, command):
    if not isinstance(command, e3_command.MiscCommand):
        currentProject = None
        with open('.current_project') as currentProjectFile:
            currentProject = currentProjectFile.readline()
        if currentProject:
            if os.path.isfile(os.path.join('projects', currentProject, '.history')):
                with open(os.path.join('projects', currentProject, '.history'), 'a') as historyFile:
                    historyFile.write(input + '\n')
                    
def get_cleantax_file(tap):
    return os.path.join(tap.get_id(), ".cleantax")

def get_0_input_dir(tap):
    return os.path.join(tap.get_id(), "0-Input")

def get_2_asp_output_dir(tap):
    return os.path.join(tap.get_id(), "2-ASP-output")

def get_4_pws_dir(tap):
    return os.path.join(tap.get_id(), "4-PWs")

def get_6_lattices_dir(tap):
    return os.path.join(tap.get_id(), "6-Lattices")