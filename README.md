# coronavirus-api
Coronavirus UK cases by county API using Kubernetes, Istio, MetalLB and Python. This is quite rough and ready, parts are hardcoded (certificates.yaml etc) and you might need to make some changes to fit your environment.

# Requirements

This guide assumes you have:

- Kubernetes 1.17.x cluster installed
- Kubectl 1.17.x binary installed and configured with management control plane
- Istioctl 1.5.0+ installed

# Installation
Edit `apply.sh` and make modifications to variables if required and then execute the script.

```
# Replace with secure passwords
MYSQL_ROOT_PASSWORD='PASSWORD' MYSQL_USER_PASSWORD='PASSWORD' ./apply.sh
```
