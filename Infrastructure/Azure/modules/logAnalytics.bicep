/*
  Microsoft Docs:
    - https://docs.microsoft.com/en-us/azure/templates/microsoft.operationalinsights/workspaces?pivots=deployment-language-bicep
*/



// ----------------------------------------
// Parameter declaration
@description('Log Analytics Workspace name')
param name string

@description('Location of resource deployment')
param location string

@description('Log Analytics Workspace SKU')
@allowed([
  'CapacityReservation'
  'Free'
  'LACluster'
  'PerGB2018'
  'PerNode'
  'Premium'
  'Standalone'
  'Standard'
])
param sku string = 'PerGB2018'

@description('The workspace data retention in days. Allowed values are per pricing plan.')
param retentionInDays int = 30

@description('The network access type for accessing Log Analytics ingestion')
@allowed([
  'Enabled'
  'Disabled'
])
param publicNetworkAccessForIngestion string = 'Enabled'

@description('The network access type for accessing Log Analytics query')
@allowed([
  'Enabled'
  'Disabled'
])
param publicNetworkAccessForQuery string = 'Enabled'

@description('Tags to be applied to the resource')
param tags object

@description('The workspace daily quota for ingestion')
param dailyQuotaGb int = -1

@description('Workspace features')
param features object = {
  legacy: 0
  searchVersion: 1
  enableLogAccessUsingOnlyResourcePermissions: true
}



// ----------------------------------------
// Variable declaration



// ----------------------------------------
// Resource declaration
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2021-12-01-preview' = {
  properties: {
    sku: {
      name: sku
    }
    retentionInDays: retentionInDays
    features: features
    workspaceCapping: {
      dailyQuotaGb: dailyQuotaGb
    }
    publicNetworkAccessForIngestion: publicNetworkAccessForIngestion
    publicNetworkAccessForQuery: publicNetworkAccessForQuery
  }
  location: location
  tags: tags
  name: name
}

output workspaceId string = logAnalyticsWorkspace.id
output workspaceCustomerId string = logAnalyticsWorkspace.properties.customerId
output workspaceKey string = listKeys(logAnalyticsWorkspace.id, '2015-11-01-preview').primarySharedKey
