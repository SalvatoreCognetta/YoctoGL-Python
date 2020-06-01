import py_commonio as cli
import py_sceneio as sio
import py_math 
import py_pathtrace as ptr
import sys


def main(*argv):
  #command line parameters
  validate = False
  info = False
  copyrigt = ""
  output = "out.json"
  filename = "scene.json"

  #parse command line
  cli = cli.make_cli("yscnproc", "Process scene")
  cli.add_option(cli, "--info,-i", info, "print scene info")
  cli.add_option(cli, "--copyright,-c", copyrigt, "copyright string")
  cli.add_option(cli, "--validate/--no-validate", validate, "Validate scene")
  cli.add_option(cli, "--output,-o", output, "output scene")
  cli.add_option(cli, "scene", filename, "input scene", True)

  #load scene
  