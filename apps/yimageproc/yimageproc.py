import py_math
import py_shape as shp
import py_image as img
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import py_filesystem   as sfs
import sys

# def filter_bilateral(img,
#     spatial_sigma, range_sigma,
#     features, features_sigma):
  # auto filtered     = img::image{img.size(), zero4f};
  # auto filter_width = (int)ceil(2.57f * spatial_sigma);
  # auto sw           = 1 / (2.0f * spatial_sigma * spatial_sigma);
  # auto rw           = 1 / (2.0f * range_sigma * range_sigma);
  # auto fw           = std::vector<float>();
  # for (auto feature_sigma : features_sigma)
  #   fw.push_back(1 / (2.0f * feature_sigma * feature_sigma));
  # for (auto j = 0; j < img.size().y; j++) {
  #   for (auto i = 0; i < img.size().x; i++) {
  #     auto av = zero4f;
  #     auto aw = 0.0f;
  #     for (auto fj = -filter_width; fj <= filter_width; fj++) {
  #       for (auto fi = -filter_width; fi <= filter_width; fi++) {
  #         auto ii = i + fi, jj = j + fj;
  #         if (ii < 0 || jj < 0) continue;
  #         if (ii >= img.size().x || jj >= img.size().y) continue;
  #         auto uv  = vec2f{float(i - ii), float(j - jj)};
  #         auto rgb = img[{i, j}] - img[{i, j}];
  #         auto w   = (float)math::exp(-dot(uv, uv) * sw) *
  #                  (float)math::exp(-dot(rgb, rgb) * rw);
  #         for (auto fi = 0; fi < features.size(); fi++) {
  #           auto feat = features[fi][{i, j}] - features[fi][{i, j}];
  #           w *= math::exp(-dot(feat, feat) * fw[fi]);
  #         }
  #         av += w * img[{ii, jj}];
  #         aw += w;
  #       }
  #     }
  #     filtered[{i, j}] = av / aw;
  #   }
  # }
  # return filtered;

def make_image_preset(type_yocto, image, error):
  def set_region(image, region, offset):
    j = 0
    while j < region.size().y:
      i = 0
      while i < region.size().x:
        if not img.image_vec4f.contains((py_math.vec2i(i, j))): continue
        image[py_math.vec2i(i, j) + offset] = region[py_math.vec2i(i, j)]
        i += 1
      j += 1
    return image

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
    sub_types = ["grid", "uvgrid", "checker",
        "gammaramp", "bumps", "bump-normal", "noise", "fbm", "blackbodyramp"]
    sub_imgs  = []

    for i in range(len(sub_types)):
      sub_imgs.append(None)

    i = 0
    while i < len(sub_types):
      if not make_image_preset(sub_types[i], sub_imgs[i], error): return False
      i +=1
    montage_size = py_math.zero2i
    for sub_img in sub_imgs:
      montage_size.x += img.image_vec4f.size(sub_img).x
      montage_size.y = max(montage_size.y, img.image_vec4f.size(sub_img).y)
    image      = img.image_vec4f(montage_size)
    pos = 0
    for sub_img in sub_imgs:
      image = set_region(image, sub_img, py_math.vec2i(pos, 0))
      pos += img.image_vec4f.size(sub_img).x
  elif type_yocto == "images2":
    sub_types = ["sky", "sunsky"]
    sub_imgs  = []

    for i in range(len(sub_types)):
      sub_imgs.append(None)

    i = 0
    while i < len(sub_imgs):
      if not img.make_image_preset(sub_types[i], sub_imgs[i], error): return False
      i +=1
    montage_size = py_math.zero2i
    for sub_img in sub_imgs:
      montage_size.x += img.image_vec4f.size(sub_img).x
      montage_size.y = max(montage_size.y, mg.image_vec4f.size(sub_img).y)
    img      = img.image_vec4f(montage_size)
    pos = 0
    for sub_img in sub_imgs:
      image = set_region(image, sub_img, py_math.vec2i(pos, 0))
      pos += img.image_vec4f.size(sub_img).x
  elif type_yocto == "test-floor":
    img.make_grid(image, size)
    image = img.add_border(image, 0.0025)
  elif type_yocto == "test-grid":
    img.make_grid(image, size)
  elif type_yocto == "test-checker":
    img.make_checker(image, size)
  elif type_yocto == "test-bumps":
    img.make_bumps(image, size)
  elif type_yocto == "test-uvramp":
    img.make_uvramp(image, size)
  elif type_yocto == "test-gammaramp":
    img.make_gammaramp(image, size)
  elif type_yocto == "test-blackbodyramp":
    img.make_blackbodyramp(image, size)
  elif type_yocto == "test-uvgrid":
    img.make_uvgrid(image, size)
  elif type_yocto == "test-sky":
    img.make_sunsky(
        image, size, py_math.pif / 4, 3.0, False, 1.0, 1.0, py_math.vec3f(0.7, 0.7, 0.7))
  elif type_yocto == "test-sunsky":
    img.make_sunsky(
        image, size, py_math.pif / 4, 3.0, True, 1.0, 1.0, py_math.vec3f(0.7, 0.7, 0.7))
  elif type_yocto == "test-noise":
    img.make_noisemap(image, size)
  elif type_yocto == "test-fbm":
    img.make_noisemap(image, size)
  elif type_yocto == "test-bumps-normal":
    img.make_bumps(image, size)
    image = img.bump_to_normal(image, 0.05)
  elif type_yocto == "test-bumps-displacement":
    img.make_bumps(image, size)
    image = img.srgb_to_rgb(image)
  elif type_yocto == "test-fbm-displacement":
    img.make_fbmmap(image, size)
    image = img.srgb_to_rgb(image)
  elif type_yocto == "test-checker-opacity":
    img.make_checker(image, size, 1, py_math.vec4f(1, 1, 1, 1), py_math.vec4f(0, 0, 0, 0))
  elif type_yocto == "test-grid-opacity":
    img.make_grid(image, size, 1, py_math.vec4f(1, 1, 1, 1), py_math.vec4f(0, 0, 0, 0))
  else:
    error = "unknown preset"
    image   = {}
    return False
  return True

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
  # filename            = "img.hdr"
  filename            = "tests/01_surface/textures/sky.hdr"

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

  # set alpha
  if alpha_filename != "":
    alpha = img.image_vec4f()
    if not img.load_image(alpha_filename, alpha, ioerror): commonio.print_fatal(ioerror)
    if len(image) != len(alpha): commonio.print_fatal("bad image size")
    j = 0
    while j < len(image).y:
      i = 0
      while i < len(img).x:
        image[py_math.vec2i(i, j)].w = alpha[py_math.vec2i(i, j)].w
        i += 1
      j += 1

  # set alpha
  if coloralpha_filename != "":
    alpha = img.image_vec4f()
    if not img.load_image(coloralpha_filename, alpha, ioerror):
      commonio.print_fatal(ioerror)
    if len(image) != len(alpha): commonio.print_fatal("bad image size")
    j = 0
    while j < len(image).y:
      i = 0
      while i < len(image).x:
        image[py_math.vec2i(i, j)].w = py_math.mean(py_math.xyz(alpha[py_math.vec2i(i, j)]))
        i += 1
      j += 1

  # set color from alpha
  if alpha_to_color:
    for c in image: 
      xyz = py_math.xyz(c)
      xyz = py_math.vec3f(c.w)

  # diff
  if diff_filename != "":
    diff = img.image_vec4f()
    if not img.load_image(diff_filename, diff, ioerror): commonio.print_fatal(ioerror)
    if len(image) != len(diff):
      commonio.print_fatal("image sizes are different")
    image = img.image_difference(img, diff, True)

  # resize
  if resize_width != 0 or resize_height != 0:
    image = img.resize_image(img, py_math.vec2i(resize_width, resize_height))

  # // bilateral
  # if (spatial_sigma && range_sigma) {
  #   img = filter_bilateral(img, spatial_sigma, range_sigma, {}, {})
  # }

  # // hdr correction
  # if (tonemap_on) {
  #   img = tonemap_image(img, tonemap_exposure, tonemap_filmic, false)
  # }

  # // save
  # if (!save_image(output, logo ? add_logo(img) : img, ioerror))
  #   cli::print_fatal(ioerror)

  # // check diff
  # if (diff_filename != "" && diff_signal) {
  #   for ( c : img) {
  #     if (max(xyz(c)) > diff_threshold)
  #       cli::print_fatal("image content differs")
  #   }
  # }

  # done

if __name__ == "__main__":
  main(sys.argv)