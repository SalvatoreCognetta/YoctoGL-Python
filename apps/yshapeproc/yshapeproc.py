import math
import py_math as mth
import py_shape as shp
import py_commonio as commonio
import py_filesystem as fs
import sys

# Shape presets used for testing.
def make_shape_preset(points, lines, triangles, quads, quadspos, quadsnorm,
    quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error):
  if type_yocto == "default-quad":
    shp.make_rect(quads, positions, normals, texcoords)
  elif type_yocto == "default-quady":
    shp.make_recty(quads, positions, normals, texcoords)
  elif type_yocto == "default-cube":
    shp.make_box(quads, positions, normals, texcoords)
  elif type_yocto == "default-cube-rounded":
    shp.make_rounded_box(quads, positions, normals, texcoords)
  elif type_yocto == "default-sphere":
    shp.make_sphere(quads, positions, normals, texcoords)
  elif type_yocto == "default-disk":
    shp.make_disk(quads, positions, normals, texcoords)
  elif type_yocto == "default-disk-bulged":
    shp.make_bulged_disk(quads, positions, normals, texcoords)
  elif type_yocto == "default-quad-bulged":
    shp.make_bulged_rect(quads, positions, normals, texcoords)
  elif type_yocto == "default-uvsphere":
    shp.make_uvsphere(quads, positions, normals, texcoords)
  elif type_yocto == "default-uvsphere-flipcap":
    shp.make_capped_uvsphere(quads, positions, normals, texcoords)
  elif type_yocto == "default-uvdisk":
    shp.make_uvdisk(quads, positions, normals, texcoords)
  elif type_yocto == "default-uvcylinder":
    shp.make_uvcylinder(quads, positions, normals, texcoords)
  elif type_yocto == "default-uvcylinder-rounded":
    shp.make_rounded_uvcylinder(quads, positions, normals, texcoords, mth.vec3i(32, 32, 32)) # may need (32, 32, 32) at the end
  elif type_yocto == "default-geosphere":
    shp.make_geosphere(triangles, positions)
  elif type_yocto == "default-floor":
    shp.make_floor(quads, positions, normals, texcoords)
  elif type_yocto == "default-floor-bent":
    shp.make_bent_floor(quads, positions, normals, texcoords)
  elif type_yocto == "default-mattball":
    shp.make_sphere(quads, positions, normals, texcoords)
  elif type_yocto == "default-hairball":
    base_triangles = []
    base_quads = []
    base_positions = []
    base_normals = []
    base_texcoords = []
    shp.make_sphere(
      base_quads, base_positions, base_normals, base_texcoords, mth.pow2(5), 0.8)
    shp.make_hair(lines, positions, normals, texcoords, radius, base_triangles,
      base_quads, base_positions, base_normals, base_texcoords, mth.vec2i(4, 65536), mth.vec2f(0.2, 0.2), mth.vec2f(0.002, 0.001))
  elif type_yocto == "default-hairball-interior":
    shp.make_sphere(quads, positions, normals, texcoords, mth.pow2(5), 0.8)
  elif type_yocto == "default-suzanne":
    shp.make_monkey(quads, positions)
  elif type_yocto == "default-cube-facevarying":
    shp.make_fvbox(quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords)
  elif type_yocto == "default-sphere-facevarying":
    shp.make_fvsphere(quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords)
  elif type_yocto == "default-quady-displaced":
    shp.make_recty(quads, positions, normals, texcoords, mth.vec2i(256, 256))
  elif type_yocto == "default-sphere-displaced":
    shp.make_sphere(quads, positions, normals, texcoords, 128)
  elif type_yocto == "test-cube":
    shp.make_rounded_box(quads, positions, normals, texcoords, mth.vec3i(32, 32, 32), 
        mth.vec3f(0.075, 0.075, 0.075), mth.vec3f(1, 1, 1), 0.3*0.075)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-uvsphere":
    shp.make_uvsphere(quads, positions, normals, texcoords, mth.vec2i(32, 32), 0.075)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-uvsphere-flipcap":
    shp.make_capped_uvsphere(quads, positions, normals, texcoords, mth.vec2i(32, 32), 
        0.075, mth.vec2f(1, 1), 0.3*0.075)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-sphere":
    shp.make_sphere(quads, positions, normals, texcoords, 32 , 0.075, 1)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-sphere-displaced":
    shp.make_sphere(quads, positions, normals, texcoords, 128, 0.075, 1)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-disk":
    shp.make_disk(quads, positions, normals, texcoords, 32, 0.075, 1)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-uvcylinder":
    shp.make_rounded_uvcylinder(quads, positions, normals, texcoords, mth.vec3i(32, 32, 32), mth.vec2f(0.075, 0.075), mth.vec3f(1, 1, 1), 0.3*0.075)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-floor":
    shp.make_floor(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(2, 2), mth.vec2f(20, 20))
  elif type_yocto == "test-quad":
    shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.075, 0.075), mth.vec2f(1, 1))
  elif type_yocto == "test-quady":
    shp.make_recty(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.075, 0.075), mth.vec2f(1, 1))
  elif type_yocto == "test-quad-displaced":
    shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(256, 256), mth.vec2f(0.075, 0.075), mth.vec2f(1, 1))
  elif type_yocto == "test-quady-displaced":
    shp.make_recty(quads, positions, normals, texcoords, mth.vec2i(256, 256), mth.vec2f(0.075, 0.075), mth.vec2f(1, 1))
  elif type_yocto == "test-mattball":
    shp.make_sphere(quads, positions, normals, texcoords, 32, 0.075)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-hairball1":
    base_triangles = []
    base_quads = []
    base_positions = []
    base_normals = []
    base_texcoords = []
    shp.make_sphere(base_quads, base_positions, base_normals, base_texcoords, 32, 0.075*0.8 , 1)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
    shp.make_hair(lines, positions, normals, texcoords, radius, base_triangles, 
        base_quads, base_positions, base_normals, base_texcoords, mth.vec2i(4, 65536), 
        mth.vec2f( 0.1*0.15, 0.1*0.15), mth.vec2f(0.1*0.15, 0.1*0.15),
        mth.vec2f(0.03, 100))
  elif type_yocto == "test-hairball2":
    base_triangles = []
    base_quads = []
    base_positions = []
    base_normals = []
    base_texcoords = []
    shp.make_sphere(base_quads, base_positions, base_normals, base_texcoords, 
        32, 0.075*0.8 , 1)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
    shp.make_hair(lines, positions, normals, texcoords, radius, base_triangles,
        base_quads, base_positions, base_normals, base_texcoords, mth.vec2i(4, 65536),
        mth.vec2f( 0.1*0.15, 0.1*0.15), mth.vec2f(0.1*0.15, 0.1*0.15))
  elif type_yocto == "test-hairball3":
    base_triangles = []
    base_quads = []
    base_positions = []
    base_normals = []
    base_texcoords = []
    shp.make_sphere(base_quads, base_positions, base_normals, base_texcoords, 
        32, 0.075*0.8 , 1)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
    shp.make_hair(lines, positions, normals, texcoords, radius, base_triangles, 
        base_quads, base_positions, base_normals, base_texcoords, mth.vec2i(4, 65536),
        mth.vec2f( 0.1*0.15, 0.1*0.15), mth.vec2f(0.1*0.15, 0.1*0.15),
        mth.vec2f(0.5, 128))
  elif type_yocto == "test-hairball-interior":
    shp.make_sphere(quads, positions, normals, texcoords, 32, 0.075 * 0.8, 1)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-suzanne-subdiv":
    shp.make_monkey(quads, positions, 0.075 * 0.8)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)
  elif type_yocto == "test-cube-subdiv":
    shp.make_fvcube(quadspos, quadsnorm, quadstexcoord, positions, normals, 
        texcoords, 0.075)
    for p in positions: p = p + mth.vec3f(0, 0.075, 0)    
  elif type_yocto == "test-arealight1":
    shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.2, 0.2))
  elif type_yocto == "test-arealight2":
    shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.2, 0.2))
  elif type_yocto == "test-largearealight1":
    shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.4, 0.4))
  elif type_yocto == "test-largearealight2":
    shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(1, 1), mth.vec2f(0.4, 0.4))
  elif type_yocto == "test-pointlight1":
    shp.make_point(points, positions, normals, texcoords, radius, 0)
  elif type_yocto == "test-pointlight2":
    shp.make_point(points, positions, normals, texcoords, radius, 0)
  elif type_yocto == "test-point":
    shp.make_points(points, positions, normals, texcoords, radius, 1)
  elif type_yocto == "test-points":
    shp.make_points(points, positions, normals, texcoords, radius, 4096)
  elif type_yocto == "test-points-random":
    shp.make_random_points(points, positions, normals, texcoords, radius, 4096, mth.vec3f(0.2, 0.2, 0.2))
  elif type_yocto == "test-particles":
    shp.make_points(points, positions, normals, texcoords, radius, 4096)
  elif type_yocto == "test-cloth":
    shp.make_rect(quads, positions, normals, texcoords, mth.vec2i(64, 64), mth.vec2f(0.2, 0.2))
  elif type_yocto == "test-clothy":
    shp.make_recty(quads, positions, normals, texcoords, mth.vec2i(64, 64), mth.vec2f(0.2, 0.2))  
  else:
    error = "unknown preset"
    return False, points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error
  return True, points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error
  

# Shape presets for testing
def make_shape_preset1(points, lines, triangles, quads, 
    positions, normals, texcoords, colors, radius, type_yocto, error):
  quadspos = []
  quadsnorm = []
  quadstexcoord = []
  ret_flag, points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error = make_shape_preset(points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error)
  if not ret_flag:
    return False, points, lines, triangles, quads, positions, normals, texcoords, colors, radius, type_yocto, error 
  if quadspos:
    raise "bad preset type" # Could be wrong
  return True, points, lines, triangles, quads, positions, normals, texcoords, colors, radius, type_yocto, error 

 # Shape presets for testing
def make_shape_preset2(quadspos, quadsnorm, quadstexcoord, positions,
    normals, texcoords, type_yocto, error):
  points    = []
  lines     = []
  triangles = []
  quads     = []
  colors    = []
  radius    = []

  ret_flag, points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error  = make_shape_preset(points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error)
  if not ret_flag:
    return False, points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error
  if not quadspos:
    raise "bad preset type" # Could be wrong
  return True, points, lines, triangles, quads, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, colors, radius, type_yocto, error


def main(*argv):
  facevarying = False
  positiononly = False
  trianglesonly = False
  smooth = False
  faceted = False
  rotate = mth.zero3f
  scale = mth.vec3f(1, 1, 1)
  uscale = 1.0
  translate = mth.zero3f
  info = False
  geodesic_source = -1
  p0 = -1
  p1 = -1
  p2 = -1
  num_geodesic_samples = 0
  geodesic_scale = 30.0
  slise = False
  output = "out.ply"
  filename = "mesh.ply"

  cli = commonio.make_cli("ymshproc", "Applies operations on a triangle mesh")
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
  commonio.add_option(cli, "--num-geodesic-samples", num_geodesic_samples, 
      "Number of sampled geodesic sources", False)
  commonio.add_option(cli, "--geodesic-scale", geodesic_scale, "Geodesic scale", False)
  commonio.add_option(cli, "--slice", slise, "Slice mesh along field isolines", False)
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
    ext = fs.path_extension(filename) # ".ypreset" 
    basename = fs.path_stem(filename) # "default-hairball"
    if ext == ".ypreset":
      ret_flag, points, lines, triangles, quads, positions, normals, texcoords, colors, radius, basename, ioerror = make_shape_preset1(points, lines, triangles, quads, positions, 
              normals, texcoords, colors, radius, basename, ioerror)
      if not ret_flag:
        commonio.print_fatal(ioerror)
    else:
      if not shp.load_shape(filename, points, lines, triangles, quads, positions, 
              normals, texcoords, colors, radius, ioerror):
        commonio.print_fatal(ioerror)
  else:
    ext = fs.path_extension(filename)
    basename = fs.path_stem(filename)
    if ext == ".ypreset":
      ret_flag, quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, basename, ioerror = make_shape_preset2(quadspos, quadsnorm, quadstexcoord, positions, normals, texcoords, basename, ioerror)
      if not ret_flag:
        commonio.print_fatal(ioerror)
    else:
      if not shp.load_fvshape(filename, quadspos, quadsnorm,  quadstexcoord,
              positions, normals, texcoords, ioerror):
        commonio.print_fatal(ioerror)
  commonio.print_progress("load shape", 1, 1)

  # remove data
  if positiononly:
    normals = []
    texcoords =[]
    colors = []
    radius = []
    quadsnorm = []
    quadstexcoord = []
    if quadsnorm: mth.swap(quads, quadspos)

  # convert data
  if trianglesonly:
    if quadspos:
      raise "cannot convert facevarying data to triangles"
    if quads:
      triangles = shp.quads_to_triangles(quads)
      quads = []
  
  # print info
  if info:
    commonio.print_info("shape stats ------------")
    stats = shp.shape_stats(points, lines, triangles, quads, quadspos, 
        quadsnorm, quadstexcoord, positions, normals, texcoords, colors, 
        radius)
    for stat in stats:
      commonio.print_info(stat)
  
  # transform
  if uscale != 1: scale = scale * uscale
  if (not mth.vec3f.isEqual(translate, mth.zero3f)) or (not mth.vec3f.isEqual(rotate, mth.zero3f)) or (not mth.vec3f.isEqual(scale, mth.vec3f(1, 1, 1))):
    commonio.print_progress("transform shape", 0, 1) # Next line is very loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong
    xform = mth.translation_frame(translate) * mth.scaling_frame(scale)* mth.rotation_frame(mth.vec3f(1, 0, 0), mth.radians(rotate.x)) * mth.rotation_frame(mth.vec3f(1, 0, 0), mth.radians(rotate.x)) * mth.rotation_frame(mth.vec3f(1, 0, 0), mth.radians(rotate.x)) 
    for p in positions: p = mth.transform_point(xform, p)
    for n in normals:
      n = mth.transform_normal(xform, n, mth.max(scale) != mth.min(scale))
    commonio.print_progress("transform shape", 1, 1)
  
  # compute normals
  if smooth:
    commonio.print_progress("smooth shape", 0, 1)
    if points:
      vec_normals = [mth.vec3f(0, 0, 1)]*len(positions)
      normals = vec_normals
    elif lines:
      shp.compute_tangents(lines, positions)
    elif triangles:
      shp.compute_normals(triangles, positions)
    elif quads:
      shp.compute_normals(quads, positions)
    elif quadspos:
      shp.comput_normals(quadspos, positions)
      if quadspos: quadsnorm = quadspos
    commonio.print_progress("smooth shape", 0, 1)
  
  # remove normals
  if faceted:
    commonio.print_progress("facet shape", 0, 1)
    normals = []
    quadsnorm = []
    commonio.print_progress("facet shape", 1, 1)
  
  # compute geodesic and store them as colors
  if geodesic_source >= 0 or num_geodesic_samples > 0:
    commonio.print_progress("compute geodesic", 0, 1)
    adjacencies = shp.face_adjacencies(triangles)
    solver = shp.make_geodesic_solver(triangles, adjacencies, positions)
    sources = []
    if geodesic_source >= 0:
      sources = [geodesic_source]
    else:
      sources = shp.sample_vertices_poisson(solver, num_geodesic_samples)
    field = shp.compute_geodesic_distances(solver, sources)

    if slise:
      tags = [0]*len(triangles)
      shp.meandering_triangles(
          field, geodesic_scale, 0, 1, 2, triangles, tags, positions, normals)
      i = 0
      while i < len(triangles):
        if tags[i] == 1: triangles[i] = mth.vec3i(-1, -1, -1)
        i += 1
    else:
      i = 0
      while i < len(colors):
        colors.append(mth.vec3f(math.sin(geodesic_scale * field[i])))
        i += 1
    commonio.print_progress("compute geodesic", 1, 1)

  if p0 != -1:
    commonio.print_progress("cut mesh", 0, 1)
    tags = [0]*len(triangles) 
    adjacencies = shp.face_adjacencies(triangles)
    solver = shp.make_geodesic_solver(triangles, adjacencies, positions)

    paths     = []
    fields    = []
    fields.append(shp.compute_geodesic_distances(solver, [p0]))
    fields.append(shp.compute_geodesic_distances(solver, [p1]))
    fields.append(shp.compute_geodesic_distances(solver, [p2]))
    for i in range(0,3):
      for f in fields[i]: f = -f
    
    paths.append(shp.integrate_field(
      triangles, positions, adjacencies, tags, 0, fields[1], p0, p1))

    paths.append(shp.integrate_field(
      triangles, positions, adjacencies, tags, 0, fields[2], p1, p2))

    paths.append(shp.integrate_field(
      triangles, positions, adjacencies, tags, 0, fields[0], p2, p0))
    
    plines     = []
    ppositions = []
    for i in range(0,3):
      pos = shp.make_positions_from_path(paths[i], positions)
      line = []
      k = 0
      while k < len(pos - 1):
        line.append(mth.vec2i(k, k+1))
        line[k] += int(len(lines))
        k += 1
      for l in line:
        plines.insert(plines[-1], l)
      for p in pos:
        ppositions.insert(ppositions[-1], p)
    points    = []
    lines     = plines
    triangles = []
    quads     = []
    positions = ppositions
    normals   = []
    texcoords = []
    colors    = []
    radius    = []
    commonio.print_progress("cut mesh", 1, 1)
  
  if info:
    commonio.print_info("shape stats ------------")
    stats = shp.shape_stats(points, lines, triangles, quads, quadspos,
        quadsnorm, quadstexcoord, positions, normals, texcoords, colors,
        radius)
    for stat in stats: commonio.print_info(stat)
  
  # save mesh
  commonio.print_progress("save shape", 0, 1)
  if quadspos:
    if not shp.save_fvshape(output, quadspos, quadsnorm, quadstexcoord,
            positions, normals, texcoords, ioerror):
      commonio.print_fatal(ioerror)
  else:
    if not shp.save_shape(output, points, lines, triangles, quads, positions,
            normals, texcoords, colors, radius, ioerror):
      commonio.print_fatal(ioerror)
  commonio.print_progress("save shape", 1, 1)

  # done


if __name__ == "__main__":
  main(sys.argv)
