# Kubernetes

## Cluster

A Kubernetes cluster consists of master (control plane) and worker (compute) nodes.
Master Node: Manages the cluster, handling scheduling, scaling, and updates.
Worker Nodes: Run the containerized applications (pods).

## Pods

The smallest deployable units in Kubernetes.
Encapsulate one or more containers that share storage and network resources.
Designed to be ephemeral; Kubernetes can replace pods to maintain the desired state.

## Services

Provide a stable IP address and DNS name for a set of pods.
Enable communication between different components of your application and external clients.
Types include ClusterIP, NodePort, and LoadBalancer.

## Deployments

Manage stateless applications by defining the desired state (e.g., number of replicas).
Handle rolling updates and rollbacks seamlessly.
Use ReplicaSets under the hood to maintain the desired number of pod replicas.

## ReplicaSets

Ensure a specified number of pod replicas are running at any given time.
Rarely used directly; usually managed by Deployments.

## ConfigMaps and Secrets

**ConfigMaps**: Store non-confidential configuration data in key-value pairs.
**Secrets**: Securely store sensitive information like passwords or tokens.
Both can be injected into pods as environment variables or mounted as files.

## Volumes

Abstract storage solutions that allow data to persist beyond the life of a pod.
Support various backends like local storage, cloud storage, or network filesystems.

## Namespaces

Provide a way to divide cluster resources between multiple users or teams.
Useful for organizing and managing resources in complex environments.

## Ingress

Manages external access to services within a cluster, typically HTTP/HTTPS routes.
Offers features like SSL termination, name-based virtual hosting, and load balancing.