$cert = Get-ChildItem -Path Cert:\CurrentUser\My -CodeSigningCert | Where-Object {$_.Subject -like "*DTN El Meniaa*" } | Select-Object -First 1
if (-not $cert) {
    $cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=DTN El Meniaa, O=Direction des Transmissions Nationales, C=DZ" -CertStoreLocation "Cert:\CurrentUser\My"
}
Set-AuthenticodeSignature -FilePath "dist\MissionTrack_DZ\MissionTrack_DZ.exe" -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
if (Test-Path "dist_installer\MissionTrack_DZ_Setup.exe") {
    Set-AuthenticodeSignature -FilePath "dist_installer\MissionTrack_DZ_Setup.exe" -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
}
