import os

def find_libpython38(root_dir="/"):
    libpython_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "libpython3.8.so.1.0":
                libpython_files.append(os.path.join(root, file))
    return libpython_files

# if __name__ == "__main__":
if __name__ == "__main__":
    libpython_files = find_libpython38()
    if libpython_files:
        print("Found the following libpython3.8.so.1.0 files:")
        for file_path in libpython_files:
            print(file_path)
    else:
        print("No libpython3.8.so.1.0 files found on the system.")
