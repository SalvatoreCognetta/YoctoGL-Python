import math
import py_math as mth
import py_shape as shp
import py_image as img
import py_pathtrace as ptr
import py_commonio  as commonio
import py_sceneio   as sio
import py_filesystem   as sfs
import sys

def parse_cli(args):
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
  
  i = 0
  for arg in args:
    if not arg.startswith('-') and i == 0 and arg.endswith('.hdr'):
      filename = arg
    elif arg.startswith('--tonemap'):
      tonemap_on = bool(args[i+1])
    elif arg.startswith('-e'):
      tonemap_exposure = int(args[i+1])
    elif arg.startswith('--filmic'):
      tonemap_filmic = bool(args[i+1])
    elif arg.startswith('--resize-width'):
      resize_width = int(args[i+1])
    elif arg.startswith('--resize-height'):
      resize_height = int(args[i+1])
    elif arg.startswith('--spatial-sigma'):
      spatial_sigma = float(args[i+1])
    elif arg.startswith('--range-sigma'):
      range_sigma = float(args[i+1])
    elif arg.startswith('--set-alpha'):
      alpha_filename = args[i+1]
    elif arg.startswith('--set-color-as-alpha'):
      coloralpha_filename = args[i+1]
    elif arg.startswith('--alpha-to-color'):
      alpha_to_color = bool(args[i+1])
    elif arg.startswith('--logo'):
      logo = bool(args[i+1])
    elif arg.startswith('--diff'):
      diff_filename = args[i+1]
    elif arg.startswith('--diff-signal'):
      diff_signal = bool(args[i+1])
    elif arg.startswith('--diff-threshold'):
      diff_threshold = float(args[i+1])
    elif arg.startswith('-o'):
      output = args[i+1]
    i += 1

  return filename, output, tonemap_on, tonemap_exposure, tonemap_filmic, logo, resize_width, resize_height, spatial_sigma, range_sigma, alpha_to_color, alpha_filename, diff_filename, diff_signal, diff_threshold
def filter_bilateral(image,
    spatial_sigma, range_sigma,
    features, features_sigma):
  filtered     = img.image_vec4f(img.image_vec4f.size(image), mth.zero4f)
  filter_width = int(math.ceil(2.57 * spatial_sigma))
  sw           = 1 / (2.0 * spatial_sigma * spatial_sigma)
  rw           = 1 / (2.0 * range_sigma * range_sigma)
  fw           = []
  for feature_sigma in features_sigma:
    fw.append(1 / (2.0 * feature_sigma * feature_sigma))
  j = 0
  while j < img.image_vec4f.size(image).y:
    i = 0
    while i < img.image_vec4f.size(image).x:
      av = mth.zero4f
      aw = 0.0
      fj = -filter_width
      while fj <= filter_width:
        fi = -filter_width
        while fi <= filter_width:
          ii = i + fi
          jj = j + fj
          if ii < 0 or jj < 0: 
            fi += 1
            continue
          if ii >= img.image_vec4f.size(image).x or jj >= img.image_vec4f.size(image).y: 
            fi += 1
            continue
          uv  = mth.vec2f(float(i - ii), float(j - jj))
          rgb = image.get(mth.vec2i(i, j)) - image.get(mth.vec2i(i, j))
          w   = float(math.exp(-mth.dot(uv, uv) * sw) ) * float(math.exp(-mth.dot(rgb, rgb) * rw))
          fi1 = 0
          while fi1 < len(features):
            feat = features[fi1].get(mth.vec2i(i, j)) - features[fi1].get(mth.vec2i(i, j))
            w *= math.exp(-mth.dot(feat, feat) * fw[fi1])
            fi1 += 1
          av = av + (w * image.get(mth.vec2i(ii, jj)))
          aw = aw + w
          fi += 1
        fj += 1
      filtered_tmp = filtered.get(mth.vec2i(i, j)) 
      filtered_tmp = av / aw
      i += 1
    j += 1
  return filtered

def make_image_preset(type_yocto, image, error):
  def set_region(image, region, offset):
    j = 0
    while j < region.size().y:
      i = 0
      while i < region.size().x:
        if not img.image_vec4f.contains(image, mth.vec2i(i, j)):
          i += 1
          continue
        img_tmp = image.get(mth.vec2i(i, j) + offset) 
        img_tmp = region.get(mth.vec2i(i, j))
        i += 1
      j += 1
    return image

  size = mth.vec2i(1024, 1024)
  if type_yocto.find("sky") != -1: size =  mth.vec2i(2048, 1024)
  if type_yocto.find("images2") != -1: size = mth.vec2i(2048, 1024)
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
        image, size, mth.pif / 4, 3.0, False, 1.0, 1.0, mth.vec3f(0.7, 0.7, 0.7))
  elif type_yocto == "sunsky":
    img.make_sunsky(
        image, size, mth.pif / 4, 3.0, True, 1.0, 1.0, mth.vec3f(0.7, 0.7, 0.7))
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
    image = img.srgb_to_rgb(img.bump_to_normal(image, 0.05))
  elif type_yocto == "images1":
    sub_types = ["grid", "uvgrid", "checker",
        "gammaramp", "bumps", "bump-normal", "noise", "fbm", "blackbodyramp"]
    sub_imgs  = []

    for i in range(len(sub_types)):
      sub_imgs.append(img.image_vec4f())

    i = 0
    while i < len(sub_types):
      ret_flag, type_yocto, image, error = make_image_preset(sub_types[i], sub_imgs[i], error)
      if not ret_flag: return False, type_yocto, image, error
      i +=1
    montage_size = mth.zero2i
    for sub_img in sub_imgs:
      montage_size.x += img.image_vec4f.size(sub_img).x
      montage_size.y = max(montage_size.y, img.image_vec4f.size(sub_img).y)
    image      = img.image_vec4f(montage_size)
    pos = 0
    for sub_img in sub_imgs:
      image = set_region(image, sub_img, mth.vec2i(pos, 0))
      pos += img.image_vec4f.size(sub_img).x
  elif type_yocto == "images2":
    sub_types = ["sky", "sunsky"]
    sub_imgs  = []

    for i in range(len(sub_types)):
      sub_imgs.append(img.image_vec4f())

    i = 0
    while i < len(sub_imgs):
      ret_flag, type_yocto, image, error = make_image_preset(sub_types[i], sub_imgs[i], error)
      if not ret_flag: return False, type_yocto, image, error
      i +=1
    montage_size = mth.zero2i
    for sub_img in sub_imgs:
      montage_size.x += img.image_vec4f.size(sub_img).x
      montage_size.y = max(montage_size.y, img.image_vec4f.size(sub_img).y)
    image      = img.image_vec4f(montage_size)
    pos = 0
    for sub_img in sub_imgs:
      image = set_region(image, sub_img, mth.vec2i(pos, 0))
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
        image, size, mth.pif / 4, 3.0, False, 1.0, 1.0, mth.vec3f(0.7, 0.7, 0.7))
  elif type_yocto == "test-sunsky":
    img.make_sunsky(
        image, size, mth.pif / 4, 3.0, True, 1.0, 1.0, mth.vec3f(0.7, 0.7, 0.7))
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
    img.make_checker(image, size, 1, mth.vec4f(1, 1, 1, 1), mth.vec4f(0, 0, 0, 0))
  elif type_yocto == "test-grid-opacity":
    img.make_grid(image, size, 1, mth.vec4f(1, 1, 1, 1), mth.vec4f(0, 0, 0, 0))
  else:
    error = "unknown preset"
    image   = []
    return False, type_yocto, image, error
  return True, type_yocto, image, error

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

  filename, output, tonemap_on, tonemap_exposure, tonemap_filmic, logo, resize_width, resize_height, spatial_sigma, range_sigma, alpha_to_color, alpha_filename, diff_filename, diff_signal, diff_threshold = parse_cli(argv[0][1:])

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
    ret_flag, basename, image, ioerror = make_image_preset(basename, image, ioerror)
    if not ret_flag: commonio.print_fatal(ioerror)
  else:
    if not img.load_image(filename, image, ioerror): commonio.print_fatal(ioerror)

  # set alpha
  if alpha_filename != "":
    alpha = img.image_vec4f()
    if not img.load_image(alpha_filename, alpha, ioerror): commonio.print_fatal(ioerror)
    if not mth.isEqual(img.image_vec4f.size(image), img.image_vec4f.size(alpha)): commonio.print_fatal("bad image size")
    j = 0
    while j < img.image_vec4f.size(image).y:
      i = 0
      while i < img.image_vec4f.size(image).x:
        image.get(mth.vec2i(i, j)).w = alpha.get(mth.vec2i(i, j)).w
        i += 1
      j += 1

  # set alpha
  if coloralpha_filename != "":
    alpha = img.image_vec4f()
    if not img.load_image(coloralpha_filename, alpha, ioerror):
      commonio.print_fatal(ioerror)
    if not mth.isEqual(img.image_vec4f.size(image), img.image_vec4f.size(alpha)): commonio.print_fatal("bad image size")
    j = 0
    while j < img.image_vec4f.size(image).y:
      i = 0
      while i < img.image_vec4f.size(image).x:
        image.get(mth.vec2i(i, j)).w = mth.mean(mth.xyz(alpha.get(mth.vec2i(i, j))))
        i += 1
      j += 1

  # set color from alpha
  if alpha_to_color:
    for c in image: 
      xyz = mth.xyz(c)
      xyz = mth.vec3f(c.w)

  # diff
  if diff_filename != "":
    diff = img.image_vec4f()
    if not img.load_image(diff_filename, diff, ioerror): commonio.print_fatal(ioerror)
    if not mth.isEqual(img.image_vec4f.size(image), img.image_vec4f.size(diff)):
      commonio.print_fatal("image sizes are different")
    image = img.image_difference(image, diff, True)

  # resize
  if resize_width != 0 or resize_height != 0:
    image = img.resize_image(image, mth.vec2i(resize_width, resize_height))

  # bilateral
  if spatial_sigma and range_sigma:
    image = filter_bilateral(image, spatial_sigma, range_sigma, [], [])

  # hdr correction
  if tonemap_on:
    image = img.tonemap_image(image, tonemap_exposure, tonemap_filmic, False)

  # save
  image_logo = None
  if logo:
    image_logo = img.add_logo(image)
  else:
    image_logo = image
  if not img.save_image(output, image_logo, ioerror):
    commonio.print_fatal(ioerror)

  # check diff
  if diff_filename != "" and diff_signal:
    for c in image:
      if mth.max(xyz(c)) > diff_threshold:
        commonio.print_fatal("image content differs")

  # done

if __name__ == "__main__":
  main(sys.argv)