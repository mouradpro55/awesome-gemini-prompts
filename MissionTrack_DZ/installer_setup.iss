[Setup]
AppId={{D1A3F749-8F82-4E5F-B71A-A21E23B1C429}
AppName=MissionTrack DZ
AppVersion=1.0.0
AppPublisher=Direction des Transmissions
DefaultDirName={autopf}\MissionTrack DZ
DefaultGroupName=MissionTrack DZ
OutputDir=dist_installer
OutputBaseFilename=MissionTrack_DZ_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

VersionInfoVersion=1.0.0.0
VersionInfoCompany=Direction des Transmissions Nationales
VersionInfoDescription=MissionTrack DZ Installer
VersionInfoCopyright=Copyright (C) 2026

[Languages]
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\MissionTrack_DZ\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MissionTrack DZ"; Filename: "{app}\MissionTrack_DZ.exe"
Name: "{group}\{cm:UninstallProgram,MissionTrack DZ}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\MissionTrack DZ"; Filename: "{app}\MissionTrack_DZ.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MissionTrack_DZ.exe"; Description: "{cm:LaunchProgram,MissionTrack DZ}"; Flags: nowait postinstall skipifsilent
