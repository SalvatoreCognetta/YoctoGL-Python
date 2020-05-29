# import py_math
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import sys

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
  print(cli.options[1].value)
  commonio.parse_cli(cli, *argv)
  # print(cli.options[1].value)

  # scene loading
  # ioscene_guard = sio.model()
  print("test")
  ioscene = sio.model.get()
  print("test")
  ioerror = ""
  if not sio.load_scene(filename, ioscene, ioerror, commonio.print_progress):
    print("Test")
    commonio.print_fatal(ioerror)

  # get camera
  iocamera = commonio.get_camera

  # convert scene
  scene_guard = ptr.scene()
  scene       = ptr.scene.get()
  camera      = ptr.camera.nullprt()
  # init_scene(scene, ioscene, camera, iocamera, cli::print_progress);


if __name__ == "__main__":
  main(sys.argv)
  
