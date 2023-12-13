# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./input;
  moves = stringToCharacters (head lines);
  maps = fold mergeAttrs {}
    (map 
      (line: let
        elems = getMatching "([A-Z0-9]{3})" line;
      in {
        ${head elems} = {
          L = elemAt elems 1;
          R = elemAt elems 2;
        };
      })
      (tail lines));
  getStep = i: elemAt moves (mod i (length moves));
  starts = filter (str: match "[A-Z0-9]{2}A" str != null) (attrNames maps);
  isEnd = node: match "[A-Z0-9]{2}Z" node != null;
  nextStep = i: node: maps.${node}.${getStep i};
  getNSteps = i: nodes: if all isEnd nodes
    then i
    else getNSteps (i+1) (map (nextStep i) nodes);
  iterations = genericClosure {
      startSet = [{key=0; nodes=starts; final=false;}];
      operator = item: let final = traceIf (all isEnd item.nodes) "fine!!" (all isEnd item.nodes); in
      if item.final
      then []
      else [ {
          key = item.key+1;
          nodes = map (nextStep item.key) item.nodes;
          inherit final;
      }];
  };
  result = (head (filter (x: x.final) iterations)).key -1;
in
  result
