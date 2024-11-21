import os
import shutil
import sys

# Define paths
venv_path = os.getenv("VIRTUAL_ENV")

if not venv_path:
    print("Error: Virtual environment is not activated.")
    sys.exit(1)

# Determine the site-packages path based on the OS
if os.name == "nt":  # Windows
    site_packages_path = os.path.join(venv_path, "Lib", "site-packages")
else:  # macOS/Linux
    site_packages_path = os.path.join(venv_path, "lib", "python3.11", "site-packages")

# Define the files and their original locations
files_to_revert = {
    os.path.join(site_packages_path, "llama_index", "core", "graph_stores", "types.py"),
    os.path.join(site_packages_path, "llama_index", "graph_stores", "neo4j", "neo4j_property_graph.py"),
    os.path.join(site_packages_path, "llama_index", "core", "indices", "property_graph", "base.py"),
    os.path.join(site_packages_path, "llama_index", "core", "indices", "property_graph", "sub_retrievers", "base.py"),
    os.path.join(site_packages_path, "llama_index", "core", "indices", "property_graph", "sub_retrievers", "vector.py"),
}

# Iterate over each file and revert them using the backup
for original_file_path in files_to_revert:
    backup_file_path = original_file_path + "_backup"

    # Check if the backup file exists
    if not os.path.exists(backup_file_path):
        print(f"Error: Backup file not found for {original_file_path}")
        continue

    try:
        # Restore the original file from the backup
        print(f"Reverting {original_file_path} to its original version...")
        shutil.copy2(backup_file_path, original_file_path)
        print(f"Reverted {original_file_path} successfully!")

    except Exception as e:
        print(f"Error during reverting {original_file_path}: {e}")
