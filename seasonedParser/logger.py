import logging
import env_variables as env

logging.basicConfig(filename=env.logfile, level=logging.INFO)
logger = logging.getLogger('seasonedParser')
fh = logging.FileHandler(env.logfile)
fh.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.WARNING)

fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh_formatter = logging.Formatter('%(levelname)s: %(message)s')
fh.setFormatter(fh_formatter)
sh.setFormatter(sh_formatter)

logger.addHandler(fh)
logger.addHandler(sh)