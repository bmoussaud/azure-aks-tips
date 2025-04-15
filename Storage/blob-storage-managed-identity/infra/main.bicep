// -----------------------------------------------------------------------------
// main.bicep
// Purpose: Provision an Azure Kubernetes Service (AKS) cluster with integrated
// Azure Container Registry (ACR) and secure Azure Storage (Blob and File) resources.
// This file follows Azure best practices, enabling managed identities, RBAC,
// workload identity, and secure storage access for cloud-native workloads.
// -----------------------------------------------------------------------------

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string = 'francecentral'

// tags that should be applied to all resources.
var tags = {
  // Tag all resources with the environment name.
  'azd-env-name': environmentName
}

#disable-next-line no-unused-vars
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: 'storageacr${uniqueString(resourceToken)}'
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    adminUserEnabled: false
  }
  tags: tags
}

resource aks 'Microsoft.ContainerService/managedClusters@2024-09-01' = {
  name: 'aks${uniqueString(resourceToken)}'
  location: location
  tags: tags
  sku: {
    name: 'Base'
    tier: 'Free' //Standard
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
   
    dnsPrefix: 'aksdns${uniqueString(resourceToken)}'
    agentPoolProfiles: [
      {
        name: 'nodepool1'
        count: 1
        vmSize: 'Standard_D8d_v4'
        osType: 'Linux'
        mode: 'System'
      }
    ]
    enableRBAC: true
    ingressProfile: {
      webAppRouting: {
        enabled: true
        
      }
    }
    oidcIssuerProfile: {
      enabled: true
    }
    networkProfile: {
      networkPlugin: 'azure'
      loadBalancerSku: 'standard'
    }
    apiServerAccessProfile: {
      enablePrivateCluster: false
    }
  
    securityProfile: {
      workloadIdentity: {
        enabled: true
      }
    }
    storageProfile: {
      blobCSIDriver: {
        enabled: true
      }
    }
  }
}

resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aks.id, acr.id, 'AcrPullRole')
  scope: acr

  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d') // AcrPull
    principalId: aks.properties.identityProfile.kubeletidentity.objectId
    principalType: 'ServicePrincipal'
  }
}

resource kubeletKeyOperatorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, 'kubelet-key-operator', aks.name)
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '81a9662b-bebf-436f-a333-f67b29880f12') // Storage Account Key Operator Service Role
    principalId: aks.properties.identityProfile.kubeletidentity.objectId
    principalType: 'ServicePrincipal'
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'storage${uniqueString(resourceToken)}'
  tags: tags
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    encryption: {
      services: {
        blob: {
          enabled: true
        }
        file: {
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  name: 'default'
  parent: storageAccount
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: 'container4aks'
  parent: blobService
  properties: {
    publicAccess: 'None'
  }

}

resource fileService 'Microsoft.Storage/storageAccounts/fileServices@2023-01-01' = {
  name: 'default'
  parent: storageAccount
}

resource fileShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-01-01' = {
  name: 'fileshare4aks'
  parent: fileService
  properties: {
    accessTier: 'Hot'
  }
}

output aksFqdn string = aks.properties.fqdn
output ACR_NAME string = acr.name
output CLUSTER string = aks.name
output RG string = resourceGroup().name
output STORAGE_ACCOUNT string = storageAccount.name
output CONTAINER_NAME string = blobContainer.name
output SHARED_NAME string = fileShare.name
output LOCATION string = location
output AKS_IDENTITY string = aks.identity.principalId
output STORAGE_ACCOUNT_ID string = storageAccount.id
