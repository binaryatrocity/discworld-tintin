#!/usr/bin/env bash
set -euo pipefail

# Directory where this script lives
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

discworld_file="$script_dir/Discworld"

# Ensure the Discworld file exists
if [ ! -f "$discworld_file" ]; then
  echo "Error: '$discworld_file' not found."
  exit 1
fi

# Escape characters that might confuse sed (& and |)
escaped_dir=$(printf '%s\n' "$script_dir" | sed 's/[&|]/\\&/g')

# Replace "PACKAGE_DIRECTORY" on the second line with the full path
sed -i "2s|PACKAGE_DIRECTORY|$escaped_dir|" "$discworld_file"

# Create (or overwrite) the symlink in /usr/local/bin
sudo ln -sf "$discworld_file" /usr/local/bin/disc

echo "The discworld-tintin package is installed, you can now type 'disc' from anywhere to connect"
