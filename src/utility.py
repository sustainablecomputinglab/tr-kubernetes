"""
Copyright-2019 <Sustainable Computing Lab>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import csv
import datetime

import iso8601
import numpy as np

def compute_pmf(selected_vms):
    """
    Computes the PMF of the selected VM pool.
    selected_vms: map of vms to node_size
    :rtype: List of floats
    """
    # Use convolution.
    availability_list = np.array([1.0])
    for vm, nodes in selected_vms.items():
        if nodes > 0:
            avail_array = np.zeros(vm.ecu * nodes + 1)
            avail_array[0] = 1 - vm.availability
            avail_array[vm.ecu * nodes] = vm.availability
            # Do convolution
            availability_list = np.convolve(avail_array, availability_list)
    return availability_list


def compute_availability(vm_basket, target_cap):
    """
    Compute the availability of a VM pool at a given target capacity.
    vm_basket: map of vms to node_size
    target_cap: target_cap
    """
    # 1. Get PMF.
    availability_list = compute_pmf(vm_basket)
    # 2. compute the availabilit from PMF.
    if target_cap > len(availability_list) - 1:
        return 1 - sum(availability_list[:int(len(availability_list)/2)])
    else:
        return 1 - sum(availability_list[:target_cap])