# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./input;
  assembleNum = str: toInt (concatStrings (filter (c: match "[0-9]" c != null) (stringToCharacters str)));
  time = assembleNum (head lines);
  record = assembleNum (last lines);
  # it's a basic 2^d grade equations, but nix doesn't have a sqrt function
  # so I think I have to implement it
  sqrt = n: 
    let
      precision = 0.001;
      tenLowerThanN = l: if 100 * l * l < n then tenLowerThanN (l*10) else l;
      tenHigherThanN = h: if 0.01 * h * h > n then tenHigherThanN (h*0.1) else h;
      lo = tenLowerThanN 1;
      hi = tenHigherThanN n;
      binSearch = lo: hi:
        let mid = (lo + hi) / 2; in
        if abs (mid * mid - n) < precision
        then mid
        else if mid * mid > n
        then binSearch lo mid
        else binSearch mid hi;
    in
      binSearch lo hi;
  delta = sqrt  (time * time - 4 * record);
  left = ceil ((time - delta) / 2);
  right = floor ((time + delta) / 2);
  result = right - left + 1;
in
  result
