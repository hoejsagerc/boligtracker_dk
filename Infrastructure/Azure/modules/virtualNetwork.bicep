
param location string
param tags object
param name string
param addressSpace object
param subnets array
param enableDdosProtection bool


resource virtualNetwork 'Microsoft.Network/virtualNetworks@2022-01-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    addressSpace: addressSpace
    subnets: [ for subnet in subnets: {
      name: subnet.name
      properties: subnet.properties
    }]
    virtualNetworkPeerings: []
    enableDdosProtection: enableDdosProtection
  }
}


output subnetIdsObject object = {
  snetStorage: resourceId('Microsoft.Network/VirtualNetworks/subnets', name, subnets[0].name)
  snetData: resourceId('Microsoft.Network/VirtualNetworks/subnets', name, subnets[1].name)
  snetContainer: resourceId('Microsoft.Network/VirtualNetworks/subnets', name, subnets[2].name)
}
