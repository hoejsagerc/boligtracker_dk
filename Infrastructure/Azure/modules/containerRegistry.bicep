param name string
param location string
param adminUserEnabled bool


resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-09-01' = {
  name: name
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: adminUserEnabled
  }
}
