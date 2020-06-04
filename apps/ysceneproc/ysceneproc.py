import py_math as mth
import py_shape as shp
import py_image as img
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import py_filesystem   as fs
import sys

def parse_cli(args):
  filename = "scene.json"
  output = "out.json"
  validate = False
  info = False
  copyright_yocto = ''
  
  i = 0
  for arg in args:
    if not arg.startswith('-') and i == 0 and arg.endswith('.json'):
      filename = arg
    elif arg.startswith('-c'):
      copyright_yocto = args[i+1]
    elif arg.startswith('-i'):
      info = bool(args[i+1])
      copyright_yocto = args[i+1]
    elif arg.startswith('--validate'):
      validate = bool(args[i+1])
    elif arg.startswith('-o'):
      output = args[i+1]
    i +=1

  return filename, output, validate, info, copyright_yocto


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
    commonio.print_fatal("cannot create directory " + dirname)
  


def main(*argv):
  # command line parameters
  validate = False
  info = False
  copyright_yocto = ""
  output = "out.json"
  filename = "scene.json"

  filename, output, validate, info, copyright_yocto = parse_cli(argv[0][1:])

  # parse command line
  cli = commonio.make_cli("yscnproc", "Process scene")
  commonio.add_option(cli, "--info,-i", info, "print scene info", False)
  commonio.add_option(cli, "--copyright,-c", copyright_yocto, "copyright string", False)
  commonio.add_option(cli, "--validate/--no-validate", validate, "Validate scene", False)
  commonio.add_option(cli, "--output,-o", output, "output scene", False)
  commonio.add_option(cli, "scene", filename, "input scene", True)

  # load scene
  ext = fs.path_extension(filename)
  basename = fs.path_stem(filename)
  scene = sio.model()
  ioerror = ""

  if (ext == ".ypreset"):
    commonio.print_progress("make preset", 0, 1)
    if not (make_preset(scene, basename, ioerror)):
      commonio.print_progress("make preset", 0, 1)
  else:
    if not (sio.load_scene(filename, scene, ioerror, commonio.print_progress)):
      commonio.print_fatal(ioerror)

  # copyright
  if (copyright_yocto != ""):
    scene.copyright = copyright_yocto
  
  # validate scene
  if (validate):
    for error in sio.scene_validation(scene):
      commonio.print_info("error" + error)

  # print infor
  if (info):
    commonio.print_info("scene stats ----------")
    for stat in sio.scene_stats(scene):
      commonio.print_info(stat)
  
  # tesselate if needed
  if (fs.path_extension(output) != ".json"):
    for iosubdiv in scene.subdivs:
      sio.tesselate_subdiv(scene, iosubdiv)
  

  # make a directory if needed
  make_dir(fs.path_parent_path(output))
  if scene.shapes:
    make_dir(fs.path_parent_path(output) + "shapes")
  if scene.subdivs:
    make_dir(fs.path_parent_path(output) + "subdivs")
  if scene.textures:
    make_dir(fs.path_parent_path(output) + "texture")
  if scene.instances:
    make_dir(fs.path_parent_path(output) + "instances")


  # save scene
  if not sio.save_scene(output, scene, ioerror, commonio.print_progress):
    commonio.print_fatal(ioerror)

if __name__ == "__main__":
  main(sys.argv)
  
