from PIL import Image
import os

def convert_to_jpg(dir_path):
  for filename in os.listdir(dir_path):
    if not filename.endswith(".jpg"):
      filepath = os.path.join(dir_path, filename)
      img = Image.open(filepath)
      rgb_im = img.convert("RGB")
      new_filepath = os.path.splitext(filepath)[0] + '.jpg'
      rgb_im.save(new_filepath)
      os.remove(filepath)

if __name__ == "__main__":
  convert_to_jpg("../images/cloth")
  convert_to_jpg("../images/person")
