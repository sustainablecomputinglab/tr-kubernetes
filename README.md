# TR-Kubernetes
 TR-Kubernetes is a container orchestration platform that optimizes the cost of executing mixed interactive and batch workloads on cloud platforms using transient VMs. In this repository, we host the code for TR-Kubernetes prototype implementation (minimally extends kube-aws). Full details of TR-Kubernetes in our [paper](http://www.ecs.umass.edu/~irwin/tr-kubernetes.pdf).

## Requirements

1. Python3

2. [AWS CLI](https://aws.amazon.com/cli/)

3. [kube-aws](https://github.com/kubernetes-incubator/kube-aws)

4. [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Creating a Kubernetes cluster using TR-Kubernetes

1. Follow the getting started instructions in [kube-aws tutorial](https://kubernetes-incubator.github.io/kube-aws/) till step-2 i.e., complete step-1 (configure) and step-2 (render) from that page to generate a cluster.yaml (with AWS credentials and DNS name etc.) and other required files.

2. Before launching the Kubernetes cluster using kube-aws, use TR-Kubernetes extensions to add the required spot VMs configuration/information (that meets users capacity availability requirment) to the cluster.yaml. To do that, please run the following command to add the spot VMs add to cluster.yaml. Note that, you may change the IN_FILE_PATH variable in tr-kubernetes.py to point to cluster.yaml generated in the above step.

  ```bash
  python tr-kubernetes.py -C 500 -A 0.9999 -AZ us-west-1c
  ```

3. Once the spot VMs information is added to cluster.yaml file, follow the rest of the instructions/steps from [kube-aws tutorial](https://kubernetes-incubator.github.io/kube-aws/) to create, modify, and destroy the Kubernetes cluster.

4. Once the cluster is up, use kubectl command line tool to create the deployments, jobs, services etc.

## Limitations

* TR-Kubernetes extension includes the availability and cost estimates for all the 14 AWS EC2 availability zones in U.S. These estimates are based on data from September 2017 to November 2017.

## Citation

```Bibitex
@article{Ambati:2019:OCE:3341617.3326143,
 author = {Ambati, Pradeep and Irwin, David},
 title = {Optimizing the Cost of Executing Mixed Interactive and Batch Workloads on Transient VMs},
 journal = {Proc. ACM Meas. Anal. Comput. Syst.},
 issue_date = {June 2019},
 volume = {3},
 number = {2},
 month = jun,
 year = {2019},
 issn = {2476-1249},
 pages = {28:1--28:24},
 articleno = {28},
 numpages = {24},
 url = {http://doi.acm.org/10.1145/3341617.3326143},
 doi = {10.1145/3341617.3326143},
 acmid = {3326143},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {cloud computing, resource allocation, run time management and scheduling},
}
```
