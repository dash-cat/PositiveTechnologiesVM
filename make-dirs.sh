#!/bin/bash

# Array of input JSON files
input_files=(
    "../data/gitea_from_binary_on_debian.json"
    "../data/icinga_from_official_repo_on_debian.json"
    "../data/moodle_from_source_on_debian12.json"
    "../data/nexus_from_tar_on_debian12.json"
    "../data/xwiki_from_zip_on_debian.json"
)

# Loop through each input file and generate the corresponding commands
for file in "${input_files[@]}"; 
do
    # Extract the base name without the extension and directory
    base_name=$(basename "$file" .json)
    
    mkdir -p to-send-6/stage1_${base_name}
    mkdir -p to-send-6/stage2_${base_name}
    mkdir -p to-send-6/stage3_${base_name}
done
