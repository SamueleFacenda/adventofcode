# run with 'nix-instantiate --eval main.nix'
let 
  lib = (builtins.getFlake "nixpkgs").legacyPackages.${builtins.currentSystem}.lib;
  inherit (builtins) readFile map filter isInt head match stringLength;
  inherit (lib.strings) splitString toInt stringToCharacters;
  inherit (lib.lists) fold last;
  inherit (lib) traceVal;
in
fold (a: b: a+b) 0
  (map
    (x: (
      let
        nums = (filter
          (ch: (match "^[0-9]$" ch) != null)
          (stringToCharacters x));
      in (toInt (head nums))*10 + (toInt (last nums))
    ))
    (filter
      (str: (stringLength str)>0)
      (splitString
        "\n"
        (readFile ./input))))
  
