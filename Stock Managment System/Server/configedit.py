import yaml, sys, os

with open("config.yml", 'r') as ymlfile:
	cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

def update(attribute, value):
	with open("config.yml", 'w+') as changefile:
		editline = 'cfg' + attribute +" = " + str(value)
		try:
			exec(editline)
		except:
			print("Error: cannot update config\nConfig.yml remains unaffected")
		yaml.dump(cfg, changefile)
