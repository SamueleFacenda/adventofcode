# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./inputtest;
  matrix = map stringToCharacters lines;
  isSymbol = chr: (match "[0-9\\.]" chr) == null;
  # boolean map of symbols
  symbol = map (map isSymbol) matrix;
  isAdiacent = row: col: fold 
    (cur: prev: prev || (
      let 
        x = row+cur.x;
        y = col+cur.y;
      in
      x >= 0 &&
      x < (length (head symbol)) &&
      y >= 0 &&
      y < (length symbol) &&
      elemAt x (elemAt y symbol)
    ))
    false 
    (cartesianProductOfSets {x=[-1 0 1];y=[-1 0 1];});
  adiacents = imap0 (rowi: val: imap0 (coli: v: isAdiacent rowi coli) val) matrix;
  isValidNum = y: x: x >= 0 && x < (length (head adiacents)) &&
    # is adiacent or, if is a number, left and right are good numbers (recursive)
    (elemAt x (elemAt y symbol) || 
    ((match "[0-9]" (elemAt x (elemAt y matrix))) != null && (
      isValidNum y (x+1) || isValidNum y (x-1)
    ))
    );
  validNums = imap0 (rowi: val: imap0 (coli: v: isValidNum rowi coli) val) matrix;
in
  inherit result;
