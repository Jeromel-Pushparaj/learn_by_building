# Importing Required Modules
# from rembg import remove
# from PIL import Image
#
# # Store path of the image in the variable input_path
# input_path = str(input("Enter the path: "))
#
# # Store path of the output image in the variable output_path
# file_type = input_path[-4:]
# if file_type == ".jpg" or ".png" or "jpeg":
#     output_path = input_path[:-4] + "_rbg.png"
#     # Processing the image
#     input = Image.open(input_path)
#
#     # Removing the background from the given Image
#     output = remove(input)
#
#     # Saving the image in the given path
#     output.save(output_path)
# else:
#     print("Invalid Image! - it's support only .jpg or .png")
