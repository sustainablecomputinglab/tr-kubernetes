"""
Copyright-2019 <Sustainable Computing Lab>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
"""
Core algorithm for computing # spot vms.
"""
import csv
from collections import defaultdict
from math import log

from utility import compute_availability
from vm import VM


def read_vm_list(AZ='us-west-1c'):
    vm_list = []
    record_file = "../data/record-us-west-1c.csv"
    with open(record_file, 'r') as my_file:
        reader = csv.reader(my_file, delimiter=',')
        list_dict = list(reader)

    vm_list = map(lambda x: VM(x[3], float(x[2]), float(x[1]), int(x[0]), float(x[-1])), list_dict[1:])
    # Sort VM List
    vm_list = sorted(vm_list, key=lambda node: node.sort_criteria(), reverse=False)
    return vm_list

def provision_spot(target_cap, target_avail, AZ='us-west-1c'):
    """
    Provisions/Picks Spot VMs to satisfy the user requirement
    vm_list: list of available vms
    target_cap: int
    target_avail: float
    rtype : Ordereddict
    """
    vm_list = read_vm_list()
    i = 0  # Iteration
    target_met = False  # Did we achieve the target cap at target avail.
    vm_pool = defaultdict(int)  # Variable to hold the best combination for each iteration
    cost_sel = 0  # Cost of each selection we consider.
    ecu_count = 0
    while not target_met:
        seq = min(i, len(vm_list)-1)  # How many VM types to consider for a iteration?
        cost_fnc = float("inf")  # Cost Function
        cur_avail = float("-inf") # Current best availability
        selection = 0
        for s in range(seq+1):
            vm_pool[vm_list[s]] += 1  # Add the VM to basket.
            ecu_count += vm_list[s].ecu
            cost_sel += vm_list[s].spot_avg_price
            # Availability for the considered vms at target cap.
            avail = compute_availability(vm_pool, target_cap)  
            # Heuristic: Did we consider atleast #nodes >= target cap.
            if ecu_count < target_cap:
                if cost_fnc > cost_sel * log(1/avail, 10):
                    cost_fnc = cost_sel * log(1/avail, 10)
                    selection = s
                    target_met = False
            elif ecu_count >= target_cap:
                if cost_fnc > cost_sel * log(1/avail, 10) and avail >= cur_avail:
                    selection = s
                    cur_avail = avail
                    cost_fnc = cost_sel * log(1/avail, 10)
                    target_met = True if avail >= target_avail else target_met
            vm_pool[vm_list[s]] -= 1
            ecu_count -= vm_list[s].ecu
            cost_sel -= vm_list[s].spot_avg_price
        vm_pool[vm_list[selection]] += 1
        ecu_count += vm_list[selection].ecu
        cost_sel += vm_list[selection].spot_avg_price
        i += 1
        # Algorithm Termination
        if ecu_count >= 3 * target_cap or target_met:
            break
    return vm_pool, cost_sel, ecu_count
