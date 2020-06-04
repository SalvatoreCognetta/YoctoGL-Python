import py_math
import py_shape as shp
import py_image as img
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import py_filesystem   as fs
import sys

def init_scene(scene: ptr.scene, ioscene: sio.model, camera: ptr.camera, iocamera: sio.camera, progress_cb):
  progress = py_math.vec2i(0, len(ioscene.cameras) + len(ioscene.environments) +
              len(ioscene.materials) + len(ioscene.textures) +
              len(ioscene.shapes) + len(ioscene.subdivs) +
              len(ioscene.objects))
              
  camera_map = {}
  camera_map[None] = None
  for iocamera in ioscene.cameras:
    if progress_cb:
      progress.x += 1
      progress_cb("convert camera", progress.x, progress.y)
    camera = ptr.add_camera(scene)
    ptr.set_frame(camera, iocamera.frame)
    ptr.set_lens(camera, iocamera.lens, iocamera.lens, iocamera.film)
    ptr.set_focus(camera, iocamera.aperture, iocamera.focus)
    camera_map[iocamera] = camera

  texture_map = {}
  texture_map[None] = None
  iotexture_tmp = None
  for iotexture in ioscene.textures:
    if progress_cb:
      progress.x += 1
      progress_cb("convert texture", progress.x, progress.y)
    texture = ptr.add_texture(scene)
    # if ptr.texture_empty(texture, 'colorf'):
    if texture.colorf: # check if a list is empty by its type flexibility. https://therenegadecoder.com/code/how-to-check-if-a-list-is-empty-in-python/#check-if-a-list-is-empty-by-its-type-flexibility
      ptr.set_texture(texture, iotexture.colorf)
      size_colorf = img.image_vec3f.size(iotexture.colorf)
      if size_colorf.x:
        iotexture_tmp = iotexture
        # print(texture)
        # print(size_colorf.x)
        # print(size_colorf.y)
    elif texture.colorb:
      ptr.set_texture(texture, iotexture.colorb)
    elif texture.scalarf:
      ptr.set_texture(texture, iotexture.scalarf)
    elif texture.scalarb:
      ptr.set_texture(texture, iotexture.scalarb)
    texture_map[iotexture] = texture
    # print(texture_map[iotexture])
  
  material_map = {}
  material_map[None] = None
  for iomaterial in ioscene.materials:
    if progress_cb:
      progress.x += 1
      progress_cb("convert material", progress.x, progress.y)
    material = ptr.add_material(scene)
    ptr.set_emission(material, iomaterial.emission, texture_map[iomaterial.emission_tex])
    ptr.set_color(material, iomaterial.color, texture_map[iomaterial.color_tex])
    ptr.set_specular(material, iomaterial.specular, texture_map[iomaterial.specular_tex])
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
  subdiv_map[None] = None
  for iosubdiv in ioscene.subdivs:
    if progress_cb:
      progress.x += 1
      progress_cb("convert subdiv", progress.x, progress.y)
    subdiv = ptr.add_shape(scene)
    ptr.set_subdiv_quadspos(subdiv, iosubdiv.quadspos)
    ptr.set_subdiv_quadstexcoord(subdiv, iosubdiv.quadstexcoord)
    ptr.set_subdiv_positions(subdiv, iosubdiv.positions)
    ptr.set_subdiv_texcoords(subdiv, iosubdiv.texcoords)
    subdiv_map[iosubdiv] = subdiv

  shape_map = {}
  shape_map[None] = None
  for ioshape in ioscene.shapes:
    if progress_cb:
      progress.x += 1
      progress_cb("convert shape", progress.x, progress.y)
    shape = ptr.add_shape(scene)
    ptr.set_points(shape, ioshape.points)
    ptr.set_lines(shape, ioshape.lines)
    ptr.set_triangles(shape, ioshape.triangles)
    if ioshape.quads:
      ptr.set_triangles(shape, shp.quads_to_triangles(ioshape.quads))
    ptr.set_positions(shape, ioshape.positions)
    ptr.set_normals(shape, ioshape.normals)
    ptr.set_texcoords(shape, ioshape.texcoords)
    ptr.set_radius(shape, ioshape.radius)
    shape_map[ioshape] = shape
  
  for ioobject in ioscene.objects:
    if progress_cb:
      progress.x += 1
      progress_cb("convert object", progress.x, progress.y)
    if ioobject.instance:
      for frame in ioobject.instance.frames:
        yocto_object = ptr.add_object(scene)
        ptr.set_frame(yocto_object, frame * ioobject.frame)
        if ioobject.shape: ptr.set_shape(yocto_object, shape_map[ioobject.shape])
        if ioobject.subdiv:
          ptr.set_shape(yocto_object, subdiv_map[ioobject.subdiv])
          ptr.set_subdiv_subdivision(subdiv_map[ioobject.subdiv],
              ioobject.material.subdivisions, True)
          ptr.set_subdiv_displacement(subdiv_map[ioobject.subdiv],
              ioobject.material.displacement,
              texture_map[ioobject.material.displacement_tex])
        ptr.set_material(yocto_object, material_map[ioobject.material])
    else:
      yocto_object = ptr.add_object(scene)
      ptr.set_frame(yocto_object, ioobject.frame)
      if ioobject.shape: ptr.set_shape(yocto_object, shape_map[ioobject.shape])
      if ioobject.subdiv:
        ptr.set_shape(yocto_object, subdiv_map[ioobject.subdiv])
        ptr.set_subdiv_subdivision(subdiv_map[ioobject.subdiv],
            ioobject.material.subdivisions, True)
        ptr.set_subdiv_displacement(subdiv_map[ioobject.subdiv],
            ioobject.material.displacement,
            texture_map[iotexture_tmp])
            # texture_map[ioobject.material.displacement_tex])
        # print(texture_map[iotexture_tmp])
      ptr.set_material(yocto_object, material_map[ioobject.material])
  
  for ioenvironment in ioscene.environments:
    if progress_cb:
      progress.x += 1
      progress_cb("convert environment", progress.x, progress.y)
    environment = ptr.add_environment(scene)
    ptr.set_frame(environment, ioenvironment.frame)
    ptr.set_emission(environment, ioenvironment.emission,
        texture_map[ioenvironment.emission_tex])

  # done
  if (progress_cb):
    progress.x += 1
    progress_cb("convert done", progress.x, progress.y)

  # get camera
  camera = camera_map[iocamera]
  return scene, ioscene, camera, iocamera


def main(*argv):
  
  # options
  params = ptr.trace_params()
  save_batch  = False
  camera_name = ""
  # imfilename  = "out.hdr"
  filename    = "surface.json"
  imfilename  = "out.jpg"
  if len(argv) > 0 and len(argv[0]) > 1:
    if (argv[0][1]).startswith('tests/'):
      filename    = argv[0][1]

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
  # print(cli.options[9].value) # If I remove this everything blow up with segmentation-fault
  # commonio.parse_cli(cli, *argv)

  # scene loading
  # ioscene_guard = sio.model()
  ioscene = sio.model()
  ioerror = ""
  #  commonio.print_fatal(ioerror)
  if not sio.load_scene(filename, ioscene, ioerror, commonio.print_progress):
    commonio.print_fatal(ioerror)
  # get camera
  iocamera = sio.get_camera(ioscene, camera_name)

  # convert scene
  # scene_guard = ptr.scene()
  scene       = ptr.scene()
  camera      = None # ptr.camera.nullprt()
  scene, ioscene, camera, iocamera = init_scene(scene, ioscene, camera, iocamera, commonio.print_progress)

  # for shape in scene.shapes:
  #   displacement_tex = shape.subdiv_displacement_tex
  #   if displacement_tex:
  #     size_colorf = img.image_vec3f.size(displacement_tex.colorf)
  #     print("size_colorf.x: ", size_colorf.x)
  #     print("size_colorf.y: ",size_colorf.y)

  #     size_colorb = img.image_vec3b.size(displacement_tex.colorb)
  #     print("size_colorb.x: ", size_colorb.x)
  #     print("size_colorb.y: ",size_colorb.y)

  #     size_scalarf = img.image_float.size(displacement_tex.scalarf)
  #     print("size_scalarf.x: ", size_scalarf.x)
  #     print("size_scalarf.y: ",size_scalarf.y)

  #     size_scalarb = img.image_byte.size(displacement_tex.scalarb)
  #     print("size_scalarb.x: ", size_scalarb.x)
  #     print("size_scalarb.y: ",size_scalarb.y)
  # print(scene.shapes[0].subdiv_displacement_tex.colorb)
  # print(scene.shapes[0].subdiv_displacement_tex.scalarf)
  # print(scene.shapes[0].subdiv_displacement_tex.scalarb)

  # init subdivs
  ptr.init_subdivs(scene, params, commonio.print_progress) # floating point exception (core dumped)

  # # build bvh
  ptr.init_bvh(scene, params, commonio.print_progress) # ok

  # build lights
  ptr.init_lights(scene, params, commonio.print_progress) # ok

  # init state
  # state_guard = std::make_unique<ptr::state>()
  state = ptr.state()
  ptr.init_state(state, scene, camera, params) # segmentation fault (core dumped)
  print(img.image_pixel.size(state.pixels).x)
  # for pixel in state.pixels:
  # render
  commonio.print_progress("render image", 0, params.samples)
  sample = 0
  while sample < params.samples:
    commonio.print_progress("render image", sample, params.samples)
    # ptr.trace_samples(state, scene, camera, params)
    if save_batch:
        ext = "-s" + str(sample) + fs.path_extension(imfilename)
        outfilename = fs.path_replace_extension(imfilename, ext)
        ioerror     = ""
        commonio.print_progress("save image", sample, params.samples)
        if not img.save_image(outfilename, state.render, ioerror):
          commonio.print_fatal(ioerror)
    sample += 1
  commonio.print_progress("render image", params.samples, params.samples)

  # save image
  commonio.print_progress("save image", 0, 1)
  if not img.save_image(imfilename, state.render, ioerror): commonio.print_fatal(ioerror)
  commonio.print_progress("save image", 1, 1)

  # done

if __name__ == "__main__":
  main(sys.argv)
  
