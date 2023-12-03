# run with 'nix-instantiate --eval main.nix'
with (import ../lib);
# sum indexes
fold (a: b: (traceVal (head a)) + b) 0
  # get only valid lines
  (filter
    (line: all
      (draw:
      (attrByPath [ "red" ] 0 draw) <= 12 &&
      (attrByPath [ "green" ] 0 draw) <= 13 &&
      (attrByPath [ "blue" ] 0 draw) <= 14)
      
      (tail line)) # first element is id
    # convert lines to [id {blue=12} {red=15;blue=0;}]
    (map
      # x: every row
      (x:
      let
        # raw text to [id num color ; ...]
        groups = flatten (filter isList (split "([0-9]+|red|green|blue|;)" x));
      in
      # [id num color num color ; num color ; num color] -> [id {color=num} {color=num;color=num}]
      [ (toInt (head groups)) ] ++ # first element is id
        # [[num color] [num color num color]] -> [{color=num}...]
      (map
        # [num color num color] -> {color=num;color=num}
        (group: (listToAttrs
          (zipListsWith
            nameValuePair
            (filter (x: (match "^[0-9]+$" x) == null) group)
            (map toInt (filter (x: (match "^[0-9]+$" x) != null) group)))))
        # [id num color ; num color num color] -> [[num color] [num color num color]]
        (splitList ";" (tail groups))))

      (fileLines ./inputtest)))
