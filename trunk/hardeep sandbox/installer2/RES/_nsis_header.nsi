; New-style look
    !include MUI2.nsh

; Interface Settings
    !define MUI_ABORTWARNING

; Pages
    ; INSTALL
    !insertmacro MUI_PAGE_WELCOME
    !insertmacro MUI_PAGE_COMPONENTS
    !insertmacro MUI_PAGE_DIRECTORY
    !insertmacro MUI_PAGE_INSTFILES
    !insertmacro MUI_PAGE_FINISH
    
    ; UNINSTALL
    !insertmacro MUI_UNPAGE_WELCOME
    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_INSTFILES
    !insertmacro MUI_UNPAGE_FINISH
  
; Languages 
    !insertmacro MUI_LANGUAGE "English"    