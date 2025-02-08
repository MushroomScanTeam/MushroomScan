# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 20:02:32 2025

@author: filip
"""

from onnx2tf import convert

# Path to your ONNX model
input_onnx_file_path = "model.onnx"

# Where to place the converted files
output_folder_path = "converted_model"

# Run the conversion
convert(
    input_onnx_file_path=input_onnx_file_path,
    output_folder_path=output_folder_path,
    output_signaturedefs=True  # If you need signature defs in SavedModel
)

print("Conversion completed!")
