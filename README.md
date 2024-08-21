# Zen Browser

This is a flake for the Zen browser.

Just add it to your NixOS `flake.nix` or home-manager:

```nix
inputs = {
  zen-browser.url = "github:MarceColl/zen-browser-flake";
  ...
}
```

Then in the `configuration.nix` in the `environment.systemPackages` add

```nix
inputs.zen-browser."${system}".default
```

```shell
$ sudo nixos-rebuild switch
$ zen
```
