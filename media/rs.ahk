^+d::  ; Hotkey for Ctrl+Shift+D
    SetTitleMatchMode, 2

    ; Check if Luna for Reddit is open
    IfWinNotExist, Luna For Reddit Version 1.4.4. By Nathan Tech.
    {
        return  ; Pass the shortcut to the OS
    }

    ; Check if Be My Eyes is open
    IfWinNotExist, Be My Eyes
    {
        MsgBox, Please Open Be My Eyes.
        return  ; Pass the shortcut to the OS after displaying the message
    }

    RetryCount := 0
    MaxRetries := 3

    Loop
    {
        ; Check the read-only edit control
        ControlGetText, EditText, Edit1, Luna For Reddit Version 1.4.3. By Nathan Tech.

        ; Regex to match URL until encountering ")"
        If RegExMatch(EditText, "https?://[^)]+", URL)
        {
            Clipboard := URL
            ; Send Ctrl+Alt+L to invoke Be My AI
            Send ^!l
            break  ; Exit the loop but not the script
        }

        RetryCount++
        ; Exit the loop if maximum retries reached
        If (RetryCount >= MaxRetries)
        {
            break
        }

        Sleep, 500  ; Wait before retrying
    }
return

; Automatically exit the script when the parent window is closed
#Persistent
SetTimer, CheckWindows, 1000
return

CheckWindows:
    IfWinNotExist, Luna For Reddit Version 1.4.3. By Nathan Tech.
    {
        ExitApp
    }
    ; Also exit if Be My Eyes is closed
    IfWinNotExist, Be My Eyes
    {
        ExitApp
    }
return
