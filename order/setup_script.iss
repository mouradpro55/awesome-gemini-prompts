[Setup]
AppName=MissionTrack DZ
AppVersion=2.0
AppPublisher=Mourad Mesbah
DefaultDirName={autopf}\MissionTrack DZ
DefaultGroupName=MissionTrack DZ
UninstallDisplayIcon={app}\MissionTrack_DZ_Modern.exe
Compression=lzma2
SolidCompression=yes
OutputDir=Output
OutputBaseFilename=MissionTrack_DZ_Setup

[Files]
Source: "dist\MissionTrack_DZ_Modern\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Template.xlsx"; DestDir: "{app}"; Flags: ignoreversion
Source: "Amiri.ttf"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MissionTrack DZ"; Filename: "{app}\MissionTrack_DZ_Modern.exe"
Name: "{commondesktop}\MissionTrack DZ"; Filename: "{app}\MissionTrack_DZ_Modern.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\MissionTrack_DZ_Modern.exe"; Description: "Launch MissionTrack DZ"; Flags: nowait postinstall skipifsilent
