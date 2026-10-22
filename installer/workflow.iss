#define AppVersion "0.3.1"
[Setup]
AppId=CCDASTRO.saspro.Workflow
AppName=CCDASTRO SASpro Workflow
AppVersion={#AppVersion}
AppPublisher=CCDASTRO, Inc.
AppPublisherURL=https://ccdastro.com/
AppSupportURL=https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/issues
AppUpdatesURL=https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases
DefaultDirName={localappdata}\SASpro\scripts\CCDASTROWorkflow
DisableDirPage=yes
DefaultGroupName=CCDASTRO SASpro Workflow
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=CCDASTRO-SASpro-Workflow-{#AppVersion}-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
#ifdef TestBuild
UninstallFilesDir={app}\.uninstall
#else
UninstallFilesDir={localappdata}\CCDASTRO\SASproWorkflowInstaller
#endif
CloseApplications=no
RestartApplications=no
SetupLogging=yes
#ifdef TestBuild
Uninstallable=yes
CreateUninstallRegKey=no
#endif
[Files]
Source: "..\CCDASTRO_SASpro_Workflow.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\ccdastro_saspro\*.py"; DestDir: "{app}\ccdastro_saspro"; Flags: ignoreversion
Source: "..\presets\*.json"; DestDir: "{app}\presets"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\INSTALL.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\INSTALL-WINDOWS.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\THIRD_PARTY_NOTICES.md"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
#ifndef TestBuild
Name: "{group}\Installation guide"; Filename: "{app}\INSTALL-WINDOWS.txt"
Name: "{group}\Downloads and updates"; Filename: "https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"
#endif
[Run]
Filename: "{app}\INSTALL-WINDOWS.txt"; Description: "Read installation and launch instructions"; Flags: postinstall shellexec skipifsilent
[Code]
function HostIsRunning(): Boolean;
var Locator, Service, Processes: Variant;
begin
#ifdef TestBuild
  Result := False;
#else
  try
    Locator := CreateOleObject('WbemScripting.SWbemLocator');
    Service := Locator.ConnectServer('', 'root\CIMV2');
    Processes := Service.ExecQuery('SELECT Name FROM Win32_Process WHERE Name = ''setiastrosuitepro.exe''');
    Result := Processes.Count > 0;
  except
    RaiseException('Unable to check whether the host is running. Close the host and try the installer again.');
  end;
#endif
end;
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  if HostIsRunning() then
    Result := 'Close Seti Astro Suite Pro and its workflow windows, then click Install again. No application will be closed automatically.';
end;
function InitializeUninstall(): Boolean;
begin
  Result := not HostIsRunning();
  if not Result then MsgBox('Close Seti Astro Suite Pro before uninstalling this workflow.', mbInformation, MB_OK);
end;
