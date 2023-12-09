# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./input;
  spl = map (splitString " ") lines;
  score = hand: let ord = sort (a: b: a > b) (attrValues hand); in
    if head ord == 5
      then 7
    else if head ord == 4
      then 6
    else if head ord == 3 && elemAt ord 1 == 2
      then 5
    else if head ord == 3
      then 4
    else if head ord == 2 && elemAt ord 1 == 2
      then 3
    else if head ord == 2
      then 2
    else 
      1;
  parseHand = str:
    let
      chrs = stringToCharacters str;
      counts = listToAttrs (
        map 
          (ch: {name = ch; value = count (x: x==ch) chrs;})
          (unique chrs));
    in {
      base = str;
      score = score counts;
    };
  hands = zipListsWith
    (hand: value: parseHand hand // {inherit value;})
    (map head spl)
    (map last spl);
  isSmallerHand = a: b:
    if a.score != b.score
    then a.score < b.score
    else compareHands a.base b.base < 0;
  cardToVal = chr: if chr == "A" then 14
    else if chr == "K" then 13
    else if chr == "Q" then 12
    else if chr == "J" then 11
    else if chr == "T" then 10
    else toInt chr;
  compareCardLists = compareLists (a: b: cardToVal a - cardToVal b);
  compareHands = a: b: compareCardLists (stringToCharacters a) (stringToCharacters b);
  sorted = sort isSmallerHand hands;
  result = sum (imap1 (i: {value,...}: i* toInt value) sorted);
in
  result
