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
      shp.make_rounded_uvcylinder(quads, positions, normals, texcoords) # may need (32, 32, 32) at the end
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
        base_quads, base_positions, base_normals, base_texcoords, (4, 65536), (0.2, 0.2), (0.002, 0.001)) #not sure how to put {4, 65536} in python
      
      
      