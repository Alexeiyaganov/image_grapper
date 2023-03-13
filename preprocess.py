import os
import cv2
import numpy as np
import random
from cloths_segmentation.pre_trained_models import create_model


def preprocess(cloth, cloth_mask):
    blue = np.zeros(cloth.shape, dtype=np.uint8)
    blue[:] = (255, 0, 0)
    mask = cloth_mask
    inv_mask = cv2.bitwise_not(mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.erode(mask, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=1)
    inv_mask = cv2.erode(inv_mask, kernel, iterations=3)
    inv_mask = cv2.dilate(inv_mask, kernel, iterations=6)

    masked_cloth = cv2.bitwise_and(cloth, cloth, mask=mask)
    cv2.imshow("masked`", masked_cloth)

    blue_background = cv2.bitwise_and(blue, blue, mask=inv_mask)
    cv2.imshow("blue", blue)

    result = cv2.add(masked_cloth, blue)
    cv2.imshow("result", result)

    return result


def convert_to_3_channel(image):
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    print(image)
    return image


def make_mask(image):
    model = create_model("Unet_2020-10-30")
    model.eval()
    image = load_rgb(cloth)
    transform = albu.Compose([albu.Normalize(p=1)], p=1)
    padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)
    x = transform(image=padded_image)["image"]
    x = torch.unsqueeze(tensor_from_rgb_image(x), 0)
    with torch.no_grad():
        prediction = model(x)[0][0]
    mask = (prediction > 0).cpu().numpy().astype(np.uint8)
    mask = unpad(mask, pads)
    res = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    cv2.imwrite(os.path.join(name, name + "_mask.jpg"), res)


if __name__ == "__main__":
    name = str(random.randint(0, 135))
    cloth = cv2.imread(os.path.join("images/cloth/", name + ".jpg"))
    cloth = convert_to_3_channel(cloth)
    make_mask(cloth)
    mask = cv2.imread(os.path.join(name, name + "_mask.jpg"), 0)
    res = preprocess(cloth, mask)
    cv2.imwrite(os.path.join("images/cloth/", name + "_blue.jpg"), res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
