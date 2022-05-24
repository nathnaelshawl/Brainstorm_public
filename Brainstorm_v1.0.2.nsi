; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Brainstorm"
!define PRODUCT_VERSION "1.0.2"
!define PRODUCT_PUBLISHER "Nathnael Shawl"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\Brainstorm.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\Brainstorm_1.0.1\Icons\app_icons\BrainstormInstallIcon.ico"
!define MUI_UNICON "Icons\app_icons\BrainstormUninstallIcon.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "license_agreement\license_agreement.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\Brainstorm.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Brainstorm_v1.0.2_installer.exe"
InstallDir "$PROGRAMFILES\Brainstorm"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite try
  File "Brainstorm.exe"
  CreateDirectory "$SMPROGRAMS\Brainstorm"
  CreateShortCut "$SMPROGRAMS\Brainstorm\Brainstorm.lnk" "$INSTDIR\Brainstorm.exe"
  CreateShortCut "$DESKTOP\Brainstorm.lnk" "$INSTDIR\Brainstorm.exe"
  SetOutPath "$INSTDIR\fonts"
  File "fonts\OpenSans-Bold.ttf"
  File "fonts\OpenSans-BoldItalic.ttf"
  File "fonts\OpenSans-ExtraBold.ttf"
  File "fonts\OpenSans-ExtraBoldItalic.ttf"
  File "fonts\OpenSans-Italic.ttf"
  File "fonts\OpenSans-Light.ttf"
  File "fonts\OpenSans-LightItalic.ttf"
  File "fonts\OpenSans-Regular.ttf"
  File "fonts\OpenSans-Semibold.ttf"
  File "fonts\OpenSans-SemiboldItalic.ttf"
  SetOutPath "$INSTDIR\Icons\app_icons"
  File "Icons\app_icons\BrainstormInstallIcon.ico"
  File "Icons\app_icons\BrainstormInstallIcon.png"
  File "Icons\app_icons\BrainstormUninstallIcon.ico"
  File "Icons\app_icons\BrainstormUninstallIcon.png"
  SetOutPath "$INSTDIR\Icons\button_icons"
  File "Icons\button_icons\bezier.png"
  File "Icons\button_icons\centerrectangle.png"
  File "Icons\button_icons\circle.png"
  File "Icons\button_icons\clear.png"
  File "Icons\button_icons\elipse.png"
  File "Icons\button_icons\eraserpaint.png"
  File "Icons\button_icons\exit.png"
  File "Icons\button_icons\eyedropper.png"
  File "Icons\button_icons\filltool.png"
  File "Icons\button_icons\line.png"
  File "Icons\button_icons\marker.png"
  File "Icons\button_icons\new.png"
  File "Icons\button_icons\open.png"
  File "Icons\button_icons\pencil.png"
  File "Icons\button_icons\polygon.png"
  File "Icons\button_icons\polyline.png"
  File "Icons\button_icons\quitCheck.png"
  File "Icons\button_icons\rectangle.png"
  File "Icons\button_icons\redo.png"
  File "Icons\button_icons\redoinactive.png"
  File "Icons\button_icons\save.png"
  File "Icons\button_icons\saveas.png"
  File "Icons\button_icons\saveunavilable.png"
  File "Icons\button_icons\square.png"
  File "Icons\button_icons\undo.png"
  File "Icons\button_icons\undoinactive.png"
  SetOutPath "$INSTDIR\Icons\link_icons"
  File "Icons\link_icons\Linkedin_logo.png"
  File "Icons\link_icons\Telegram_logo.png"
  File "Icons\link_icons\Youtube_logo.png"
  SetOutPath "$INSTDIR\license_agreement"
  File "license_agreement\license_agreement.txt"
  SetOutPath "$INSTDIR\sample_files(Brainstorm)"
  File "sample_files(Brainstorm)\drawing.jpg"
  File "sample_files(Brainstorm)\drawing1.jpg"
  File "sample_files(Brainstorm)\drawing3.jpg"
  File "sample_files(Brainstorm)\peach_phone.png"
  File "sample_files(Brainstorm)\Sample_Image.png"
  File "sample_files(Brainstorm)\sample_image2.png"
  File "sample_files(Brainstorm)\sample_image3.png"
  File "sample_files(Brainstorm)\sample_image4.png"
  File "sample_files(Brainstorm)\sample_image5.png"
  File "sample_files(Brainstorm)\zoro.png"
SectionEnd

Section -AdditionalIcons
  SetOutPath $INSTDIR
  CreateShortCut "$SMPROGRAMS\Brainstorm\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\Brainstorm.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\Brainstorm.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "Brainstorm was successfully removed from your. Thankyou for using Brainstorm!!!"
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove Brainstorm and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\sample_files(Brainstorm)\zoro.png"
  Delete "$INSTDIR\sample_files(Brainstorm)\sample_image5.png"
  Delete "$INSTDIR\sample_files(Brainstorm)\sample_image4.png"
  Delete "$INSTDIR\sample_files(Brainstorm)\sample_image3.png"
  Delete "$INSTDIR\sample_files(Brainstorm)\sample_image2.png"
  Delete "$INSTDIR\sample_files(Brainstorm)\Sample_Image.png"
  Delete "$INSTDIR\sample_files(Brainstorm)\peach_phone.png"
  Delete "$INSTDIR\sample_files(Brainstorm)\drawing3.jpg"
  Delete "$INSTDIR\sample_files(Brainstorm)\drawing1.jpg"
  Delete "$INSTDIR\sample_files(Brainstorm)\drawing.jpg"
  Delete "$INSTDIR\license_agreement\license_agreement.txt"
  Delete "$INSTDIR\Icons\link_icons\Youtube_logo.png"
  Delete "$INSTDIR\Icons\link_icons\Telegram_logo.png"
  Delete "$INSTDIR\Icons\link_icons\Linkedin_logo.png"
  Delete "$INSTDIR\Icons\button_icons\undoinactive.png"
  Delete "$INSTDIR\Icons\button_icons\undo.png"
  Delete "$INSTDIR\Icons\button_icons\square.png"
  Delete "$INSTDIR\Icons\button_icons\saveunavilable.png"
  Delete "$INSTDIR\Icons\button_icons\saveas.png"
  Delete "$INSTDIR\Icons\button_icons\save.png"
  Delete "$INSTDIR\Icons\button_icons\redoinactive.png"
  Delete "$INSTDIR\Icons\button_icons\redo.png"
  Delete "$INSTDIR\Icons\button_icons\rectangle.png"
  Delete "$INSTDIR\Icons\button_icons\quitCheck.png"
  Delete "$INSTDIR\Icons\button_icons\polyline.png"
  Delete "$INSTDIR\Icons\button_icons\polygon.png"
  Delete "$INSTDIR\Icons\button_icons\pencil.png"
  Delete "$INSTDIR\Icons\button_icons\open.png"
  Delete "$INSTDIR\Icons\button_icons\new.png"
  Delete "$INSTDIR\Icons\button_icons\marker.png"
  Delete "$INSTDIR\Icons\button_icons\line.png"
  Delete "$INSTDIR\Icons\button_icons\filltool.png"
  Delete "$INSTDIR\Icons\button_icons\eyedropper.png"
  Delete "$INSTDIR\Icons\button_icons\exit.png"
  Delete "$INSTDIR\Icons\button_icons\eraserpaint.png"
  Delete "$INSTDIR\Icons\button_icons\elipse.png"
  Delete "$INSTDIR\Icons\button_icons\clear.png"
  Delete "$INSTDIR\Icons\button_icons\circle.png"
  Delete "$INSTDIR\Icons\button_icons\centerrectangle.png"
  Delete "$INSTDIR\Icons\button_icons\bezier.png"
  Delete "$INSTDIR\Icons\app_icons\BrainstormUninstallIcon.png"
  Delete "$INSTDIR\Icons\app_icons\BrainstormUninstallIcon.ico"
  Delete "$INSTDIR\Icons\app_icons\BrainstormInstallIcon.png"
  Delete "$INSTDIR\Icons\app_icons\BrainstormInstallIcon.ico"
  Delete "$INSTDIR\fonts\OpenSans-SemiboldItalic.ttf"
  Delete "$INSTDIR\fonts\OpenSans-Semibold.ttf"
  Delete "$INSTDIR\fonts\OpenSans-Regular.ttf"
  Delete "$INSTDIR\fonts\OpenSans-LightItalic.ttf"
  Delete "$INSTDIR\fonts\OpenSans-Light.ttf"
  Delete "$INSTDIR\fonts\OpenSans-Italic.ttf"
  Delete "$INSTDIR\fonts\OpenSans-ExtraBoldItalic.ttf"
  Delete "$INSTDIR\fonts\OpenSans-ExtraBold.ttf"
  Delete "$INSTDIR\fonts\OpenSans-BoldItalic.ttf"
  Delete "$INSTDIR\fonts\OpenSans-Bold.ttf"
  Delete "$INSTDIR\Brainstorm.exe"

  Delete "$SMPROGRAMS\Brainstorm\Uninstall.lnk"
  Delete "$DESKTOP\Brainstorm.lnk"
  Delete "$SMPROGRAMS\Brainstorm\Brainstorm.lnk"

  RMDir "$SMPROGRAMS\Brainstorm"
  RMDir "$INSTDIR\sample_files(Brainstorm)"
  RMDir "$INSTDIR\license_agreement"
  RMDir "$INSTDIR\Icons\link_icons"
  RMDir "$INSTDIR\Icons\button_icons"
  RMDir "$INSTDIR\Icons\app_icons"
  RMDir "$INSTDIR\fonts"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd