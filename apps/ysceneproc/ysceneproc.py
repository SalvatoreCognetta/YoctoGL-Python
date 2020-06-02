import py_commonio as cli
import py_sceneio as sio
import py_math 
import py_pathtrace as ptr
import py_filesystem as fs
import sys

def make_preset(scene, type, error):
  if(type == "cornellbox"):
    sio.make_cornellbox(scene)
    return True
  else:
    error = "uknown preset"
    return False
  return True

def make_dir(dirname):
  if(fs.path_exists(dirname)): return
  try:
    fs.path_create_directories(dirname)
  except:
    cli.print_fatal("cannot create directory " + dirname)

  


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
  ext = fs.path_extension(filename)
  basename = fs.path_stem(filename)
  scene = ptr.scene()
  ioerror = ""

  if (ext == ".ypreset"):
    cli.print_progress("make preset", 0, 1)
    if not (make_preset(scene, basename, ioerror)):
      cli.print_progress("make preset", 0, 1)
  else:
    if not (sio.load_scene(filename, scene , ioerror)):
      cli.print_fatal(ioerror)


  # if (copyrigt != ""):
  #   for error in 

