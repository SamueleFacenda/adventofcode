
import logging
from functools import wraps
from time import time
import re

def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            print(f"Total execution time: {end_ if end_ > 0 else 0} ms")
    return _time_it

logging.basicConfig(filename='aoc.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
logging.info('Start of program')

class Valve():
    def __init__(self, name, flow_rate:int, connections):
        self.name = name
        self.flow_rate = flow_rate
        self.connections = connections

    def __repr__(self) -> str:
        return f"Valve('{self.name}', {self.flow_rate}, {self.connections})"

    def __eq__(self, __o: object) -> bool:
        return (self.name == __o.name 
                and self.flow_rate == __o.flow_rate 
                and self.connections == __o.connections)


@measure
def parse():
    """Parse input."""
    store_dict = {}
    # valves = []
    prog = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); '
                      r'tunnels? leads? to valves? ((([A-Z]{2}), )*([A-Z]{2}))')
    with open('input', 'r') as f:

        for line in f:
            line = line.strip()
            match = prog.match(line)
            if match:
                name = match.group(1)
                flow_rate = int(match.group(2))
                connections = set(match.group(3).split(', '))
                valve = Valve(name, flow_rate, connections)
                # valves.append(valve)
                store_dict[name] = valve
    logging.debug(store_dict)
    steps = {x:{y:1 if y in store_dict[x].connections else float('inf') for y in store_dict} for x in store_dict}
    logging.debug('Before Floyd-Warshall')
    for start in steps:
        logging.debug(f'{start}: {steps[start]}')
    # Floyd-Warshall Algorithm for steps between nodes (valves)
    for k in steps:
        for i in steps:
            for j in steps:
                steps[i][j] = min(steps[i][j], steps[i][k] + steps[k][j])
    logging.debug('After Floyd-Warshall')
    for start in steps:
        logging.debug(f'{start}: {steps[start]}')

    # logging.debug(valves)
    return store_dict, steps #, valves

def traveling_elf(valves, steps, last_valve, time_remaining, state_machine, state, flow, answer):
    # if opened_valves is None:
    #     opened_valves = set()
    answer[state] = max(answer.get(state,0), flow)
    for valve in valves:
        minutes = time_remaining - steps[last_valve][valve] - 1
        # Bitmasking for state. Each bit represents valve
        if (state_machine[valve] & state) or (minutes <=0):
            continue
        #recursion - add this valve to the state. Add this valve to the flow
        traveling_elf(valves, steps, valve, minutes, state_machine, 
                      state | state_machine[valve], 
                      flow + (minutes * valves[valve].flow_rate), 
                      answer)
    logging.debug(f'In recursion: {answer}')
    return answer


@measure
def part1(parsed_data):
    valve_dict, steps = parsed_data
    minutes = 30
    valves = {name:valve for (name,valve) in valve_dict.items() if valve.flow_rate > 0}
    state_machine = {v: 1<<i for i, v in enumerate(valves)}
    last_valve = 'AA'
    starting_state = 0
    starting_flow = 0
    total_flow = max(traveling_elf(valves, steps, last_valve, minutes, 
                                   state_machine, starting_state, starting_flow, 
                                   {}).values())
    return total_flow
    
@measure
def part2(parsed_data):
    valve_dict, steps = parsed_data
    minutes = 26
    valves = {name:valve for (name,valve) in valve_dict.items() if valve.flow_rate > 0}
    state_machine = {v: 1<<i for i, v in enumerate(valves)}
    last_valve = 'AA'
    starting_state = 0
    starting_flow = 0
    paths = traveling_elf(valves, steps, last_valve, minutes, 
                        state_machine, starting_state, starting_flow, {})
    total_flow = max(my_val + el_val for k1, my_val in paths.items() 
                     for k2, el_val in paths.items() if not k1 & k2)
    return total_flow
    

def solve():
    """Solve the puzzle for the given input."""
    parsed_data = parse()
    solution1 = part1(parsed_data)
    # reload - as in pytest, this parsed data is a fixture
    # parsed_data = parse(data)
    solution2 = part2(parsed_data)

    return solution1, solution2

if __name__ == "__main__":
    solutions = solve()
    print("\n".join(str(solution) for solution in solutions))