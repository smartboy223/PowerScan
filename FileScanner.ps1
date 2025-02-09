param (
    [Parameter(Mandatory=$true)]
    [string]$Keywords,
    [Parameter(Mandatory=$true)]
    [string]$OutputFile,
    [int]$MaxResults = [int]::MaxValue,a
    [string]$Include = "",
    [string]$Exclude = "",
    [string]$RootFolder = $PSScriptRoot
)

# Define log and progress file paths
$logFile = "Refined_Results\scan.log"
$progressFile = "Refined_Results\progress.txt"

# Ensure output directories exist
$outputDir = Split-Path -Path $OutputFile -Parent
if (-not (Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}
if (-not (Test-Path -Path "Refined_Results")) {
    New-Item -ItemType Directory -Path "Refined_Results" | Out-Null
}

# Clear log and progress files
Set-Content -Path $logFile -Value "" -Encoding UTF8
Set-Content -Path $progressFile -Value "0"

$results = @()
$progress = 0

try {
    # Retrieve all files recursively under the chosen RootFolder, excluding unwanted extensions
    $files = Get-ChildItem -Path $RootFolder -Recurse -File | Where-Object { $_.Extension -notin @(".ps1", ".html", ".json", ".log") }
} catch {
    Add-Content -Path $logFile -Value "Error retrieving files from ${RootFolder}: $($_.Exception.Message)"
    exit
}

$totalFiles = $files.Count

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8

        if ($content -match "\b$Keywords\b") {

            # If an Include filter is specified, ensure at least one word is found.
            if ($Include -ne "") {
                $includeWords = $Include -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
                $includeMatched = $false
                foreach ($word in $includeWords) {
                    if ($content -match "\b$([regex]::Escape($word))\b") {
                        $includeMatched = $true
                        break
                    }
                }
                if (-not $includeMatched) { continue }
            }

            # If an Exclude filter is specified, skip the file if any word is found.
            if ($Exclude -ne "") {
                $excludeWords = $Exclude -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
                $excludeFound = $false
                foreach ($word in $excludeWords) {
                    if ($content -match "\b$([regex]::Escape($word))\b") {
                        $excludeFound = $true
                        break
                    }
                }
                if ($excludeFound) { continue }
            }

            # Use Select-String to retrieve matches for the primary keyword
            $matches = Select-String -Path $file.FullName -Pattern "\b$Keywords\b" -AllMatches
            if ($matches.Matches.Count -gt 0) {
                $fileResults = @{
                    FileName = $file.FullName;
                    Matches  = @()
                }
                foreach ($match in $matches) {
                    if ($fileResults.Matches.Count -ge $MaxResults) { break }
                    $fileResults.Matches += @{
                        LineNumber = $match.LineNumber;
                        Text       = $match.Line.Trim()
                    }
                }
                $results += $fileResults
            }
        }
    }
    catch {
        Add-Content -Path $logFile -Value "Error scanning file: $($file.FullName). Error: $($_.Exception.Message)"
    }
    
    $progress += (1 / $totalFiles) * 100
    Set-Content -Path $progressFile -Value ([math]::Round($progress))
}

try {
    $results | ConvertTo-Json -Depth 3 | Set-Content -Path $OutputFile -Encoding UTF8
}
catch {
    Add-Content -Path $logFile -Value "Error saving results: $($_.Exception.Message)"
}

Add-Content -Path $logFile -Value "Scan completed. Results saved to $OutputFile."
