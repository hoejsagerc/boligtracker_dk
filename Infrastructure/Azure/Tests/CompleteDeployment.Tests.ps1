param (
    [Parameter(Mandatory=$false)]
    [String]$script:mainFilePath = "../main.bicep",

    [Parameter(Mandatory=$false)]
    [String]$script:parameterFilePath = "../parameters.json",

    [Parameter(Mandatory=$false)]
    [string]$script:modulesFolder = "../modules/",

    [Parameter(Mandatory=$true)]
    [string]$script:resourceGroup
)


# Creating script scoped variables
$script:validationOutputFilePath = $script:mainFilePath.replace(".bicep", ".json")
$script:operatingSystem = $env:OS

# Finding all described modules in the main.bicep file
$content = Get-Content $mainFilePath
$contentLines = $content.Split([Environment]::NewLine)
$script:modules = New-Object System.Collections.ArrayList
foreach($line in $contentLines) {
    $line.split(" ") | ForEach-Object {
        if (($_).ToLower() -match "modules/") {
            $modules.add($_.split("/")[1].replace("'", "")) | Out-Null
        }
    }
}


# Testing if all the modules described in the main.bicep file, actually exists
Describe "Checking Bicep Module" {

    Foreach($module in $script:modules) {
        Context "Checking if Module exists" {        
            It "Checking if module $($module) exists" {
                $testPath = Test-Path "$($script:modulesFolder)/$($module)"
                $testPath | Should -be $true
            }
        }
    }
}

# Testing Bicep Linting
Describe "Bicep Build Linting" {
    Context "Check if bicep build command succeeded" {
        BeforeAll {
            If ($operatingSystem -eq "Windows_NT") {
                $output = az bicep build --file $mainFilePath --outdir "../" 2>&1
            }
            else {
                $output = az bicep build --file $mainFilePath --outdir "../" 2`>`&1
            }
        }

        It "Check Bicep linting" {
            $output | Should -Be $null
        }

        It "Checks if output file exists" {
            $pathTest = Test-Path $validationOutputFilePath
            $pathTest | Should -Be $true -Because $output
        }
    }
}



Describe "Bicep Deployment Validation" {
    BeforeAll {
        $validateOutput = az deployment group validate --resource-group $resourceGroup --template-file $parameterFilePath --output json
        if($validateOutput) {
            $validateOutput | Out-file "../validateOutput.json"
        }
    }

    Context "Checking if Bicep Validation will run" {
        It "Checking bicep validate command will run" {
            $validateOutput | Should -Not -Be $null -Because $validateOutput
        }

        It "Checking that validation had no errors" {
            $hashOutput = $validateOutput | ConvertFrom-Json -AsHashtable
            $hashOutput.error | Should -Be $null -Because $hashOutput.error
        }

        It "Checking that validation was successful" {
            $hashOutput = $validateOutput | ConvertFrom-Json -AsHashtable
            $hashOutput.properties.provisioningState | Should -Be "Succeeded"
        }
    }
}