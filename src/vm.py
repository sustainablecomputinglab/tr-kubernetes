"""
Copyright-2019 <Sustainable Computing Lab>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from math import log


# Class definition for VM
class VM:
    def __init__(self, name, on_demand_price, spot_avg_price, ecu, availability, memory=None):
        """
        :type name: string
        :type on_demand_price: float
        :type spot_avg_rpice: float
        :ecu: int
        :availability: float
        """
        self.name = name
        self.on_demand_price = on_demand_price
        self.spot_avg_price = spot_avg_price
        self.ecu = ecu
        self.availability = availability
        self.memory = memory

    # Sorting criteria for VM.
    def sort_criteria(self):
        return self.spot_avg_price * log(1/self.availability, 10)/(self.ecu)
