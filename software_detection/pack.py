import os
import tarfile

# Define the product details
product_name = "wireguard"
distribution_type = "official_packages"
operating_system = "debian_12"

# Define the directory and archive names
directory_name = f"{product_name}_from_{distribution_type}_on_{operating_system}"
archive_name = f"{directory_name}.tar.gz"

# Create the directory
os.makedirs(directory_name, exist_ok=True)

# Paths to the files to be included in the archive
files_to_include = [
  "/path/to/detect.py",
  "/path/to/oval_vars.xml.j2",
  "/path/to/requirements.txt"
]

# Copy the files to the new directory
for file_path in files_to_include:
  os.system(f"cp {file_path} {directory_name}/")

# Create the tar.gz archive
with tarfile.open(archive_name, "w:gz") as tar:
  tar.add(directory_name, arcname=os.path.basename(directory_name))

print(f"Archive {archive_name} created successfully.")
