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