from src import cleaner, parser, loader, shell, config

def init():
	raws = loader.load(config.library)
	clears = cleaner.clean(raws, config.substitutions)
	general = parser.parse(clears, config.adjustments, verbose=True)
	
	return general


general = init()
sh = shell.Shell(general, config.adjustments)