'''
@author: Thomas
'''
import logging, sys
import e3_run
import e3_parse
import e3_io

def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")
    config = e3_io.get_config()
    sys.path.append(config['eulerXPath'])
    
    #pinject_config = Config()
    run = None
    if len(sys.argv) > 1:
        run = e3_run.OneShot(e3_parse.CommandProvider())
    else:
        run = e3_run.Interactive(e3_parse.CommandProvider())
    run.run()
    #obj_graph = pinject.new_object_graph(binding_specs=[pinject_config])
    #run = obj_graph.provide(Run)
    #run.run()
    
if __name__ == '__main__':
    main()