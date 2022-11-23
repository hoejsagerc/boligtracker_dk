param name string
param location string
param subnetId string
param logAnalyticsWorkspaceId string
param logAnalyticsWorkspaceKey string


resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2022-06-01-preview' = {
  name: name
  location: location
  properties: {
    vnetConfiguration: {
      internal: false
      infrastructureSubnetId: subnetId
      dockerBridgeCidr: '10.1.0.1/16'
      platformReservedCidr: '10.0.0.0/16'
      platformReservedDnsIP: '10.0.0.2'
      outboundSettings: {
        outBoundType: 'LoadBalancer'
      }
    }
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspaceId
        sharedKey: logAnalyticsWorkspaceKey
      }
    }
    zoneRedundant: false
    customDomainConfiguration: {
    }
  }
  sku: {
    name: 'Consumption'
  }
}
