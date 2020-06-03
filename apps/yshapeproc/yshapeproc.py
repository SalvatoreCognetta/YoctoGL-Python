import py_math as mth
import py_shape as shp
import py_commonio as commonio
import py_filesystem as fs
import sys

def make_shape_preset(points, lines, triangles, quads, quadspos, quadsnorm,
    quadstexcoord, positions, normals, texcoords, colors, radius, tipe, error):
    if tipe == "default-quad":
      shp.make_rect(quads, positions, normals, texcoords)
    elif tipe == "default-quady":
      shp.make_recty(quads, positions, normals, texcoords)
    elif tipe == "default-cube":
      shp.make_box(quads, positions, normals, texcoords)
    elif tipe == "default-cube-rounded":
      shp.make_rounded_box(quads, positions, normals, texcoords)
    elif tipe == "default-sphere":
      shp.make_sphere(quads, positions, normals, texcoords)
    elif tipe == "default-disk":
      shp.make_disk(quads, positions, normals, texcoords)
    elif tipe == "default-disk-bulged":
      shp.make_bulged_disk(quads, positions, normals, texcoords)
    elif tipe == "default-quad-bulged":
      shp.make_bulged_rect(quads, positions, normals, texcoords)
    elif tipe == "default-uvsphere":
      shp.make_uvsphere(quads, positions, normals, texcoords)
    elif tipe == "default-uvsphere-flipcap":
      shp.make_capped_uvsphere(quads, positions, normals, texcoords)
    elif tipe == "default-uvdisk":
      shp.make_uvdisk(quads, positions, normals, texcoords)
    elif tipe == "default-uvcylinder":
      shp.make_uvcylinder(quads, positions, normals, texcoords)
    elif tipe == "default-uvcylinder-rounded":
      shp.make_rounded_uvcylinder(quads, positions, normals, texcoords, mth.vec3i(32, 32, 32)) # may need (32, 32, 32) at the end
    elif tipe == "default-geosphere":
      shp.make_geosphere(triangles, positions)
    elif tipe == "default-floor":
      shp.make_floor(quads, positions, normals, texcoords)
    elif tipe == "default-floor-bent":
      shp.make_bent_floor(quads, positions, normals, texcoords)
    elif tipe == "default-mattball":
      shp.make_sphere(quads, positions, normals, texcoords)
    elif tipe == "default-hairball":
      base_triangles = []
      base_quads = []
      base_positions = []
      base_normals = []
      base_texcoords = []
      shp.make_sphere(
        base_quads, base_positions, base_normals, base_texcoords, mth.pow2(5), 0.8)
      shp.make_hair(lines, positions, normals, texcoords, radius, base_triangles,
        base_quads, base_positions, base_normals, base_texcoords, mth.vec2i(4, 65536), mth.vec2f(0.2, 0.2), mth.vec2f(0.002, 0.001)) #not sure how to put {4, 65536} in python
    elif tipe == "default-hairball-interior":
      shp.make_sphere(quads, positions, normals, texcoords, mth.pow2(5), 0.8)
    elif tipe == "default-suzanne":
      shp.make_monkey(quads, positions)
    elif tipe == "default-cube-facevarying":
      shp.make_fvbox(quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords)
    elif tipe == "default-sphere-facevarying":
      shp.make_fvsphere(quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords)
    elif tipe == "default-quady-displaced":
      shp.make_recty(quads, positions, normals, texcoords, mth.vec2i(256, 256))
    elif tipe == "default-sphere-displaced":
      shp.make_sphere(quads, positions, normals, texcoords, 128)
    elif tipe == "test-cube":
      shp.make_rounded_box(quads, positions, normals, texcoords, mth.vec3i(32, 32, 32), mth.vec3f(0.075, 0.075, 0.075), mth.vec3f(1, 1, 1), 0.3*0.075)
      for p in positions:
        p =  p + mth.vec3f(0, 0.075, 0) # di sicuro sbagliato chiedi a salvatore
    elif tipe == "test-uvsphere":
      shp.make_uvsphere(quads, positions, normals, texcoords, mth.vec2i(32, 32), 0.075)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-uvsphere-flipcap":
      shp.make_capped_uvsphere(quads, positions, normals, texcoords, mth.vec2i(32, 32), 0.075, mth.vec2f(1, 1), 0.3*0.075)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-sphere":
      shp.make_sphere(quads, positions, normals, texcoords, 32 , 0.075, 1)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-sphere-displaced":
      shp.make_sphere(quads, positions, normals, texcoords, 128, 0.075, 1)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-disk":
      shp.make_disk(quads, positions, normals, texcoords, 32, 0.075, 1)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-uvcylinder":
      shp.make_rounded_uvcylinder(quads, positions, normals, texcoords, mth.vec3i(32, 32, 32), mth.vec2f(0.075, 0.075), mth.vec3f(1, 1, 1), 0.3*0.075)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-floor":
      shp.make_floor(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(2, 2), mth.vec2f(20, 20))
    elif tipe == "test-quad":
      shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.075, 0.075), mth.vec2f(1, 1))
    elif tipe == "test-quady":
      shp.make_recty(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.075, 0.075), mth.vec2f(1, 1))
    elif tipe == "test-quad-displaced":
      shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(256, 256), mth.vec2f(0.075, 0.075), mth.vec2f(1, 1))
    elif tipe == "test-quady-displaced":
      shp.make_recty(quads, positions, normals, texcoords, mth.vec2i(256, 256), mth.vec2f(0.075, 0.075), mth.vec2f(1, 1))
    elif tipe == "test-mattball":
      shp.make_sphere(quads, positions, normals, texcoords, 32, 0.075)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-hairball1":
      base_triangles = []
      base_quads = []
      base_positions = []
      base_normals = []
      base_texcoords = []
      shp.make_sphere(base_quads, base_positions, base_normals, base_texcoords, 32, 0.075*0.8 , 1)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
      shp.make_hair(lines, positions, normals, texcoords, radius, base_triangles, base_quads, base_positions, base_normals, base_texcoords,
        mth.vec2i(4, 65536), mth.vec2f( 0.1*0.15, 0.1*0.15), mth.vec2f(0.1*0.15, 0.1*0.15), mth.vec2f(0.03, 100))
    elif tipe == "test-hairball2":
      base_triangles = []
      base_quads = []
      base_positions = []
      base_normals = []
      base_texcoords = []
      shp.make_sphere(base_quads, base_positions, base_normals, base_texcoords, 32, 0.075*0.8 , 1)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
      shp.make_hair(lines, positions, normals, texcoords, radius, base_triangles, base_quads, base_positions, base_normals, base_texcoords,
        mth.vec2i(4, 65536), mth.vec2f( 0.1*0.15, 0.1*0.15), mth.vec2f(0.1*0.15, 0.1*0.15))
    elif tipe == "test-hairball3":
      base_triangles = []
      base_quads = []
      base_positions = []
      base_normals = []
      base_texcoords = []
      shp.make_sphere(base_quads, base_positions, base_normals, base_texcoords, 32, 0.075*0.8 , 1)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
      shp.make_hair(lines, positions, normals, texcoords, radius, base_triangles, base_quads, base_positions, base_normals, base_texcoords,
        mth.vec2i(4, 65536), mth.vec2f( 0.1*0.15, 0.1*0.15), mth.vec2f(0.1*0.15, 0.1*0.15), mth.vec2f(0.5, 128))
    elif tipe == "test-hairball-interior":
      shp.make_sphere(quads, positions, normals, texcoords, 32, 0.075 * 0.8, 1)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-suzanne-subdiv":
      shp.make_monkey(quads, positions, 0.075 * 0.8)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)
    elif tipe == "test-cube-subdiv":
      shp.make_fvcube(quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, 0.075)
      for p in positions:
        p = p + mth.vec3f(0, 0.075, 0)    
    elif tipe == "test-arealight1":
      shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.2, 0.2))
    elif tipe == "test-arealight2":
      shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.2, 0.2))
    elif tipe == "test-largearealight1":
      shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.4, 0.4))
    elif tipe == "test-largearealight2":
      shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.4, 0.4))
    elif tipe == "test-pointlight1":
      shp.make_point(points, positions, normals, texcoords, radius, 0)
    elif tipe == "test-pointlight2":
      shp.make_point(points, positions, normals, texcoords, radius, 0)
    elif tipe == "test-point":
      shp.make_points(points, positions, normals, texcoords, radius, 1)
    elif tipe == "test-points":
      shp.make_points(points, positions, normals, texcoords, radius, 4096)
    elif tipe == "test-points-random":
      shp.make_random_points(points, positions, normals, texcoords, radius, 4096, mth.vec3f(0.2, 0.2, 0.2))
    elif tipe == "test-particles":
      shp.make_points(points, positions, normals, texcoords, radius, 4096)
    elif tipe == "test-cloth":
      shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(64, 64), mth.vec2f(0.2, 0.2))
    elif tipe == "test-clothy":
      shp.make_recty(quads, positions, normals, texcoords, mth.vec2i(64, 64), mth.vec2f(0.2, 0.2))  
    else:
      error = "unknown preset"
      return False, points, lines, triangles, quads, quadspos, quadsnorm,
      quadstexcoord, positions, normals, texcoords, colors, radius, tipe, error


# Shape presets for testing
def make_shape_preset1(points, lines, triangles, quads, positions, normals, texcoords, colors, radius,
    tipe, error):
    quadspos = []
    quadsnorm = []
    quadstexcoord = []
    if not make_shape_preset(points, lines, triangles, quads, quadspos, quadsnorm,
          quadstexcoord, positions, normals, texcoords, colors, radius, tipe, error):

          return False, points, lines, triangles, quads, positions, normals, texcoords, colors, radius,
          tipe, error 
    if not quadspos:
      raise "bad preset type" # Could be wrong

 
def main(*argv):
  facevarying = False
  positiononly = False
  trianglesonly = False
  smooth = False
  faceted = False
  rotate = mth.zero3f
  scale = mth.vec3f(1)
  uscale = 1.0
  translate = mth.zero3f
  info = False
  geodesic_source = -1
  p0 = -1
  p1 = -1
  p2 = -1
  num_geodesic_samples = 0
  geodesic_scale = 30.0
  slice = False
  output = "out.ply"
  filename = "mesh.ply"

  cli = commonio.make("ymshproc", "Applies operations on a triangle mesh")
  commonio.add_option(cli, "--facevarying", facevarying, "Preserve facevarying",False)
  commonio.add_option(cli, "--positiononly", positiononly, "Remove all but positions", False)
  commonio.add_option(cli, "--trianglesonly", trianglesonly, "Remove all but triangles" ,False)
  commonio.add_option(cli, "--smooth", smooth, "Compute smooth normals",False)
  commonio.add_option(cli, "--faceted", faceted, "Remove normals",False)
  commonio.add_option(cli, "--rotatey,-ry", rotate.y, "Rotate around y axis",False)
  commonio.add_option(cli, "--rotatex,-rx", rotate.x, "Rotate around x axis",False)
  commonio.add_option(cli, "--rotatez,-rz", rotate.z, "Rotate around z axis",False)
  commonio.add_option(cli, "--translatey,-ty", translate.y, "Translate along y axis",False)
  commonio.add_option(cli, "--translatex,-tx", translate.x, "Translate along x axis",False)
  commonio.add_option(cli, "--translatez,-tz", translate.z, "Translate along z axis",False)
  commonio.add_option(cli, "--scale,-s", uscale, "Scale along xyz axes",False)
  commonio.add_option(cli, "--scaley,-sy", scale.y, "Scale along y axis",False)
  commonio.add_option(cli, "--scalex,-sx", scale.x, "Scale along x axis",False)
  commonio.add_option(cli, "--scalez,-sz", scale.z, "Scale along z axis",False)
  commonio.add_option(cli, "--info,-i", info, "print mesh info",False)
  commonio.add_option(cli, "--geodesic-source,-g", geodesic_source, "Geodesic source",False)
  commonio.add_option(cli, "--path-vertex0,-p0", p0, "Path vertex 0",False)
  commonio.add_option(cli, "--path-vertex1,-p1", p1, "Path vertex 1",False)
  commonio.add_option(cli, "--path-vertex2,-p2", p2, "Path vertex 2",False)
  commonio.add_option(cli, "--num-geodesic-samples", num_geodesic_samples, "Number of sampled geodesic sources", False)
  commonio.add_option(cli, "--geodesic-scale", geodesic_scale, "Geodesic scale", False)
  commonio.add_option(cli, "--slice", slice, "Slice mesh along field isolines", False)
  commonio.add_option(cli, "--output,-o", output, "output mesh", False)
  commonio.add_option(cli, "mesh", filename, "input mesh", True)

  positions= []
  normals = []
  texcoords = []
  colors = []
  radius = []
  points = []
  lines = []
  triangles = []
  quads = []
  quadspos = []
  quadsnorm = []
  quadstexcoord = []

  ioerror = ""
  commonio.print_progress("load shape", 0, 1)
  if not facevarying:
    ext = fs.path_extension(filename)
    basename = fs.path_stem(filename)
    if ext == ".ypreset":
      if not make_shape_preset(points, lines, triangles, quads, positions, normals, texcoords, colors,
        radius, ioerror):
        commonio.print_fatal(ioerror)
    else:
      if not shp.load_shape(filename, points, lines, triangles, quads, positions, normals, texcoords, colors,
        radius, ioerror):
        commonio.print_fatal(ioerror)
  else:
    ext = fs.path_extension(filename)
    basename = fs.path_stem(filename)
    if ext == ".ypreset":
      if not make_shape_preset1(quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords,
        basename, ioerror):
        commonio.print_fatal(ioerror)
    else:
      if not shp.load_fvshape(filename, quadspos, quadsnorm,  quadstexcoord, positions, normals, texcoords,
        ioerror):
        commonio.print_fatal(ioerror)
  

  commonio.print_progress("load shape", 1, 1)

  #swap function
  def swap(left, right):
    temp = left
    left = right
    right = temp
    return (left, right)


  #remove data
  if positiononly:
    normals = []
    texcoords =[]
    colors = []
    radius = []
    quadsnorm = []
    quadstexcoord = []

    if quadsnorm:
      swap(quads, quadspos)#not sure about swap

  #convert data
  if trianglesonly:
    if quadspos:
      raise "cannot convert facevarying data to triangles"
    if quads:
      triangles = shp.quads_to_triangles
      quads = []
  
  if info:
    commonio.print_info("shape stats ------------")
    stats = shp.shape_stats(points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions,
      normals, texcoords, colors, radius)
    for stat in stats:
      commonio.print_info(stat)
  
  #transform
  if uscale != 1:
    scale = scale * uscale
  if translate != mth.zero3f or rotate != mth.zero3f or scale != mth.vec3f(1):
    commonio.print_progress("transform shape", 0, 1) # Next line is very loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong
    xform = mth.translation_frame(translate) * mth.scaling_frame(scale)* mth.rotation_frame(mth.vec3f(1, 0, 0), mth.radians(rotate.x)) * mth.rotation_frame(mth.vec3f(1, 0, 0), mth.radians(rotate.x)) * mth.rotation_frame(mth.vec3f(1, 0, 0), mth.radians(rotate.x)) 
    for p in positions:
      p = mth.transform_point(xform, p)
    for n in normals:
      n = mth.transform_normal(xform, n, mth.max(scale) != mth.min(scale))
    commonio.print_progress("transform shape", 1, 1)
  
  #compute normals
  if (smooth):
    commonio.print_progress("smooth shape", 0, 1)
    if points:
      normals = [positions.len(), mth.vec3f(0, 0, 1)] #WTF DOES THIS MEAN?
    elif lines:
      shp.compute_tangents(lines, positions)
    elif triangles:
      shp.compute_normals(triangles, positions)
    elif quads:
      shp.compute_normals(quads, positions)
    elif quadspos:
      shp.comput_normals(quadspos, positions)
      if quadspos:
        quadsnorm = quadspos
    commonio.print_progress("smooth shape", 0, 1)
  
  #remove normals
  if faceted:
    commonio.print_progress("facet shape", 0, 1)
    normals = []
    quadsnorm = []
    commonio.print_progress("facet shape", 1, 1)
  
  # #compute geodesic and store them as colors
  # if geodesic_source >= 0 or num_geodesic_samples > 0:
  #   commonio.print_progress("compute geodesic", 0, 1)







    
