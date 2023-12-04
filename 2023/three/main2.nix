# run with 'nix-instantiate --eval main.nix'

# metto il numero in ogni cella del numero
# per ogni gear, guardo i vicini, se sono numeri li aggiungo alla lista
# ritorno il prodotto della lista (modo per mappare la matrice)
with (import ../lib);
let
  lines = fileLines ./input;
  matrix = map stringToCharacters lines;
  ylen = length matrix;
  xlen = length (head matrix);
  mxAt = mx: y: x: elemAt (elemAt mx y) x;

  isSymbol = chr: (match "\\*" chr) != null;
  # boolean map of symbols
  symbol = map (map isSymbol) matrix;

  # map the matrix cells: if they are a number sum the cell val to the left cell val*10 (recursive)
  # blocks when reachs the left side (return null) or a non-integer cell (return null)
  buildNum = y: x: if x < 0 then 0 else
  (
    let
      val = mxAt matrix y x;
    in
    if match "[0-9]" val == null
    then 0
    else (buildNum y (x - 1)) * 10 + (toInt val)
  );
  completeNums = imap0 (rowi: row: imap0 (coli: v: buildNum rowi coli) row) matrix;

  # copy the num in all the num cells
  # every num is the max of himself and the right cell (recursive)
  expandNum = y: x:
    if x >= xlen || mxAt completeNums y x == 0
    then 0
    else max (mxAt completeNums y x) (expandNum y (x + 1));
  expanded = imap0 (rowi: row: imap0 (coli: v: expandNum rowi coli) row) completeNums;

  # not really right, if two numbers on the same gear are equals, the gear is discarded
  # anyway, it works.
  gearRatio = row: col: val:
    if val != "*" then 0
    else
      let
        nearNums = fold
          # test, numbers are not equals
          (cur: prev:
            let
              x = col + cur.x;
              y = row + cur.y;
            in
            if
              x >= 0 &&
              x < xlen &&
              y >= 0 &&
              y < ylen
            then prev ++ [ (mxAt expanded y x) ]
            else prev
          )
          [ ]
          (cartesianProductOfSets { x = [ (-1) 0 1 ]; y = [ (-1) 0 1 ]; });
        validNears = subtractLists [ 0 ] (unique nearNums);
      in
      if length validNears != 2 then 0
      else fold (a: b: a * b) 1 validNears;


  finalMatrix = imap0 (rowi: row: imap0 (gearRatio rowi) row) matrix;

  result = fold (cur: prev: (sum cur) + prev) 0 finalMatrix;
in
result
