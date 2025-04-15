# Blob Storage with Managed Identity on AKS

This sample demonstrates how to use Azure Blob Storage with Managed Identity in an Azure Kubernetes Service (AKS) environment. It includes a FastAPI application that writes timestamps to a file mounted from Azure Blob Storage using a Kubernetes Persistent Volume (PV) and Persistent Volume Claim (PVC).

## Features
- FastAPI app that writes timestamps to a file in a mounted storage path
- Uses Azure Blob Storage mounted via CSI driver
- Managed Identity authentication (no secrets in code)
- Kubernetes manifests for deployment and storage

## Prerequisites
- Azure CLI
- AKS cluster with Managed Identity enabled
- Azure Blob Storage account
- CSI driver for Blob Storage installed on the cluster
- kubectl
- Docker

## Folder Structure
```
blob-storage-managed-identity/
├── azurefile-container-pv.yaml         # PV definition for Azure File/Blob
├── azurefile-container-pvc.yaml        # PVC definition for Azure File/Blob
├── deployment-container.yaml           # Deployment manifest for the app
├── src/
│   ├── app.py                         # FastAPI application
│   ├── Dockerfile                     # Container definition
│   └── requirements.txt               # Python dependencies
└── k8s/
    ├── deployment-app.yaml            # Example deployment
    └── storage.yaml                   # Example storage class and PVC
```

## How It Works
1. **Storage Mount**: Azure Blob Storage is mounted to `/mnt/<target>` in the container using the CSI driver and Kubernetes PV/PVC.
2. **Managed Identity**: The AKS pod uses a managed identity to access the storage account securely.
3. **App Endpoint**: The FastAPI app exposes a POST endpoint `/write-content/{target}` that writes the current UTC timestamp to `/mnt/{target}/output.txt`.

## Deployment Steps
1. **Build and Push the Docker Image**
   ```sh
   docker build -t <your-registry>/blob-storage-app:latest src/
   docker push <your-registry>/blob-storage-app:latest
   ```
2. **Configure Azure Resources**
   - Create a storage account and enable Blob NFS or Azure Files as needed.
   - Assign the managed identity with Storage Blob Data Contributor role.
3. **Apply Kubernetes Manifests**
   ```sh
   kubectl apply -f azurefile-container-pv.yaml
   kubectl apply -f azurefile-container-pvc.yaml
   kubectl apply -f deployment-container.yaml
   ```
4. **Test the Application**
   - Port-forward or expose the service.
   - Use curl or Postman to POST to `/write-content/<target>`.
   - Check the mounted storage for `output.txt` with timestamps.


## Deployment

1. `azd auth login`
1. `azd provision`


1. `task build_acr_python_ai`
1. `task build_acr`
1. `task deploy_app`
1. `task smoke_tests`

```bash
./write_files.sh     # command to generate files with different size, from 1M to 10G. Edit the file to change the target (container or shared)
./read_files.sh      # command to read files with different size, from 1M to 10G. Edit the file to change the target (container or shared)
./download_models.sh # command to download  an huggin face model to storage (container or shared)
./use_models.sh      # command to use a downloaded huggin face model to storage (container or shared)
```




## Example Request
```sh
curl  http://<app-service>:8000 #homepage
curl -X POST http://<app-service>:8000/write-content/shared #to write a timestamp to the shared file on the service account
curl -X POST http://<app-service>:8000/write-content/container #to write a timestamp to the container file on the service account

curl http://localhost:8000/model/microsoft_bitnet-b1.58-2B-4T/target/shared
curl http://localhost:8000/model/microsoft_bitnet-b1.58-2B-4T/target/container
curl http://localhost:8000/download/model/microsoft_bitnet-b1.58-2B-4T/target/shared

```
```
curl -X POST http://${IP}:80/write-content/shared/file/1M/size/1 |jq 
curl -X POST http://${IP}:80/write-content/shared/file/10M/size/10 | jq
curl -X POST http://${IP}:80/write-content/shared/file/10M/size/100
curl -X POST http://${IP}:80/write-content/shared/file/thousand/size/1000
curl -X POST http://${IP}:80/write-content/shared/file/tenthousand/size/10000
```
## Security
- No storage keys or secrets are stored in the code or manifests.
- Access is managed via Azure Managed Identity.

## References
- [Azure Blob CSI Driver](https://learn.microsoft.com/en-us/azure/aks/azure-csi-blobs)
- [AKS Managed Identity](https://learn.microsoft.com/en-us/azure/aks/use-managed-identity)
- [FastAPI](https://fastapi.tiangolo.com/)

## License
MIT


