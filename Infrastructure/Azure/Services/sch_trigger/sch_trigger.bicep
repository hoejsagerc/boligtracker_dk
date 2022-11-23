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
param queueName string

/* PARAMETERS FOR THE ENVORNMENT VARIABLE SECRETS */
@secure()
param db_password string
@secure()
param db_username string
@secure()
param acr_password string
@secure()
param queueConnectionString string


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
        {
          name: 'queue-conn-string'
          value: queueConnectionString
        }
      ]
      activeRevisionsMode: 'multiple'
      /*ingress: {
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
      }*/
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
          image: 'acrboligtracker.azurecr.io/boligtracker/sch_trigger:${containerTag}'
          name: 'boligtracker-schtrigger'
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
              name: 'QUEUE_CONN_STRING'
              value: ''
              secretRef: 'queue-conn-string'
            }
            {
              name: 'QUEUE_NAME'
              value: queueName
            }
            {
              name: 'DB_USER'
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
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
  identity: {
    type: 'None'
  }
}
