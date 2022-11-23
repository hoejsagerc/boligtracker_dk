/* PARAMETERS FOR THE RESOURCE CONFIGURATION */
param location string = resourceGroup().location
param name string
param tags object
param appEnvironmentName string
param containerRegistryName string

/* PARAMETER FOR CONTAINER */
param containerTag string

/*PARAMETERS FOR ENVIRONMENT VARIABLES*/
param db_Name string
param db_Host string

/* PARAMETERS FOR THE ENVORNMENT VARIABLE SECRETS */
@secure()
param db_password string
@secure()
param db_username string
@secure()
param acr_password string


resource appEnvironment 'Microsoft.App/managedEnvironments@2022-06-01-preview' existing = {
  name: appEnvironmentName
}


resource containerApp 'Microsoft.App/containerApps@2022-06-01-preview' = {
  name: name
  location: location
  tags: tags
  properties: {
    managedEnvironmentId: appEnvironment.id
    environmentId: appEnvironment.id
    configuration: {
      secrets: [
        {
          name: 'db-password'
          value: db_password
        }
        {
          name: 'db-username'
          value: db_username
        }
        {
          name: 'acr-passowrd'
          value: acr_password
        }
      ]
      activeRevisionsMode: 'multiple'
      ingress: {
        external: true
        targetPort: 80
        exposedPort: 0
        transport: 'Auto'
        traffic: [
          {
            weight: 100
            latestRevision: true
          }
        ]
        customDomains: []
        allowInsecure: false
      }
      registries: [
        {
          server: '${containerRegistryName}.azurecr.io'
          username: containerRegistryName
          passwordSecretRef: 'acr-passowrd'
          identity: ''
        }
      ]
    }
    template: {
      revisionSuffix: ''
      containers: [
        {
          image: 'acrboligtracker.azurecr.io/boligtracker/api:${containerTag}'
          name: 'boligtracker-api'
          env: [
            {
              name: 'DB_NAME'
              value: db_Name
            }
            {
              name: 'DB_HOST'
              value: db_Host
            }
            {
              name: 'DB_USERNAME'
              value: ''
              secretRef: 'db-username'
            }
            {
              name: 'DB_PASSWORD'
              value: ''
              secretRef: 'db-password'
            }
          ]
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          probes: []
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 10
      }
    }
  }
  identity: {
    type: 'None'
  }
}
