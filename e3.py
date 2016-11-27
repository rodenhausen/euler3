'''
@author: Thomas
'''
import logging, sys
from e3_run import OneShot
from e3_run import Interactive
from e3_parse import CommandProvider
from e3_io import get_config

def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")
    config = get_config()
    sys.path.append(config['eulerXPath'])
    
    #pinject_config = Config()
    run = None
    if len(sys.argv) > 1:
        run = OneShot(CommandProvider())
    else:
        run = Interactive(CommandProvider())
    run.run()
    #obj_graph = pinject.new_object_graph(binding_specs=[pinject_config])
    #run = obj_graph.provide(Run)
    #run.run()
    
if __name__ == '__main__':
    main()