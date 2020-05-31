import py_math
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import sys

def init_scene(scene, ioscene, camera, iocamera, progress_cb):
  progress = py_math.vec2i(0, len(ioscene.cameras) + len(ioscene.environments) +
              len(ioscene.materials) + len(ioscene.textures) +
              len(ioscene.shapes) + len(ioscene.subdivs) +
              len(ioscene.objects))
              
  camera_map = {}
  print("Test init_scene")
  for iocamera in ioscene.cameras:
    print("Test init_scene")
    if progress_cb:
      progress.x += 1
      progress_cb("convert camera", progress.x, progress.y)
    camera = ptr.add_camera(scene)
    ptr.set_frame(camera, iocamera.frame)
    ptr.set_lens(camera, iocamera.lens, iocamera.lens, iocamera.film)
    ptr.set_focus(camera, iocamera.aperture, iocamera.focus)
    camera_map[iocamera] = camera

  texture_map = {}
  for iotexture in ioscene.textures:
    if progress_cb:
      progress.x += 1
      progress_cb("convert texture", progress.x, progress.y)
    texture = ptr.add_texture(scene)
    if texture.colorf: # check if a list is empty by its type flexibility.
      ptr.set_texture(texture, iotexture.colorf)
    elif iotexture.colorb:
      ptr.set_texture(texture, iotexture.colorb)
    elif iotexture.scalarf:
      ptr.set_texture(texture, iotexture.scalarf)
    elif iotexture.scalarb:
      ptr.set_texture(texture, iotexture.scalarb)
    texture_map[iotexture] = texture
  
  material_map = {}
  for iomaterial in ioscene.materials:
    if progress_cb:
      progress.x += 1
      progress_cb("convert material", progress.x, progress.y)
    material = ptr.add_material
    # ptr.set_emission(material, iomaterial.emission)


def main(*argv):
  print(argv[0])

  # options
  params = ptr.trace_params()
  save_batch  = False
  camera_name = ""
  imfilename  = "out.hdr"
  filename    = "surface.json"
  # imfilename  = "out/lowres/01_surface_720_256.jpg"
  if len(argv) > 0 and len(argv[0]) > 1:
    if (argv[0][1]).startswith('tests/'):
      filename    = argv[0][1]
  print(filename)

  # parse command line
  cli = commonio.make_cli("yscntrace", "Offline path tracing")
  commonio.add_option(cli, "--camera", camera_name, "Camera name.", False)
  commonio.add_option(cli, "--resolution,-r", params.resolution, "Image resolution.", False)
  commonio.add_option(cli, "--samples,-s", params.samples, "Number of samples.", False)
  commonio.add_option(cli, "--shader,-t", params.shader, "Shader type.", ptr.shader_names, False)
  commonio.add_option(cli, "--bounces,-b", params.bounces, "Maximum number of bounces.", False)
  commonio.add_option(cli, "--clamp", params.clamp, "Final pixel clamping.", False)
  commonio.add_option(cli, "--save-batch", save_batch, "Save images progressively", False)
  commonio.add_option(cli, "--output-image,-o", imfilename, "Image filename", False)
  commonio.add_option(cli, "scene", filename, "Scene filename", True)

  # args = [["./apps/yscenetrace/yscentrace.py"], ["tests/01_surface/surface.json"], ["-t"], ["path"], ["-s"], ["256"], ["-r"], ["720"]]
  print(cli.options[9].value) # If I remove this everything blow up with segmentation-fault
  # commonio.parse_cli(cli, *argv)

  for option in cli.options:
    print("Name: ", option.name)
    print("Usage: ", option.usage)
    print("Type: ", option.type)
    print("Value: ", option.value)

  
  print("cli argument parse")

  filename = "tests/01_surface/surface.json"

  # scene loading
  # ioscene_guard = sio.model()
  ioscene = sio.model()
  print("ioscene created")
  ioerror = ""
  #if not sio.load_scene(filename, ioscene, ioerror, commonio.print_progress):
  #  commonio.print_fatal(ioerror)
  if not sio.load_scene(filename, ioscene, ioerror, commonio.print_progress):
    print("error loading_scene")
    commonio.print_fatal(ioerror)
  else:  
    print("python: scene loaded correctly")
  # get camera
  iocamera = sio.get_camera(ioscene, camera_name)

  # convert scene
  # scene_guard = ptr.scene()
  scene       = ptr.scene.get()
  camera      = None # ptr.camera.nullprt()
  init_scene(scene, ioscene, camera, iocamera, commonio.print_progress)


if __name__ == "__main__":
  main(sys.argv)
  
