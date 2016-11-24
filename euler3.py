'''
@author: Thomas
'''
import logging, sys
from run import OneShot
from run import Interactive
from parse import CommandProvider
from io import _Getch

def main():
    getch = _Getch()
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")
    #pinject_config = Config()
    #run = None
    #if len(sys.argv) > 1:
    #    run = OneShot(CommandProvider())
    #else:
    #    run = Interactive(CommandProvider())
    #run.run()
    #obj_graph = pinject.new_object_graph(binding_specs=[pinject_config])
    #run = obj_graph.provide(Run)
    #run.run()
    
if __name__ == '__main__':
    main()