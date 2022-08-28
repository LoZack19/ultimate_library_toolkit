import yaml

def init_config(filename: str) -> dict:
	config = {}
	
	with open(filename, 'r') as infile:
		config = yaml.load(infile, Loader=yaml.FullLoader)
	
	return config

CONFIG_FILE = "/home/giovanni/Scaricati/ULT/config.yaml"
CONFIG = init_config(CONFIG_FILE)

library = CONFIG["library"]
substitutions = CONFIG["substitutions"]
adjustments = CONFIG["adjustments"]
