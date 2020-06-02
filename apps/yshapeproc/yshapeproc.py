import py_math
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