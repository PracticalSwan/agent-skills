# XAMPP PHP Environment Setup Script
# PowerShell script to configure XAMPP for PHP development

param(
    [string]$XamppPath = "C:\xampp",
    [string]$ProjectPath = ""
)

Write-Host "XAMPP PHP Environment Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if XAMPP is installed
if (-not (Test-Path $XamppPath)) {
    Write-Host "ERROR: XAMPP not found at $XamppPath" -ForegroundColor Red
    Write-Host "Please install XAMPP from https://www.apachefriends.org/" -ForegroundColor Yellow
    exit 1
}

$PhpIniPath = "$XamppPath\php\php.ini"
$HttpdConfPath = "$XamppPath\apache\conf\httpd.conf"

# Backup original files
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item $PhpIniPath "$PhpIniPath.bak_$Timestamp" -Force
Copy-Item $HttpdConfPath "$HttpdConfPath.bak_$Timestamp" -Force
Write-Host "Backed up original configuration files" -ForegroundColor Green

# Configure PHP settings
Write-Host "`nConfiguring PHP settings..." -ForegroundColor Yellow

$PhpIniContent = Get-Content $PhpIniPath -Raw

# Enable error reporting for development
$PhpIniContent = $PhpIniContent -replace 'error_reporting = .*', 'error_reporting = E_ALL'
$PhpIniContent = $PhpIniContent -replace 'display_errors = .*', 'display_errors = On'
$PhpIniContent = $PhpIniContent -replace 'display_startup_errors = .*', 'display_startup_errors = On'

# Increase upload limits
$PhpIniContent = $PhpIniContent -replace 'upload_max_filesize = .*', 'upload_max_filesize = 10M'
$PhpIniContent = $PhpIniContent -replace 'post_max_size = .*', 'post_max_size = 10M'

# Set timezone (modify as needed)
$PhpIniContent = $PhpIniContent -replace ';date.timezone =.*', "date.timezone = `"UTC`""

# Ensure PDO extensions are enabled
if ($PhpIniContent -notmatch 'extension=pdo_mysql') {
    $PhpIniContent = $PhpIniContent -replace '(;)?extension=pdo_mysql', 'extension=pdo_mysql'
}

# Save PHP configuration
$PhpIniContent | Set-Content $PhpIniPath -Encoding UTF8
Write-Host "PHP configuration updated" -ForegroundColor Green

# Configure Apache for project
if ($ProjectPath -and (Test-Path $ProjectPath)) {
    Write-Host "`nConfiguring Apache virtual host..." -ForegroundColor Yellow

    $ProjectName = Split-Path $ProjectPath -Leaf
    $VhostConfig = @"
    <VirtualHost *:80>
        ServerName $ProjectName.local
        DocumentRoot "$ProjectPath"

        <Directory "$ProjectPath">
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

        ErrorLog "logs/${ProjectName}_error.log"
        CustomLog "logs/${ProjectName}_access.log" common
    </VirtualHost>
"@

    $HttpdVhostPath = "$XamppPath\apache\conf\extra\httpd-vhosts.conf"

    # Backup vhosts file
    Copy-Item $HttpdVhostPath "$HttpdVhostPath.bak_$Timestamp" -Force

    # Add virtual host
    $VhostConfig | Add-Content $HttpdVhostPath

    Write-Host "Virtual host configured: http://$ProjectName.local" -ForegroundColor Green
    Write-Host "Add '127.0.0.1 $ProjectName.local' to C:\Windows\System32\drivers\etc\hosts" -ForegroundColor Yellow
}

# Start Apache and MySQL
Write-Host "`nStarting XAMPP services..." -ForegroundColor Yellow

$XamppControl = "$XamppPath\xampp_control.exe"
if (Test-Path $XamppControl) {
    Start-Process $XamppControl
    Write-Host "XAMPP Control Panel opened" -ForegroundColor Green
} else {
    Write-Host "Starting Apache service..." -ForegroundColor Yellow
    Start-Service Apache2 -ErrorAction SilentlyContinue
    Write-Host "Starting MySQL service..." -ForegroundColor Yellow
    Start-Service MySQL -ErrorAction SilentlyContinue
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "PHP version:" -ForegroundColor Cyan
& "$XamppPath\php\php.exe" -v

Write-Host "`nTo use:" -ForegroundColor Cyan
Write-Host "  1. Place your PHP files in htdocs folder or use virtual host" -ForegroundColor White
Write-Host "  2. Access via http://localhost/your-project or http://your-project.local" -ForegroundColor White
Write-Host "  3. MySQL: username 'root', password (empty by default)" -ForegroundColor White
