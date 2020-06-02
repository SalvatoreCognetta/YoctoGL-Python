import py_math
import py_shape as shp
import py_image as img
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import py_filesystem   as sfs
import sys

def make_image_preset(type_yocto, image, error):
  # set_region = [](img::image<vec4f>& img, const img::image<vec4f>& region,
  #                       const vec2i& offset) {
  #   for (j = 0; j < region.size().y; j++) {
  #     for (i = 0; i < region.size().x; i++) {
  #       if (!img.contains({i, j})) continue;
  #       img[vec2i{i, j} + offset] = region[{i, j}];
  #     }
  #   }
  # };

  size = py_math.vec2i(1024, 1024)
  if type_yocto.find("sky") != type_yocto.npos: size =  py_math.vec2i(2048, 1024)
  if type_yocto.find("images2") != type_yocto.npos: size = py_math.vec2i(2048, 1024)
  if type_yocto == "grid":
    img.make_grid(image, size)
  elif type_yocto == "checker":
    img.make_checker(image, size)
  elif type_yocto == "bumps":
    img.make_bumps(image, size)
  elif type_yocto == "uvramp":
    img.make_uvramp(image, size)
  elif type_yocto == "gammaramp":
    img.make_gammaramp(image, size)
  elif type_yocto == "blackbodyramp":
    img.make_blackbodyramp(image, size)
  elif type_yocto == "uvgrid":
    img.make_uvgrid(image, size)
  elif type_yocto == "sky":
    img.make_sunsky(
        image, size, py_math.pif / 4, 3.0, False, 1.0, 1.0, py_math.vec3f(0.7, 0.7, 0.7))
  elif type_yocto == "sunsky":
    img.make_sunsky(
        image, size, py_math.pif / 4, 3.0, True, 1.0, 1.0, py_math.vec3f(0.7, 0.7, 0.7))
  elif type_yocto == "noise":
    img.make_noisemap(image, size, 1)
  elif type_yocto == "fbm":
    img.make_fbmmap(image, size, 1)
  elif type_yocto == "ridge":
    img.make_ridgemap(image, size, 1)
  elif type_yocto == "turbulence":
    img.make_turbulencemap(image, size, 1)
  elif type_yocto == "bump-normal":
    img.make_bumps(image, size)
    img = img.srgb_to_rgb(img.bump_to_normal(image, 0.05))
  elif type_yocto == "images1":
    sub_types = {"grid", "uvgrid", "checker",
        "gammaramp", "bumps", "bump-normal", "noise", "fbm", "blackbodyramp"}
    sub_imgs  = {}
    i = 0
    # while i < len(sub_types):
    #   if not make_image_preset(sub_types[i], sub_imgs[i], error): return False
    #   i +=1
    # montage_size = py_math.zero2i
    # for sub_img in sub_imgs:
    #   montage_size.x += img.image_vec4f.size(sub_img).x
    #   montage_size.y = max(montage_size.y, img.image_vec4f.size(sub_img).y)
#     image      = img.image_vec4f(montage_size)
#     pos = 0
#     for sub_img in sub_imgs:
#       set_region(image, sub_img, py_math.vec2i(pos, 0))
#       pos += img.image_vec4f.size(sub_img).x
#   } else if (type_yocto == "images2") {
#     sub_types = std::vector<std::string>{"sky", "sunsky"};
#     sub_imgs  = std::vector<img::image<vec4f>>(sub_types.size());
#     for (i = 0; i < sub_imgs.size(); i++) {
#       if (!img.make_image_preset(sub_types[i], sub_imgs[i], error)) return false;
#     }
#     montage_size = zero2i;
#     for ( sub_img : sub_imgs) {
#       montage_size.x += sub_img.size().x;
#       montage_size.y = max(montage_size.y, sub_img.size().y);
#     }
#     img      = img::image<vec4f>(montage_size);
#     pos = 0;
#     for ( sub_img : sub_imgs) {
#       set_region(image, sub_img, {pos, 0});
#       pos += sub_img.size().x;
#     }
#   } else if (type_yocto == "test-floor") {
#     img.make_grid(image, size);
#     img = add_border(image, 0.0025f);
#   } else if (type_yocto == "test-grid") {
#     img.make_grid(image, size);
#   } else if (type_yocto == "test-checker") {
#     img.make_checker(image, size);
#   } else if (type_yocto == "test-bumps") {
#     img.make_bumps(image, size);
#   } else if (type_yocto == "test-uvramp") {
#     img.make_uvramp(image, size);
#   } else if (type_yocto == "test-gammaramp") {
#     img.make_gammaramp(image, size);
#   } else if (type_yocto == "test-blackbodyramp") {
#     img.make_blackbodyramp(image, size);
#   } else if (type_yocto == "test-uvgrid") {
#     img.make_uvgrid(image, size);
#   } else if (type_yocto == "test-sky") {
#     img.make_sunsky(
#         img, size, pif / 4, 3.0f, false, 1.0f, 1.0f, vec3f{0.7f, 0.7f, 0.7f});
#   } else if (type_yocto == "test-sunsky") {
#     img.make_sunsky(
#         img, size, pif / 4, 3.0f, true, 1.0f, 1.0f, vec3f{0.7f, 0.7f, 0.7f});
#   } else if (type_yocto == "test-noise") {
#     img.make_noisemap(image, size);
#   } else if (type_yocto == "test-fbm") {
#     img.make_noisemap(image, size);
#   } else if (type_yocto == "test-bumps-normal") {
#     img.make_bumps(image, size);
#     img = bump_to_normal(image, 0.05f);
#   } else if (type_yocto == "test-bumps-displacement") {
#     img.make_bumps(image, size);
#     img = srgb_to_rgb(image);
#   } else if (type_yocto == "test-fbm-displacement") {
#     img.make_fbmmap(image, size);
#     img = srgb_to_rgb(image);
#   } else if (type_yocto == "test-checker-opacity") {
#     img.make_checker(image, size, 1, {1, 1, 1, 1}, {0, 0, 0, 0});
#   } else if (type_yocto == "test-grid-opacity") {
#     img.make_grid(image, size, 1, {1, 1, 1, 1}, {0, 0, 0, 0});
#   } else {
#     error = "unknown preset";
#     img   = {};
#     return false;
#   }
#   return true;
# }

def main(*argv):
  # command line parameters
  tonemap_on          = False
  tonemap_exposure    = 0
  tonemap_filmic      = False
  logo                = False
  resize_width        = 0
  resize_height       = 0
  spatial_sigma       = 0.0
  range_sigma         = 0.0
  alpha_to_color      = False
  alpha_filename      = ""
  coloralpha_filename = ""
  diff_filename       = ""
  diff_signal         = False
  diff_threshold      = 0.0
  output              = "out.png"
  filename            = "img.hdr"

  # parse command line
  cli = commonio.make_cli("yimgproc", "Transform images")
  commonio.add_option(cli, "--tonemap/--no-tonemap", tonemap_on, "Tonemap image", False)
  commonio.add_option(cli, "--exposure,-e", tonemap_exposure, "Tonemap exposure", False)
  commonio.add_option(
      cli, "--filmic/--no-filmic", tonemap_filmic, "Tonemap uses filmic curve", False)
  commonio.add_option(cli, "--resize-width", resize_width,
      "resize size (0 to maintain aspect)", False)
  commonio.add_option(cli, "--resize-height", resize_height,
      "resize size (0 to maintain aspect)", False)
  commonio.add_option(cli, "--spatial-sigma", spatial_sigma, "blur spatial sigma", False)
  commonio.add_option(cli, "--range-sigma", range_sigma, "bilateral blur range sigma", False)
  commonio.add_option(
      cli, "--set-alpha", alpha_filename, "set alpha as this image alpha", False)
  commonio.add_option(cli, "--set-color-as-alpha", coloralpha_filename,
      "set alpha as this image color", False)
  commonio.add_option(cli, "--alpha-to-color/--no-alpha-to-color", alpha_to_color,
      "Set color as alpha", False)
  commonio.add_option(cli, "--logo/--no-logo", logo, "Add logo", False)
  commonio.add_option(cli, "--diff", diff_filename, "compute the diff between images", False)
  commonio.add_option(cli, "--diff-signal", diff_signal, "signal a diff as error", False)
  commonio.add_option(cli, "--diff-threshold,", diff_threshold, "diff threshold", False)
  commonio.add_option(cli, "--output,-o", output, "output image filename", False)
  commonio.add_option(cli, "filename", filename, "input image filename", True)

  # error std::string buffer
  error = ""

  # load
  ext      = sfs.path_extension(filename)
  basename = sfs.path_stem(filename)
  ioerror  = ""
  image      = img.image_vec4f()
  if ext == ".ypreset":
    if not make_image_preset(basename, image, ioerror): commonio.print_fatal(ioerror)
  else:
    if not img.load_image(filename, image, ioerror): commonio.print_fatal(ioerror)


if __name__ == "__main__":
  main(sys.argv)