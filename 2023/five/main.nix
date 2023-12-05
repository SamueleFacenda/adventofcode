# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./input;
  seeds = getNums (head lines);
  parseRange = line:
    let
      nums = getNums line;
    in rec {
      start = elemAt nums 1;
      end = start + last nums;
      offset = head nums - start;
    };
  parseMapTitle = getMatching "(seed|soil|fertilizer|water|light|temperature|humidity|location)";
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
    then v
    else (
      let cur = elemAt ranges i; in
      if v >= cur.start && v < cur.end
      then v + cur.offset
      else mapWithMaps v ranges (i+1)
    );
  mapVal = {v, type ? "seed"}: 
    #if ! hasAttr type maps
    if type == "location"
    then v
    else mapVal 
      {v = mapWithMaps v maps."${type}".maps 0;
      type = maps."${type}".dest;};
  result = minVal (map (x: mapVal {v=x;}) seeds);
in
  result
