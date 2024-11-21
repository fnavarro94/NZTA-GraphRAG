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

# Define the patch mappings
files_to_patch = {
    "patch_files/graph_stores_types.py": os.path.join(site_packages_path, "llama_index", "core", "graph_stores", "types.py"),
    "patch_files/Neo4j_property_graph_node_retrieval_patch.py": os.path.join(site_packages_path, "llama_index", "graph_stores", "neo4j", "neo4j_property_graph.py"),
    "patch_files/property_graph_base.py": os.path.join(site_packages_path, "llama_index", "core", "indices", "property_graph", "base.py"),
    "patch_files/sub_retrievers_base.py": os.path.join(site_packages_path, "llama_index", "core", "indices", "property_graph", "sub_retrievers", "base.py"),
    "patch_files/sub_retrievers_vector.py": os.path.join(site_packages_path, "llama_index", "core", "indices", "property_graph", "sub_retrievers", "vector.py"),
}

# Iterate over each file and apply patches
for patch_file, original_file_path in files_to_patch.items():
    backup_file_path = original_file_path + "_backup"

    # Check if the original file exists
    if not os.path.exists(original_file_path):
        print(f"Error: Original file not found at {original_file_path}")
        continue

    # Check if the patch file exists
    if not os.path.exists(patch_file):
        print(f"Error: Patch file not found at {patch_file}")
        continue

    try:
        # Backup the original file if the backup does not already exist
        if not os.path.exists(backup_file_path):
            print(f"Backing up the original file: {original_file_path}")
            shutil.copy2(original_file_path, backup_file_path)
            print(f"Backup created at {backup_file_path}")
        else:
            print(f"Backup already exists: {backup_file_path}")

        # Replace the original file with the patched file
        print(f"Applying the patch from {patch_file} to {original_file_path}...")
        shutil.copy2(patch_file, original_file_path)
        print("Patch applied successfully!")

    except Exception as e:
        print(f"Error during patching {original_file_path}: {e}")
