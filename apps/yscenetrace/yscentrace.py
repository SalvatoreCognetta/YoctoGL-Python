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
  for iocamera in ioscene.camera:
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
    

def main(*argv):
  print(*argv)

  # options
  params = ptr.trace_params()
  save_batch  = False
  camera_name = ""
  imfilename  = "out.hdr"
  filename    = "scene.json"

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
  print(cli.options[1].value) # If I remove this everything blow up with segmentation-fault
  commonio.parse_cli(cli, *argv)
  print("cli argument parse")

  filename = "tests/01_surface/surface.json"

  # scene loading
  # ioscene_guard = sio.model()
  ioscene = sio.model.get()
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
  scene_guard = ptr.scene()
  scene       = ptr.scene.get()
  camera      = ptr.camera.nullprt()
  # init_scene(scene, ioscene, camera, iocamera, cli::print_progress);


if __name__ == "__main__":
  main(sys.argv)
  
