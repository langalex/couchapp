; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{0CDA65F1-9FD8-42C5-8DD0-F65F7E8B7304}
AppName=Couchapp
AppVerName=Couchapp 0.5
AppPublisher=Beno�t Chesneau
AppPublisherURL=http://benoitc.github.com/couchapp
AppSupportURL=http://benoitc.github.com/couchapp
AppUpdatesURL=http://benoitc.github.com/couchapp
DefaultDirName={pf}\Couchapp
DefaultGroupName=Couchapp
LicenseFile=LICENSE
InfoAfterFile=contrib\win32\postinstall.txt
OutputBaseFilename=couchapp-0.5
Compression=lzma
SolidCompression=yes
SourceDir=..\..

[Languages]
Name: english; MessagesFile: compiler:Default.isl

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked

[Files]
Source: dist\couchapp.exe; DestDir: {app}; Flags: ignoreversion
Source: dist\_hashlib.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\_socket.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\_ssl.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\_win32sysloader.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\API-MS-Win-Core-LocalRegistry-L1-1-0.dll; DestDir: {app}; Flags: ignoreversion
Source: dist\API-MS-Win-Core-ProcessThreads-L1-1-0.dll; DestDir: {app}; Flags: ignoreversion
Source: dist\API-MS-Win-Security-Base-L1-1-0.dll; DestDir: {app}; Flags: ignoreversion
Source: dist\bz2.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\couchapp.exe; DestDir: {app}; Flags: ignoreversion
Source: dist\library.zip; DestDir: {app}; Flags: ignoreversion
Source: dist\POWRPROF.dll; DestDir: {app}; Flags: ignoreversion
Source: dist\python26.dll; DestDir: {app}; Flags: ignoreversion
Source: dist\pythoncom26.dll; DestDir: {app}; Flags: ignoreversion
Source: dist\pywintypes26.dll; DestDir: {app}; Flags: ignoreversion
Source: dist\select.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\unicodedata.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\w9xpopen.exe; DestDir: {app}; Flags: ignoreversion
Source: dist\win32api.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\win32com.shell.shell.pyd; DestDir: {app}; Flags: ignoreversion
Source: dist\couchapp\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\Microsoft.VC*.CRT.manifest; DestDir: {app}; Flags: ignoreversion
Source: dist\Microsoft.VC*.MFC.manifest; DestDir: {app}
Source: dist\mfc*.dll; DestDir: {app}
Source: dist\msvc*.dll; DestDir: {app}
Source: dist\add_path.exe; DestDir: {app}
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: {group}\Couchapp; Filename: {app}\couchapp.exe
Name: {commondesktop}\Couchapp; Filename: {app}\couchapp.exe; Tasks: desktopicon

[Run]
Filename: {app}\add_path.exe; Parameters: {app}; Description: Add the installation path to the search path; Flags: postinstall

[UninstallRun]
Filename: {app}\add_path.exe; Parameters: /del {app}
