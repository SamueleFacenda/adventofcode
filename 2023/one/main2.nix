# run with 'nix-instantiate --eval main.nix'
let 
  lib = (builtins.getFlake "nixpkgs").legacyPackages.${builtins.currentSystem}.lib;
  inherit (builtins) readFile map filter isInt head match stringLength replaceStrings;
  inherit (lib.strings) splitString toInt stringToCharacters;
  inherit (lib.lists) fold last zipLists;
  inherit (lib) traceVal traceValFn;
  # apply the replace every time to the result of the previous, not in one run like default
  replaceStringsIterative = from: to: str: 
    fold
      (cur: prev: replaceStrings
        [cur.fst]
        [cur.snd]
        prev )
      str
      (zipLists from to);
in
# sum list
fold (a: b: a+b) 0
  # line to number
  (map
    (line:
      let
        nums = (filter
          # is digit
          (ch: (match "^[0-9]$" ch) != null)
          (stringToCharacters 
            (replaceStringsIterative
              [ "one" "two" "three" "four" "five" "six" "seven" "eight" "nine" ]
              # numbers can share digits if they are adiacent
              [ "one1one" "two2two" "three3three" "four4four" "five5five" "six6six" "seven7seven" "eight8eight" "nine9nine" ]
              line )));
      in (toInt (head nums))*10 + (toInt (last nums))
    )
    # all the lines
    (filter
      (str: (stringLength str)>0)
      (splitString
        "\n"
        (readFile ./input))))
  
