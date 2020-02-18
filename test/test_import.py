import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../src"))

def test_import_env_variables():
  import env_variables as env 
  assert env.logfile == 'conf/output.log'
