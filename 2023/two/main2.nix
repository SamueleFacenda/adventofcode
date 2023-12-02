# run with 'nix-instantiate --eval main.nix'
let
  lib = (builtins.getFlake "nixpkgs").legacyPackages.${builtins.currentSystem}.lib;
  inherit (builtins) readFile map filter isInt head match stringLength split isList listToAttrs tail all toString;
  inherit (lib.strings) splitString toInt stringToCharacters;
  inherit (lib.lists) fold last flatten zipListsWith;
  inherit (lib.attrsets) nameValuePair attrByPath catAttrs;
  inherit (lib.debug) traceVal traceValFn;
  inherit (lib.trivial) max;
  fileLines = file: filter
    (str: (stringLength str) > 0)
    (splitString "\n" (readFile file));
  # return a list of lists
  splitList = split: list: fold
    (cur: prev:
      if cur == split
      then [ [ ] ] ++ prev
      else [ ((head prev) ++ [ cur ]) ] ++ (tail prev)) # append to first list
    [ [ ] ]
    list;
in
# sum all the values
fold (a: b: a + b) 0
  # map line to minimum power
  (map
    # line: [{color=num} {color=num;color=num}]
    (line:
    let
      getMaxAttr = attr: let attrs = catAttrs attr line; in fold max (head attrs) attrs;
    in
    (getMaxAttr "blue") * (getMaxAttr "red") * (getMaxAttr "green"))

    # convert lines to [{blue=12} {red=15;blue=0;}]
    (map
      (row:
      # [[num color] [num color num color]] -> [{color=num}...]
      (map
        # [num color num color] -> {color=num;color=num}
        (group: (listToAttrs
          (zipListsWith
            nameValuePair
            (filter (x: (match "^[0-9]+$" x) == null) group)
            (map toInt (filter (x: (match "^[0-9]+$" x) != null) group)))))
        # [num color ; num color num color] -> [[num color] [num color num color]]
        (splitList ";"
          (tail # remove id
            (flatten # get ["id" "num" "color" ";" ...]
              (filter isList
                # text to [["id"] "something" ["num"] ["color"] ...]
                (split "([0-9]+|red|green|blue|;)" row)))))))

      (fileLines ./input)))
