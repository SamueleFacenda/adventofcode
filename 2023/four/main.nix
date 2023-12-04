# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./inputtest;
  rawToScratchCard = row: 
    let
      numsAndSep = flatten (filter isList (split "([0-9]+|\\|)" row));
      id = head numsAndSep;
      splitted = splitList "|" (tail numsAndSep);
      winning = head splitted;
      nums = last splitted;
    in
      { inherit id winning nums; };
  scratchcards = map rawToScratchCard lines;
  countWinnings = {winning, nums, ...} :
    length (intersectLists winning nums);
  guesses = map countWinnings scratchcards;
  
in
  guesses
