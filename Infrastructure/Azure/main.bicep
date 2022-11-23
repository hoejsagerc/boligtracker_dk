param tagValues object = {
  createdBy: 'pipeline'
  env: 'production'
  product: 'boligtracker'
}
param subnets array
param location string = resourceGroup().location

module virtualNetwork 'modules/virtualNetwork.bicep' = {
  name: 'vnet-prod-boligtracker'
  params: {
    tags: tagValues
    name: 'vnet-prod-boligtracker'
    location: location
    addressSpace: {
      addressPrefixes: [
        '10.101.0.0/21'
      ]
    }
    enableDdosProtection: false
    subnets: subnets
  }
}

module logAnalyticsWorkspace 'modules/logAnalytics.bicep' = {
  name: 'la-prod-boligtracker'
  params: {
    name: 'la-prod-boligtracker'
    location: location
    tags: tagValues
  }
}

module storageAccount 'modules/storageAccount.bicep' = {
  name: 'saboligtracker'
  params: {
    name: 'saboligtracker'
    location: location
    sku: 'Standard_LRS'
    kind: 'StorageV2'
    tags: tagValues
    subnetId: virtualNetwork.outputs.subnetIdsObject.snetStorage
    subnetIp: '10.101.0.4'
    allowBlobPublicAccess: false
    publicNetworkAccess: 'Disabled'
    queues: [
      'schedules'
    ]
  }
  dependsOn: [
    virtualNetwork
  ]
}

module containerRegistry 'modules/containerRegistry.bicep' = {
  name: 'acrboligtracker'
  params: {
    name: 'acrboligtracker'
    location: location
    adminUserEnabled: true
  }
}

module containerAppEnv 'modules/containerAppEnv.bicep' = {
  name: 'cae-prod-boligtracker'
  params: {
    name: 'cae-prod-boligtracker'
    location: location
    logAnalyticsWorkspaceId: logAnalyticsWorkspace.outputs.workspaceCustomerId
    subnetId: virtualNetwork.outputs.subnetIdsObject.snetContainer
    logAnalyticsWorkspaceKey: logAnalyticsWorkspace.outputs.workspaceKey
  }
}
