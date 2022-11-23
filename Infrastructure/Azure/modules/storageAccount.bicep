param sku string
param kind string
param name string
param location string
param tags object
param allowBlobPublicAccess bool
param publicNetworkAccess string
param subnetId string
param subnetIp string
param queues array


resource storageAccount 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  sku: {
    name: sku
  }
  kind: kind
  name: name
  location: location
  tags: tags
  properties: {
    dnsEndpointType: 'Standard'
    defaultToOAuthAuthentication: false
    publicNetworkAccess: publicNetworkAccess
    allowCrossTenantReplication: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: allowBlobPublicAccess
    allowSharedKeyAccess: true
    networkAcls: {
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: []
      defaultAction: 'Deny'
    }
    supportsHttpsTrafficOnly: true
    encryption: {
      requireInfrastructureEncryption: false
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    accessTier: 'Hot'
  }
}


resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  location: location
  name: 'pep-${name}'
  properties: {
    subnet: {
      id: subnetId
    }
    customNetworkInterfaceName: 'nic-sa-storage-nic'
    privateLinkServiceConnections: [
      {
        name: 'pep-${name}'
        properties: {
          privateLinkServiceId: storageAccount.id
          groupIds: [
            'queue'
        ]
        }
      }
    ]
  }
  tags: {
  }
  dependsOn: []
}



resource queueService 'Microsoft.Storage/storageAccounts/queueServices@2022-05-01' = {
  name: 'default'
  parent: storageAccount
  properties: {
    cors: {}
  }
}


resource scheduleQueue 'Microsoft.Storage/storageAccounts/queueServices/queues@2022-05-01' = [for queue in queues :{
  name: queue
  parent: queueService
  properties: {
    metadata:{}
  }
}]
