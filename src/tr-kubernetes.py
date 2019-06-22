"""
Copyright-2019 <Sustainable Computing Lab>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import argparse
import sys
from collections import OrderedDict

import oyaml as yaml

from algo import provision_spot
from vm import VM

IN_FILE_PATH = "./yaml-template/cluster.yaml"

def wrap_spot_fleet(spot_vm, count, pool_num):
  """
  wrapper for representing a spot VM as spot fleet in configuration file
  type spot_vm: VM object
  type count: Int
  type pool_num: Int
  rtype: OrderedDict
  """
  spot_fleet = OrderedDict()
  spot_fleet["name"] = "nodepool-spot-"+str(pool_num)
  spot_fleet["spotFleet"] = OrderedDict()
  # spot_fleet["spotFleet"]["iamFleetRoleArn"] = "arn:aws:iam::014861551224:role/aws-ec2-spot-fleet-tagging-role"
  spot_fleet["spotFleet"]["targetCapacity"] = spot_vm.ecu*count
  spot_fleet["spotFleet"]["spotPrice"] = spot_vm.on_demand_price
  spot_fleet["spotFleet"]["launchSpecifications"] = []
  new_dict = OrderedDict()
  new_dict["weightedCapacity"] = spot_vm.ecu
  new_dict["instanceType"] = spot_vm.name
  spot_fleet["spotFleet"]["launchSpecifications"].append(new_dict)
  return spot_fleet

def config_yaml(target_capacity, target_availability,AZ='us-west-1c'):
  """
  Takes user input and adds the algorithm output to config file(yaml)

  """
  # Load base config file
  with open(IN_FILE_PATH, 'rb') as f:
    cluster = yaml.load(f,  Loader=yaml.FullLoader)
  vm_pool, _, _ = provision_spot(target_capacity, target_availability, AZ=AZ)
  pool_num = 1
  for vm, count in vm_pool.items():
    if count > 0:
      pool_num += 1
      cluster["worker"]["nodePools"].append(wrap_spot_fleet(vm, count, pool_num))
  with open(IN_FILE_PATH, 'w') as f:
    yaml.dump(cluster, f)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-C", type=int, metavar='Capacity in ECU (Integer)')
  parser.add_argument("-A", type=float, metavar='Availability (Float, < 1.0)')
  parser.add_argument("-AZ", type=str, default='us-west-1c', metavar='Avaialbility Zone (str)')
  args = parser.parse_args()

  if (not args.A) or  (not args.C):
    parser.print_help()
    sys.exit()
  
  config_yaml(args.C, args.A, args.AZ)
