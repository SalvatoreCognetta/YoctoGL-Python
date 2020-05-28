import py_pathtrace

if __name__ == "__main__":
  # options
  params = py_pathtrace.trace_params()
  save_batch  = False
  camera_name = ""
  imfilename  = "out.hdr"
  filename    = "scene.json"

  # parse command line