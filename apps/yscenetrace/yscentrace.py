import py_math
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import sys

def init_scene(scene: ptr.scene, ioscene: sio.model, camera: ptr.camera, iocamera: sio.camera, progress_cb):
  progress = py_math.vec2i(0, len(ioscene.cameras) + len(ioscene.environments) +
              len(ioscene.materials) + len(ioscene.textures) +
              len(ioscene.shapes) + len(ioscene.subdivs) +
              len(ioscene.objects))
              
  camera_map = {}
  print("Test init_scene")
  for iocamera in ioscene.cameras:
    print("Test iocamera")
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
    if texture.colorf: # check if a list is empty by its type flexibility. https://therenegadecoder.com/code/how-to-check-if-a-list-is-empty-in-python/#check-if-a-list-is-empty-by-its-type-flexibility
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
    material = ptr.add_material(scene)
    ptr.set_emission(material, iomaterial.emission, texture_map[iomaterial.emission_tex])
    ptr.set_color(material, iomaterial.color, texture_map[iomaterial.color_tex])
    ptr.set_specular(material, iomaterial.specular, texture_map[iomaterial.specular])
    ptr.set_ior(material, iomaterial.ior)
    ptr.set_metallic(material, iomaterial.metallic, texture_map[iomaterial.metallic_tex])
    ptr.set_transmission(material, iomaterial.transmission, iomaterial.thin, iomaterial.trdepth, texture_map[iomaterial.transmission_tex])
    ptr.set_roughness(material, iomaterial.roughness, texture_map[iomaterial.roughness_tex])
    ptr.set_opacity(material, iomaterial.opacity, texture_map[iomaterial.opacity_tex])
    ptr.set_thin(material, iomaterial.thin)
    ptr.set_scattering(material, iomaterial.scattering, iomaterial.scanisotropy, texture_map[iomaterial.scattering_tex])
    ptr.set_normalmap(material, texture_map[iomaterial.normal_tex])
    material_map[iomaterial] = material

  subdiv_map = {}
  for iosubdiv in ioscene.subdivs:
    if progress_cb:
      progress.x += 1
      progress_cb("convert subdiv", progress.x, progress.y)
    subdiv = ptr.add_shape(scene)
    ptr.set_subdiv_quadspos(subdiv, iosubdiv.quadspos)
    ptr.set_subdiv_quadstexcoord(subdiv, iosubdiv.quadstexcoords)
    ptr.set_subdiv_positions(subdiv, iosubdiv.positions)
    ptr.set_subdiv_texcoords(subdiv, iosubdiv.texcoords)
    subdiv_map[iosubdiv] = subdiv

  shape_map = {}
  for ioshape in ioscene.shapes:
    if progress_cb:
      progress.x += 1
      progress_cb("convert shape", progress.x, progress.y)
    shape = ptr.add_shape(scene)
    ptr.set_points(shape, ioshape.points)
    ptr.set_lines(shape, ioshape.lines)
    ptr.set_triangles(shape, ioshape.triangles)
    # if ioshape.quads:
    #   ptr.set_triangles(shape, )


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

  # scene loading
  # ioscene_guard = sio.model()
  ioscene = sio.model()
  print("ioscene created")
  ioerror = ""
  if not sio.load_scene(filename, ioscene, ioerror, commonio.print_progress):
    print("error loading_scene")
    commonio.print_fatal(ioerror)
  else:  
    print("python: scene loaded correctly")
  # get camera
  iocamera = sio.get_camera(ioscene, camera_name)

  # convert scene
  # scene_guard = ptr.scene()
  scene       = ptr.scene()
  camera      = None # ptr.camera.nullprt()
  init_scene(scene, ioscene, camera, iocamera, commonio.print_progress)


if __name__ == "__main__":
  main(sys.argv)
  
