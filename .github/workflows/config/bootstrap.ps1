Write-Host "Installing Security Platform..."

# ==========================================
# Python Dependencies
# ==========================================

pip install pre-commit
pip install git+https://github.com/awslabs/automated-security-helper.git@v3.5.4
pip install "typer==0.19.2"
pip install semgrep

# ==========================================
# Install CDK-NAG Dependencies
# ==========================================

Write-Host "Installing CDK-NAG dependencies..."

pip install aws-cdk-lib==2.260.0
pip install constructs
pip install cdk-nag==2.28.195

if ($LASTEXITCODE -ne 0) {

    Write-Host "ERROR: Failed to install CDK-NAG dependencies"
    exit 1

}

Write-Host "Validating CDK-NAG installation..."

python -c "import cdk_nag; import aws_cdk; import constructs"

if ($LASTEXITCODE -ne 0) {

    Write-Host "ERROR: CDK-NAG validation failed"
    exit 1

}

Write-Host "CDK-NAG dependencies installed successfully"

# ==========================================
# Verify npm
# ==========================================

npm --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: npm is not installed"
    exit 1
}

# ==========================================
# Verify Docker (Optional)
# ==========================================

docker --version

if ($LASTEXITCODE -eq 0) {

    Write-Host "Docker detected"
    Write-Host "Container image scanning available"

}
else {

    Write-Host "Docker not detected"
    Write-Host "Container image scanning will be skipped"

}

# ==========================================
# Install Node Dependencies (all Node projects)
# ==========================================

Write-Host "Searching for package.json files..."

Get-ChildItem -Recurse -Filter package.json | ForEach-Object {

    Write-Host ""
    Write-Host "Found Node project:"
    Write-Host $_.DirectoryName

    Push-Location $_.DirectoryName

    Write-Host "Running npm install..."

    npm install

    if ($LASTEXITCODE -ne 0) {

        Write-Host "ERROR: npm install failed in $($_.DirectoryName)"

        Pop-Location
        exit 1

    }

    Pop-Location

}

# ==========================================
# Install Syft
# ==========================================

Write-Host "Installing Syft..."

winget install Anchore.Syft -e --silent --accept-package-agreements --accept-source-agreements

# ==========================================
# Install Grype
# ==========================================

Write-Host "Installing Grype..."

winget install Anchore.Grype -e --silent --accept-package-agreements --accept-source-agreements

# ==========================================
# Add Syft/Grype to CURRENT session PATH
# (required for ASH to detect them immediately)
# ==========================================

$syftPath = Get-ChildItem `
    "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" `
    -Recurse `
    -Filter syft.exe `
    -ErrorAction SilentlyContinue |
    Select-Object -First 1

if ($syftPath) {

    $env:PATH += ";$($syftPath.DirectoryName)"

    Write-Host "Syft found at:"
    Write-Host $syftPath.FullName

}

$grypePath = Get-ChildItem `
    "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" `
    -Recurse `
    -Filter grype.exe `
    -ErrorAction SilentlyContinue |
    Select-Object -First 1

if ($grypePath) {

    $env:PATH += ";$($grypePath.DirectoryName)"

    Write-Host "Grype found at:"
    Write-Host $grypePath.FullName

}

# ==========================================
# Verify Syft
# ==========================================

Write-Host "Validating Syft..."

syft version

if ($LASTEXITCODE -ne 0) {

    Write-Host "ERROR: Syft installation failed"
    exit 1

}

# ==========================================
# Verify Grype
# ==========================================

Write-Host "Validating Grype..."

grype version

if ($LASTEXITCODE -ne 0) {

    Write-Host "ERROR: Grype installation failed"
    exit 1

}

# ==========================================
# Refresh ASH Dependencies
# ==========================================

ash dependencies update

# ==========================================
# Install Git Hooks
# ==========================================

#pre-commit install
#pre-commit install --hook-type pre-push
Write-Host "hooks installed"
pre-commit install --config config/.pre-commit-config.yaml

pre-commit install --hook-type pre-push --config config/.pre-commit-config.yaml

Write-Host "Security Platform Installed Successfully"
