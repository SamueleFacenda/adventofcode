# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./input;
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
  countWinnings = {winning, nums, ...}: length (intersectLists winning nums);
  scratchWins = id: 
    listToAttrs (
      map 
        (idcard: nameValuePair (toString idcard) 1)
        (range id (countWinnings (elemAt scratchcards id))));
  wins = id: countWinnings (elemAt scratchcards id);
  getTotalCard = {cardSet, out ? 0, i ? 1}:
    if ! cardSet ? "${(toString i)}"
    then out
    else 
      let
        winCount = wins (i -1);
        prev = cardSet."${(toString i)}";
      in getTotalCard {
        i = i+1;
        out = out + prev;# there is one scratccard by default
        cardSet = cardSet // (
          genAttrs
            (map toString (range (i+1) (i+winCount)))
            (id: cardSet."${(toString id)}" + prev)# old plus wins
        );
      };
  result = getTotalCard {cardSet=(genAttrs (map ({id, ...}: toString id) scratchcards) (const 1));};
in
  result
