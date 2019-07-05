import sys, string, os, yaml
import Server.configedit as configedit

def import_suppliers():
    # Read config file
    with open("config.yml", 'r') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    for s in config['suppliers']:
        if config['suppliers'][s]['enabled'] == True:
                impstring = "import Suppliers."+s.upper()+"."+s
                try:
                    exec(impstring)
                    print("Succesfuly imported", s)
                except:
                    print("Could not import", s)
