; MySetupScript.iss
[Setup]
AppName=AnalisaSEO
AppVersion=3.0
AppPublisher=Isvandika Adisana - FT UNWIR
AppPublisherURL=https://isvandika.netlify.app
AppSupportURL=https://facebook.com/xylphyxiria
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

[Files]
; Aplikasi utama dan dependensi
Source: "Z:\SKRIPSI\SEOChecker\dist\AnalisaSEO\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Folder NLTK
Source: "Z:\SKRIPSI\SEOChecker\nltk_data\*"; DestDir: "{app}\nltk_data"; Flags: ignoreversion recursesubdirs createallsubdirs

; Icon
Source: "Z:\SKRIPSI\SEOChecker\Assets\favicon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AnalisisSEOSkripsi"; Filename: "{app}\AnalisaSEO.exe"; IconFilename: "{app}\favicon.ico"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\AnalisaSEO.exe"; Description: "{cm:LaunchProgram,AnalisisSEOSkripsi}"; Flags: nowait postinstall skipifsilent
