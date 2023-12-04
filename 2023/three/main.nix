# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./input;
  matrix = map stringToCharacters lines;
  ylen = length matrix;
  xlen = length (head matrix);
  mxAt = mx: y: x: elemAt (elemAt mx y) x;

  isSymbol = chr: (match "[0-9\\.]" chr) == null;
  # boolean map of symbols
  symbol = map (map isSymbol) matrix;

  isAdiacent = row: col: fold
    (cur: prev: prev || (
      let
        x = col + cur.x;
        y = row + cur.y;
      in
      x >= 0 &&
        x < xlen &&
        y >= 0 &&
        y < ylen &&
        mxAt symbol y x
    ))
    false
    (cartesianProductOfSets { x = [ (-1) 0 1 ]; y = [ (-1) 0 1 ]; });
  # boolean map of adiacent to symbol
  adiacents = imap0 (rowi: row: imap0 (coli: v: isAdiacent rowi coli) row) matrix;

  # recursex: 0 if left and right, 1/-1 for right/left
  # int -> int -> int -> bool
  isValidNum = y: x: recursex: x >= 0 && x < xlen &&
    # is a number and, or is adiancent or left or right are good (recursive)
    (match "[0-9]" (mxAt matrix y x) != null &&
      (mxAt adiacents y x ||
        (
          let
            # list of side to check (numbers to add to x)
            sidelist = if recursex == 0 then [ 1 (-1) ] else [ recursex ];
          in
          fold (side: prev: prev || isValidNum y (x + side) side) false sidelist
        ))
    );
  validNums = imap0 (rowi: row: imap0 (coli: v: isValidNum rowi coli 0) row) matrix;

  # map the matrix cells: if they are a number sum the cell val to the left cell val*10 (recursive)
  # blocks when reachs the left side (return null) or a non-integer cell (return null)
  buildNum = y: x: if x < 0 then null else
  (
    let
      val = mxAt matrix y x;
    in
    if match "[0-9]" val == null
    then null
    else
      let
        left = buildNum y (x - 1);
        numl = if left == null then 0 else left;
      in
      numl * 10 + (toInt val)
  );
  completeNums = imap0 (rowi: row: imap0 (coli: v: buildNum rowi coli) row) matrix;

  # map the completeNums matrix to keep only the right value of a series of num
  getValid = val: y: x:
    if
      val != null &&
      (x == xlen - 1 || mxAt completeNums y (x + 1) == null) && # is the first chr of a num (end line or right is null)
      mxAt validNums y x# is adiacent
    then val else 0;
  finalMatrix = imap0 (rowi: row: imap0 (coli: v: getValid v rowi coli) row) completeNums;

  result = fold (cur: prev: (fold (a: b: a + b) 0 cur) + prev) 0 finalMatrix;
in
result
