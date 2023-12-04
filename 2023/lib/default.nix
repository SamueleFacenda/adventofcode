# utils to import
rec {
  lib = (builtins.getFlake "nixpkgs").legacyPackages.${builtins.currentSystem}.lib;
  inherit (builtins) readFile map filter isInt head match stringLength split isList listToAttrs tail all toString tryEval elemAt length;
  inherit (lib.strings) splitString toInt stringToCharacters fixedWidthNumber;
  inherit (lib.lists) fold last flatten zipListsWith imap0 subtractLists;
  inherit (lib.attrsets) nameValuePair attrByPath catAttrs cartesianProductOfSets;
  inherit (lib.debug) traceVal traceValFn;
  inherit (lib.trivial) max boolToString;
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
  sum = fold (a: b: a+b) 0;
  minAttr = list: attr: let attrs = catAttrs attr list; in fold max (head attrs) attrs;
  tryOrDefault = default: expr: let res = tryEval expr; in if res.success then res.value else default;
  traceBoolList = traceValFn (y: toString (map (x: if x then "#" else ".") y));
  traceBoolListPrefixed = pre: traceValFn (y: toString ([pre] ++ (map (x: if x then "#" else ".") y)));
}
