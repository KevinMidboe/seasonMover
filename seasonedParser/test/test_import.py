import sys, os

def test_import_env_variables():
  import env_variables as env 
  assert env.logfile == 'conf/output.log'
