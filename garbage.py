import psutil, numpy, cv2, os 
from PIL import Image 
from typing import *

def dump_garbage_to_disk(directory : str) -> None: 

    def generate_string(string_length : int) -> str:
        return "".join(
            chr(int(ascii_code)) for ascii_code in 
                numpy.random.randint(65, 91, (string_length, ), dtype = numpy.int32)
        )

    def create_folder(folder_name : str) -> str:
        if not (os.path.exists(folder_name)):
            os.makedirs(folder_name)
        return folder_name 

    def save_image(image_name : str, target_image : numpy.ndarray) -> bool:
        try:
            Image.fromarray(target_image).save(image_name, compress_level = 0)
        except (PermissionError, IOError, OSError):
            return False 
        return True 

    def remaining_disk_space(folder_name : str) -> int:
        return psutil.disk_usage(folder_name).free 

    def dump_random_chunk(filename : str, image_shape : Tuple[ int, int, int ]) -> bool:
        random_image = numpy.random.randint(0, 256, image_shape, dtype = numpy.uint8)
        return save_image(filename, random_image)

    if not (os.path.exists(directory)):
        raise OSError(f"The specified directory does not exist: \"{directory}\"")

    garbage_folder = create_folder(os.path.join(directory, generate_string(25)))

    image_shape = [4096, 4096, 3]

    dim_index = 0

    counter = 1

    disk_size_length = len(str(remaining_disk_space(garbage_folder)))

    while ((image_shape[0] >= 2) and (image_shape[1] >= 2)):

        while (dump_random_chunk(os.path.join(
            garbage_folder, f"image_{counter}.png"), tuple(image_shape))
        ):

            shape_str = "({}, {}, 3)".format(
                str(image_shape[0]).rjust(4, ' '),
                str(image_shape[1]).rjust(4, ' ')
            )

            remaining_str = str(remaining_disk_space(garbage_folder)).rjust(disk_size_length, ' ')

            print(f"[ {shape_str} ] [ {remaining_str} ] [ {counter} ]")

            counter += 1

        image_shape[dim_index] = image_shape[dim_index] // 2

        dim_index = 1 - dim_index 

    os.system(f"rmdir /s /q \"{garbage_folder}\"")

    print("\n<< Free space have been successfully overwritten >>\n")

if (__name__ == "__main__"):

    target_directory = "B:/"

    dump_garbage_to_disk(target_directory)