import shutil
from file_strategies import CompressedReusableFile, PlainFile
from path_manager import ManagePath


def compress():
    managed_path = ManagePath(path)
    all_dir_items = managed_path.all_names_in_path()
    name = input('file name')
    for name in all_dir_items:
        if name == input_name:
            file_obj = PlainFile(os.path.join(path, name))

    CompressedReusableFile(f"{file_obj.file_name}.txt.gz", 'w').compress()


def main():
    managed_path = ManagePath(path)
    all_dir_items = managed_path.all_names_in_path()

    for name in all_dir_items:
        if name == input_name:
            file_obj = CompressedReusableFile(os.path.join(path, name))
    decompressed_buffer_item = file_obj.decompress()

    with open(f"{file_obj.file_name}.txt", 'w') as decompressed_file:
        shutil.copyfileobj(decompressed_buffer_item, decompressed_file)

        decompress_file_obj = PlainFile(decompressed_file)

if '__main__' == __name__:
    main()