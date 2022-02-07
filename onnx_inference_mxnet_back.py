import numpy as np
import mxnet as mx
import config

from PIL import Image
from mxnet.contrib.onnx.onnx2mx.import_model import import_model
from collections import namedtuple


def image_preprocessing(image_name: str) -> mx.ndarray.ndarray.NDArray:
    """
    Preprocessing the image for model
    """
    image = mx.image.imread(image_name)
    image = mx.image.imresize(image, config.image_resize_to[0], config.image_resize_to[1])
    image = image.transpose((2, 0, 1))
    image = image.expand_dims(axis=0)
    image = image.astype(dtype='float32')
    return image


def get_model(ctx: mx.context.Context, model_name: str, input_size: tuple) -> mx.module.module.Module:
    """
    Load ONNX model as MXNet
    """
    sym, arg_params, aux_params = import_model(model_name)
    all_layers = sym.get_internals()
    sym = all_layers["fc1_output"]
    model = mx.mod.Module(symbol=sym, context=ctx, label_names=[])
    model.bind(for_training=False, data_shapes=[('data', (1, 3, input_size[0], input_size[1]))])
    model.set_params(arg_params, aux_params, allow_missing=True)
    return model


def get_feature(model: mx.module.module.Module, input_picture: np.ndarray) -> np.ndarray:
    Batch = namedtuple("Batch", ["data"])
    model.forward(Batch([input_picture]))
    embedding = np.squeeze(model.get_outputs()[0].asnumpy())
    return embedding


ctx = mx.cpu()
# Path to ONNX model
model_name = 'model_onnx/converted_model.onnx'
# Load ONNX model
print(type(config.input_size))
model = get_model(ctx, model_name, config.input_size)
print(type(model))
img_txt = 'onnx_1.6.txt'
image = 'photo.bmp'

image = Image.open(image)
img = np.array(image)

img = np.swapaxes(img, 0, 2)
img = np.swapaxes(img, 1, 2)  # change to (c, h,w) order
# img = img[np.newaxis, :]  # extend to (n, c, h, w)
img = image_preprocessing('photo.bmp')
print(type(img))
out = get_feature(model, img)
print(type(out))


open(img_txt, 'w').close()
with open(img_txt, "a") as file:
    for i in range(len(out)):
        file.write(str(out[i]) + '\n')
'''
def main():
    ctx = mx.cpu()
    image = image_preprocessing(config.image_name)
    model = get_model(ctx, config.mxnet_model_prefix, 0, image)
    model_out = model_output(model, image)
    write_output(config.output_file_name, model_out)
    print('Done.')


if __name__ == "__main__":
    main()
'''
