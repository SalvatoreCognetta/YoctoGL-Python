import py_pathtrace
import py_commonio


if __name__ == "__main__":
  # options
  params = py_pathtrace.trace_params()
  save_batch  = False
  camera_name = ""
  imfilename  = "out.hdr"
  filename    = "scene.json"

  # parse command line
  cli = py_commonio.make_cli("yscenetrace", "Offline path tracing")
  py_commonio.add_option(cli, "--camera", camera_name, "Camera name.")
  py_commonio.add_option(cli, "--resolution,-r", params.resolution, "Image resolution.")
  py_commonio.add_option(cli, "--samples,-s", params.samples, "Number of samples.")
  py_commonio.add_option(cli, "--shader,-t", params.shader, "Shader type.", py_pathtrace.shader_names)
  py_commonio.add_option(cli, "--bounces,-b", params.bounces, "Maximum number of bounces.")
  py_commonio.add_option(cli, "--clamp", params.clamp, "Final pixel clamping.")
  py_commonio.add_option(cli, "--save-batch", save_batch, "Save images progressively")
  py_commonio.add_option(cli, "--output-image,-o", imfilename, "Image filename")
  py_commonio.add_option(cli, "scene", filename, "Scene filename", True)

