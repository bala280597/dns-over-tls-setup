# DNS-over-TLS-proxy

## Background
DNS over TLS (Transport Layer Security) or “DoT” is an IETF standard that provides full-stream encryption between a DNS client and a DNS server. DNS has traditionally suffered from a “last mile” security problem: Communications between a DNS client and the DNS server are almost always unencrypted, and therefore subject to spoofing, interception, and more. 

## Implementation
The script dnsovertls.py uses the socket and ssl modules to achieve the given task. 
It creates a socket and binds it on port 12555. It can receive a TCP DNS request on this port and forward it to any DNS provider that supports DNS over TLS.
Used DNS server='1.1.1.1' and DNS port=853 as default.

### Docker image and container
To build a docker container just run the following command
  - docker build -t bala2805/dns-tls .
  
  ![image](https://user-images.githubusercontent.com/47313756/151123823-8fa6442b-06cc-49bb-bb69-a84c4ff3adc5.png)

  
To run the docker container 
  - docker run -d --name dns-proxy-server -p 12555:12555 bala2805/dns-tls:latest

To test the setup
  - dig @127.0.0.1 -p 12555 +tcp google.com
  
  ![image](https://user-images.githubusercontent.com/47313756/151125622-2951264b-923e-40b5-b06c-1b40fc3863f4.png)

## Improvements
The following improvements can be done to this service:
  * Handles a multiple request at a time. 

## Security Consideration
Use of DNS over TLS is designed to address the privacy risks that arise out of the ability to eavesdrop on DNS messages.  
It does not address other security issues in DNS such as:
  - Man in Middle Attack : DNS protocol interactions performed in the clear can be modified by a person-in-the-middle attacker.
  - Middleboxes are present in some networks and have been known to interfere with normal DNS resolution.

## Micro Service Containerized application
The following process can be done in microservice architecture.
  * Create Deployment Kind with created image . It helps desired number of pods running as mentioned in replicas.
  * Create Service with LoadBalancer.
  * Use the desired service IP to encrypt dns queries with desired port

### Kubernetes Deployment & Service
Create deployment with build image and open container port 12555.
  - kubectl create -f deploy.yml

Create service with type LoadBalancer to expose created deployment.
  - kubectl create -f svc.yml
  
  ![image](https://user-images.githubusercontent.com/47313756/151124076-3456389a-91ff-4116-84f1-dcbe100fea5a.png)

To test the setup
  - dig @ServiceIp -p 12555 +tcp google.com
  
  ![image](https://user-images.githubusercontent.com/47313756/151124945-69d2a29d-00b3-4c30-a066-afb3a882d285.png)
