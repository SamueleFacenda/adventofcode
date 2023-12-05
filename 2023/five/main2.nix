# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./input;
  seeds = getNums (head lines);
  seedRanges = zipListsWith
    (start: span: {inherit start; end = start + span -1;})
    (getStepped 2 0 seeds)
    (getStepped 2 1 seeds);
  parseRange = line:
    let
      nums = getNums line;
    in rec {
      start = elemAt nums 1;
      end = start + last nums -1;
      offset = head nums - start;
    };
  parseMapTitle = getMatching "(seed|soil|fertilizer|water|light|temperature|humidity|location)";
  applyRange = range: val: mapAttrs (n: v: v + range.offset) val;
  parseMaps = i: mapSet: curPath:
    if i == length lines
    then mapSet
    else (
      let curLine = elemAt lines i; in
      if match ".*map.*" curLine != null
      then
        let 
          newPath = parseMapTitle curLine; 
          from = head newPath;
          dest = last newPath;
        in 
        parseMaps 
          (i+1) 
          (mapSet // setAttrByPath [from] {inherit dest; maps = [];})
          ([from "maps"])
      else
        parseMaps 
          (i+1)
          (mapAttrPath curPath (concat [(parseRange curLine)]) mapSet)
          curPath
    );
  # start i = 1 because of the seeds on the first line
  maps = parseMaps 1 {} null;
  mapWithMaps = v: ranges: i: 
    if i == length ranges
    then [v]
    else (
      # divide a input range in more subrange if needed
      let cur = elemAt ranges i; in
      if cur.start <= v.start && v.end <= cur.end # completely inside
        then 
          [(applyRange cur v)]
        else if v.end < cur.start || cur.end < v.start # completely outside
        then 
          mapWithMaps v ranges (i+1)
        else if v.start < cur.start && cur.end < v.end # range inside value
        then 
          mapWithMaps {inherit (v) start; end = cur.start -1;} ranges (i+1) ++
          [(applyRange cur {inherit (cur) start end;})] ++
          mapWithMaps {start = cur.end+1; inherit (v) end;} ranges (i+1)
        else if v.start < cur.start # halway left
        then 
          mapWithMaps {inherit (v) start; end = cur.start -1;} ranges (i+1) ++
          [(applyRange cur {inherit (cur) start; inherit (v) end;})]
        else # halfway right
          [(applyRange cur {inherit (v) start; inherit (cur) end;})] ++
          mapWithMaps {start = cur.end+1; inherit (v) end;} ranges (i+1)
    );
  mapVal = {v, type ? "seed"}: 
    #if ! hasAttr type maps
    if type == "location"
    then v
    else mapVal 
      # input: a list of ranges: output: flattened list of lists of ranges
      {v = flatten(map (x: mapWithMaps x maps.${type}.maps 0) v);
      type = maps.${type}.dest;};
  result = minVal  (map (x: x.start) (mapVal {v=seedRanges;}));
in
  deepSeq seedRanges result
