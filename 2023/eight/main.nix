# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./input;
  moves = stringToCharacters (head lines);
  maps = fold mergeAttrs {}
    (map 
      (line: let
        elems = getMatching "([A-Z]{3})" line;
      in {
        ${head elems} = {
          L = elemAt elems 1;
          R = elemAt elems 2;
        };
      })
      (tail lines));
  getStep = i: elemAt moves (mod i (length moves));
  nStepsToZ = i: cur:
    if cur == "ZZZ"
    then i
    else nStepsToZ (i+1) maps.${cur}.${getStep i};
  result = nStepsToZ 0 "AAA";
in
  result
