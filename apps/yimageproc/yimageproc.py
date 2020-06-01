import py_math
import py_shape as shp
import py_image as img
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import py_filesystem   as sfs
import sys

def make_image_preset(type, image, error):
  # set_region = [](img::image<vec4f>& img, const img::image<vec4f>& region,
  #                       const vec2i& offset) {
  #   for (j = 0; j < region.size().y; j++) {
  #     for (i = 0; i < region.size().x; i++) {
  #       if (!img.contains({i, j})) continue;
  #       img[vec2i{i, j} + offset] = region[{i, j}];
  #     }
  #   }
  # };

#   size = py_math.vec2i(1024, 1024)
#   if type.find("sky") != type.npos: size =  py_math.vec2i(2048, 1024)
#   if type.find("images2") != type.npos: size = py_math.vec2i(2048, 1024)
#   if type == "grid":
#     make_grid(img, size)
#   elif type == "checker":
#     make_checker(img, size)
#   elif type == "bumps":
#     make_bumps(img, size)
#   elif type == "uvramp":
#     make_uvramp(img, size)
#   elif type == "gammaramp":
#     make_gammaramp(img, size)
#   elif type == "blackbodyramp":
#     make_blackbodyramp(img, size)
#   elif type == "uvgrid":
#     make_uvgrid(img, size)
#   elif type == "sky":
#     make_sunsky(
#         img, size, pif / 4, 3.0, false, 1.0, 1.0, vec3f(0.7, 0.7, 0.7))
#   elif type == "sunsky":
#     make_sunsky(
#         img, size, pif / 4, 3.0, true, 1.0, 1.0, vec3f(0.7, 0.7, 0.7))
#   elif type == "noise":
#     make_noisemap(img, size, 1)
#   elif type == "fbm":
#     make_fbmmap(img, size, 1)
#   elif type == "ridge":
#     make_ridgemap(img, size, 1)
#   elif type == "turbulence":
#     make_turbulencemap(img, size, 1)
#   elif type == "bump-normal":
#     make_bumps(img, size)
#     img = srgb_to_rgb(bump_to_normal(img, 0.05))
#   elif type == "images1":
#     sub_types = std::vector<std::string>{"grid", "uvgrid", "checker",
#         "gammaramp", "bumps", "bump-normal", "noise", "fbm", "blackbodyramp"}
#     sub_imgs  = std::vector<img::image<vec4f>>(sub_types.size())
#     for (i = 0; i < sub_imgs.size(); i++) {
#       if (!make_image_preset(sub_types[i], sub_imgs[i], error)) return false;
#     }
#     montage_size = zero2i;
#     for ( sub_img : sub_imgs) {
#       montage_size.x += sub_img.size().x;
#       montage_size.y = max(montage_size.y, sub_img.size().y);
#     }
#     img      = img::image<vec4f>(montage_size);
#     pos = 0;
#     for ( sub_img : sub_imgs) {
#       set_region(img, sub_img, {pos, 0});
#       pos += sub_img.size().x;
#     }
#   } else if (type == "images2") {
#     sub_types = std::vector<std::string>{"sky", "sunsky"};
#     sub_imgs  = std::vector<img::image<vec4f>>(sub_types.size());
#     for (i = 0; i < sub_imgs.size(); i++) {
#       if (!make_image_preset(sub_types[i], sub_imgs[i], error)) return false;
#     }
#     montage_size = zero2i;
#     for ( sub_img : sub_imgs) {
#       montage_size.x += sub_img.size().x;
#       montage_size.y = max(montage_size.y, sub_img.size().y);
#     }
#     img      = img::image<vec4f>(montage_size);
#     pos = 0;
#     for ( sub_img : sub_imgs) {
#       set_region(img, sub_img, {pos, 0});
#       pos += sub_img.size().x;
#     }
#   } else if (type == "test-floor") {
#     make_grid(img, size);
#     img = add_border(img, 0.0025f);
#   } else if (type == "test-grid") {
#     make_grid(img, size);
#   } else if (type == "test-checker") {
#     make_checker(img, size);
#   } else if (type == "test-bumps") {
#     make_bumps(img, size);
#   } else if (type == "test-uvramp") {
#     make_uvramp(img, size);
#   } else if (type == "test-gammaramp") {
#     make_gammaramp(img, size);
#   } else if (type == "test-blackbodyramp") {
#     make_blackbodyramp(img, size);
#   } else if (type == "test-uvgrid") {
#     make_uvgrid(img, size);
#   } else if (type == "test-sky") {
#     make_sunsky(
#         img, size, pif / 4, 3.0f, false, 1.0f, 1.0f, vec3f{0.7f, 0.7f, 0.7f});
#   } else if (type == "test-sunsky") {
#     make_sunsky(
#         img, size, pif / 4, 3.0f, true, 1.0f, 1.0f, vec3f{0.7f, 0.7f, 0.7f});
#   } else if (type == "test-noise") {
#     make_noisemap(img, size);
#   } else if (type == "test-fbm") {
#     make_noisemap(img, size);
#   } else if (type == "test-bumps-normal") {
#     make_bumps(img, size);
#     img = bump_to_normal(img, 0.05f);
#   } else if (type == "test-bumps-displacement") {
#     make_bumps(img, size);
#     img = srgb_to_rgb(img);
#   } else if (type == "test-fbm-displacement") {
#     make_fbmmap(img, size);
#     img = srgb_to_rgb(img);
#   } else if (type == "test-checker-opacity") {
#     make_checker(img, size, 1, {1, 1, 1, 1}, {0, 0, 0, 0});
#   } else if (type == "test-grid-opacity") {
#     make_grid(img, size, 1, {1, 1, 1, 1}, {0, 0, 0, 0});
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
  commonio.add_option(cli, "--tonemap/--no-tonemap", tonemap_on, "Tonemap image")
  commonio.add_option(cli, "--exposure,-e", tonemap_exposure, "Tonemap exposure")
  commonio.add_option(
      cli, "--filmic/--no-filmic", tonemap_filmic, "Tonemap uses filmic curve")
  commonio.add_option(cli, "--resize-width", resize_width,
      "resize size (0 to maintain aspect)")
  commonio.add_option(cli, "--resize-height", resize_height,
      "resize size (0 to maintain aspect)")
  commonio.add_option(cli, "--spatial-sigma", spatial_sigma, "blur spatial sigma")
  commonio.add_option(cli, "--range-sigma", range_sigma, "bilateral blur range sigma")
  commonio.add_option(
      cli, "--set-alpha", alpha_filename, "set alpha as this image alpha")
  commonio.add_option(cli, "--set-color-as-alpha", coloralpha_filename,
      "set alpha as this image color")
  commonio.add_option(cli, "--alpha-to-color/--no-alpha-to-color", alpha_to_color,
      "Set color as alpha")
  commonio.add_option(cli, "--logo/--no-logo", logo, "Add logo")
  commonio.add_option(cli, "--diff", diff_filename, "compute the diff between images")
  commonio.add_option(cli, "--diff-signal", diff_signal, "signal a diff as error")
  commonio.add_option(cli, "--diff-threshold,", diff_threshold, "diff threshold")
  commonio.add_option(cli, "--output,-o", output, "output image filename")
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
    if not load_image(filename, image, ioerror): commonio.print_fatal(ioerror)


if __name__ == "__main__":
  main(sys.argv)