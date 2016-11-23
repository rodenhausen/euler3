'''
@author: Thomas
'''
import pinject
import yaml

'''
pinject problems/open questions
(1) How to create a config where bindings exist that are not needed for every "Run"?
e.g. loadTapInput when a showPossibleWorlds command is supposed to be run
In Guice they are then just ignored by pinject will throw an exception saying it cant find a target to inject into.
(2) AttributeError: 'Config' object has no attribute 'loadTapInput', even though it is set from outside?
'''
class Config(pinject.BindingSpec):
    def __init__(self):
        with open('.config', 'r') as f:
            config = yaml.safe_load(f)
        self.reasoningReasoner = config['reasoning']['reasoner']
        self.outputFormat = config['output']['format']
        self.publishGitRepository = config['publish']['git_repository']
    
    def configure(self, bind):
        bind('command', to_class=self.command)
        bind('reasoningReasoner', to_instance=self.reasoningReasoner)
        bind('loadTapInput', to_instance=self.loadTapInput)#'abstract.txt')
        #bind('outputFormat', to_instance=self.outputFormat)
        #bind('publishGitRepository', to_instance=self.publishGitRepository)
        