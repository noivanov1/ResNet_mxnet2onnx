# MXNet inference
image_name = 'photo.bmp'
image_resize_to = [112, 112]
mxnet_model_prefix = 'model_mxnet/model'
output_file_name = 'mxnet_inference.txt'

# Conversion MXNet to ONNX
onnx_model_name = 'model_onnx/converted_model.onnx'
mxnet2onnx_log = 'mxnet2onnx_log.txt'
conversion_input_size = [1, 3, 112, 112]

# ONNX inference
