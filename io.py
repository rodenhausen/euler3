'''
Created on Nov 22, 2016

@author: Thomas
'''
import yaml
import os.path
from model import Tap

def get_config():
    with open('.config', 'r') as f:
        return yaml.safe_load(f)

def set_name(name, tap):
    names = { }
    with open('.names', 'r+') as namesFile:
            doc = yaml.load(namesFile)
            if doc:
                for key, value in doc.iteritems():
                    names[key] = value
            names[name] = tap.get_id()
            yaml.dump(names, namesFile, default_flow_style=False)

def get_current_tap():
    with open('.current_tap', 'r') as currentTapFile:
        return get_tap(os.path.join(currentTapFile.readline(), '.tap'))
        
def set_current_tap(tap):
    with open('.current_tap', 'w') as currentTapfile:
        currentTapfile.write(tap.get_id())

def store_tap(tap):
    tapFile = os.path.join(tap.get_id(), ".tap")
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

def get_tap(tapFile):
    if not os.path.isfile(tapFile):
        return None
    with open(tapFile, 'r') as f:
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
    return Tap(taxonomyA, taxonomyB, articulations)

def get_tap_by_id(id):
    tapFile = os.path.join(id, ".tap")
    if os.path.isdir(id):
        if os.path.isfile(tapFile):
            return get_tap(tapFile)
    return None

def get_tap_by_name(name):
    with open('.names', 'r') as namesFile:
        doc = yaml.load(namesFile)
        return get_tap_by_id(doc[name])

def get_tap_by_id_or_name(id):
    with open('.names', 'r') as namesFile:
        doc = yaml.load(namesFile)
        if doc:
            if doc[id]:
                return get_tap_by_name(doc[id])
    return get_tap_by_id(id)
