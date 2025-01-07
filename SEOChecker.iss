; testingproduction.iss
[Setup]
AppName=AnalisaSEO
AppVersion=3.0-beta
AppPublisher=Isvandika Adisana - FT UNWIR
AppPublisherURL=https://isvandika.netlify.app
AppSupportURL=https://github.com/XYLxiria
AppUpdatesURL=https://github.com/XYLxiria
DefaultDirName={commonpf}\AnalisisSEOSkripsi
DefaultGroupName=AnalisisSEOSkripsi
OutputDir=Output
OutputBaseFilename=SEOAnalyzerInstallerV3.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
WizardImageFile=Z:\SKRIPSI\SEOChecker\Assets\installer_image.bmp
WizardSmallImageFile=Z:\SKRIPSI\SEOChecker\Assets\installer_small_image.bmp
SetupIconFile=Z:\SKRIPSI\SEOChecker\Assets\favicon.ico
LicenseFile=Z:\SKRIPSI\SEOChecker\Assets\license.txt
PrivilegesRequired=admin
VersionInfoVersion=3.0.0.0
VersionInfoDescription=Python AI-based SEO analysis desktop application
VersionInfoCompany=Isvandika Adisana - FT UNWIR
VersionInfoProductName=AnalisaSEO


[Files]
; Aplikasi utama dan dependensi
Source: "Z:\SKRIPSI\SEOChecker\dist\AnalisaSEO\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Folder NLTK
Source: "Z:\SKRIPSI\SEOChecker\nltk_data\*"; DestDir: "{app}\nltk_data"; Flags: ignoreversion recursesubdirs createallsubdirs

; Icon
Source: "Z:\SKRIPSI\SEOChecker\Assets\favicon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AnalisisSEO"; Filename: "{app}\AnalisaSEO.exe"; IconFilename: "{app}\favicon.ico"
Name: "{userdesktop}\AnalisisSEO"; Filename: "{app}\AnalisaSEO.exe"; IconFilename: "{app}\favicon.ico"; WorkingDir: "{app}"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\AnalisaSEO.exe"; Description: "{cm:LaunchProgram,AnalisisSEOSkripsi}"; Flags: nowait postinstall skipifsilent runasoriginaluser
