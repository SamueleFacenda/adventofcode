# run with 'nix-instantiate --eval main.nix'
let 
  lib = (builtins.getFlake "nixpkgs").legacyPackages.${builtins.currentSystem}.lib;
  inherit (builtins) readFile map filter isInt head match stringLength split;
  inherit (lib.strings) splitString toInt stringToCharacters;
  inherit (lib.lists) fold last;
  inherit (lib) traceVal;
  fileLines = file: filter
                      (str: (stringLength str)>0)
                      (splitString "\n" (readFile ./input)));
in
fold (a: b: (first a) +b) 0
  (filter
    (line: all
      (draw: draw.red <= 12 && draw.green <= 13 && draw.blue <= 14)
      (tail line)) # first element is id
    (map
      (x: (
        map
          (groups: )
          (split "(?:Game ([0-9]+):)|(?: ([0-9]+) (red|blue|green),?(;)?)" x)
      ))
      (fileLines ./inputtest))
