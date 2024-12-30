# Application Gateway For Container

https://learn.microsoft.com/en-us/azure/application-gateway/for-containers/

Application Gateway for Containers is an application layer (layer 7) load balancing and dynamic traffic management product for workloads running in a Kubernetes cluster. It extends Azure's Application Load Balancing portfolio and is a new offering under the Application Gateway product family.

Application Gateway for Containers is the evolution of the Application Gateway Ingress Controller (AGIC), a Kubernetes application that enables Azure Kubernetes Service (AKS) customers to use Azure's native Application Gateway application load-balancer. In its current form, AGIC monitors a subset of Kubernetes Resources for changes and applies them to the Application Gateway, utilizing Azure Resource Manager (ARM).


## Deploy Application Gateway for Containers ALB Controller

https://learn.microsoft.com/en-us/azure/application-gateway/for-containers/quickstart-deploy-application-gateway-for-containers-alb-controller?tabs=install-helm-windows

Deploy a brand new AKS Cluster and configure the ALB Controller. An Application Gateway for Containers *ALB Controller* is a Kubernetes deployment that orchestrates configuration and deployment of Application Gateway for Containers by watching Kubernetes both Custom Resources and Resource configurations, such as, but not limited to, Ingress, Gateway, and ApplicationLoadBalancer. It uses both ARM / Application Gateway for Containers configuration APIs to propagate configuration to the Application Gateway for Containers Azure deployment. 

```
task azure_auth
task new_aks_cluster
task azure_alb_identity
task deploy_alb_controller
task verify_alb_controller
``` 

## Application Gateway for Containers: bring your own deployment

https://learn.microsoft.com/en-us/azure/application-gateway/for-containers/quickstart-create-application-gateway-for-containers-byo-deployment

```
task byo_create_application_gateway4c
``` 