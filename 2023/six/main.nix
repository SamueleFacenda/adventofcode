# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
let
  lines = fileLines ./inputtest;
  times = getNums (head lines);
  records = getNums (last lines);
  calcNGoodsWrapped = time: record: timePush:
    if timePush == time
    then 
      0
    else 
      (if timePush * (time - timePush) > record then 1 else 0) + 
      calcNGoodsWrapped time record (timePush+1);
  calcNGoods = time: record: calcNGoodsWrapped time record 0;
  goods = zipListsWith calcNGoods times records;
  result = fold (a: b: a*b) 1 goods;
in
  result
