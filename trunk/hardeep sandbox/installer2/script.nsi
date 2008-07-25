; New-style look
    !include MUI2.nsh

; Interface Settings
    !define MUI_ABORTWARNING

; Pages
    ; INSTALL
    !insertmacro MUI_PAGE_WELCOME
    ; !insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
    !insertmacro MUI_PAGE_COMPONENTS
    !insertmacro MUI_PAGE_DIRECTORY
    !insertmacro MUI_PAGE_INSTFILES
    
    ; UNINSTALL
    !insertmacro MUI_UNPAGE_WELCOME
    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_INSTFILES
  
; Languages 
    !insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "Dummy Section" SecDummy
    ReadRegStr $0 HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" 'PATH'
    MessageBox MB_OK|MB_ICONEXCLAMATION $0
SectionEnd

; Descriptions
    ; Language strings
    LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

    ; Assign language strings to sections
    !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
        !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
    !insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller Section
Section "Uninstall"
    ; FILES GO HERE
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
SectionEnd

; General
    Name "UofT Installer"
    OutFile "BUILD/Install.exe"
    InstallDir "$PROGRAMFILES\Modern UI Test"
    RequestExecutionLevel user