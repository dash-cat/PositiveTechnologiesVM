#!/bin/bash

# Change to the to-send-2 directory
cd to-send-2

# Loop through each directory in to-send-2
for dir in */; do
  # Remove the trailing slash
  dir=${dir%/}
  # Create a tar.gz archive with the same name as the directory
  tar -czvf "${dir}.tar.gz" -C "$dir" .
done

echo "Archives created successfully."