upstream=$(curl -s https://api.github.com/repos/zen-browser/desktop/releases/latest | jq -r '.tag_name')
local=$(cat ./flake.nix | grep -oP 'version = "\K[^"]+')

if [ "$upstream" != "$local" ]; then
  echo "new_version=true" >> $GITHUB_OUTPUT
fi

echo "$upstream"
