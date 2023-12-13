# utils to import
rec {
  lib = (builtins.getFlake "nixpkgs").legacyPackages.${builtins.currentSystem}.lib;
  inherit (builtins) attrValues floor ceil trace mapAttrs hasAttr deepSeq readFile map filter isInt head match stringLength split isList listToAttrs tail all toString tryEval elemAt length;
  inherit (lib.strings) splitString toInt stringToCharacters fixedWidthNumber concatStrings;
  inherit (lib.lists) compareLists imap1 count sort fold last flatten zipListsWith imap0 subtractLists unique intersectLists range drop;
  inherit (lib.attrsets) filterAttrs nameValuePair attrByPath catAttrs cartesianProductOfSets genAttrs setAttrByPath getAttrFromPath recursiveUpdate;
  inherit (lib.debug) traceVal traceValFn traceValSeq traceSeq traceValSeqFn;
  inherit (lib.trivial) max boolToString const concat min mod compare mergeAttrs;
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
  sum = fold add 0;
  maxAttr = list: attr: let attrs = catAttrs attr list; in fold max (head attrs) attrs;
  tryOrDefault = default: expr: let res = tryEval expr; in if res.success then res.value else default;
  traceBoolList = traceValFn (y: toString (map (x: if x then "#" else ".") y));
  traceBoolListPrefixed = pre: traceValFn (y: toString ([pre] ++ (map (x: if x then "#" else ".") y)));
  getNums = x: map toInt (getMatching "([0-9]+)" x);
  getMatching = regx: line:  flatten (filter isList (split regx line));
  mapAttrPath = path: op: set: recursiveUpdate set (setAttrByPath path (op (getAttrFromPath path set)));
  minVal = x: fold min (head x) x;
  getStepped = step: base: list: map (x: x.v) (filter (x: mod (x.i - base + step) step == 0) (imap0 (i: v: {inherit i v;}) list));
  add = a: b: a+b;
  abs = x: if x > 0 then x else -x;
}
