import sys, string, os, yaml
import Server.configedit as configedit

def import_suppliers(s):
	# Read config file
	with open("config.yml", 'r') as cfg:
		config = yaml.load(cfg, Loader=yaml.FullLoader)

	impstring = "from Suppliers."+s.upper()+"."+s+" import "+s
	return impstring
