#!/bin/bash
cd to-send-9

for dir in */; do
  dir=${dir%/}
  tar -czvf "${dir}.tar.gz" -C "$dir" .
done

echo "Archives created successfully."
