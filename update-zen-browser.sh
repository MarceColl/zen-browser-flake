#!/usr/bin/env bash

upstream=$(./new-version.sh | tee version)

echo "Updating to $upstream"

baseUrl="https://github.com/zen-browser/desktop/releases/download/$upstream"

# Modiyf with sed the nix file
sed -i "s/version = \".*\"/version = \"$upstream\"/" ./flake.nix

# Update the hash specific.sha256
specfic=$(nix-prefetch-url --type sha256 --unpack $baseUrl/zen.linux-specific.tar.bz2)
sed -i "s/specific.sha256 = \".*\"/specific.sha256 = \"$specfic\"/" ./flake.nix

# Update the hash generic.sha256
generic=$(nix-prefetch-url --type sha256 --unpack $baseUrl/zen.linux-generic.tar.bz2)
sed -i "s/generic.sha256 = \".*\"/generic.sha256 = \"$generic\"/" ./flake.nix

nix flake update
nix build
