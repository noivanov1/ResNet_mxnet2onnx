import numpy as np
import mxnet as mx
import config

from collections import namedtuple


def image_preprocessing(image_name: str) -> np.ndarray:
    image = mx.image.imread(image_name)
    image = mx.image.imresize(image, 112, 112)  # resize
    image = image.transpose((2, 0, 1))  # Channel first
    image = image.expand_dims(axis=0)  # batchify
    image = image.astype(dtype='float32')
    return image


def model_output(ctx: mx.context.Context, model_prefix: str, epoch: int, image: np.ndarray) -> np.ndarray:
    sym, arg_params, aux_params = mx.model.load_checkpoint(model_prefix, epoch)
    model = mx.mod.Module(symbol=sym, context=ctx, label_names=[])
    arg_params["data"] = image
    model.bind(for_training=False, data_shapes=[("data", arg_params["data"].shape)])
    model.set_params(arg_params, aux_params, allow_missing=True)
    Batch = namedtuple("Batch", ["data"])
    model.forward(Batch([image]))
    return np.squeeze(model.get_outputs()[0].asnumpy())


def write_output(file_name: str, model_out: np.array):
    with open(file_name, 'w') as out:
        for i in range(len(model_out)):
            out.write(str(model_out[i]) + '\n')


def main():
    ctx = mx.cpu()
    image = image_preprocessing(config.image_name)
    model_out = model_output(ctx, config.model_prefix, 0, image)
    write_output(config.output_file_name, model_out)


if __name__ == "__main__":
    main()
