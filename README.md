## PREVIEW

![](/Gif_for_readme/Voidshells.gif)

## INDEX

- [DESCRIPTION](#description)
- [INSTALL](#install)
	- [EXAMPLES](#examples)
		- [LINUX](#Linux)
		- [WINDOWS](#windows)
	- [PARAMETERS](#parameters)
- [USAGE](#usage)

## DESCRIPTION
Voidshells is a command line tool with a friendly output that generates reverse shells, this tool provides the following features:

- Supported Operative systems: **Linux, Windows**
- Supported languages:
    - For Linux:   **Python, Php, Ruby, Perl, Bash, Nc, Msfvenom**
    - For Windows: **Nc,  Powershell, Msfvenom**
- Supported Linux shells: **sh, bash, zsh**
- Encoding types: **Base64, url**
- Encoding N times
- Syntax error checker for arguments

## INSTALL
```
git clone https://github.com/Void4m0n/Voidshells.git
cd Voidshells
pip3 install -r requirements.txt
```

## USAGE

### EXAMPLES

#### LINUX

Simple reverse shells spawn:

```
python3 Voidshell.py -i 192.168.1.1 -p 1234 -o linux -l bash -s bash
```

Reverse shells encoded in base64 and url:

```
python3 Voidshells.py -i 192.168.1.1 -p 1234 -o linux -l python -s bash -c base64 url
```

Reverse shells for Linux in multiple languages:

```
python3 Voidshells.py -i 192.168.1.1 -p 1234 -o linux -l python php bash -s bash sh
```

#### WINDOWS

Simple reverse shells spawn for windows:

```
python3 Voidshells.py -i 192.168.1.1 -p 1234 -o windows -l powershell
```

### PARAMETERS
**Required**, *Optionals*

|Parameter&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|Description|Usage|
|---------|-----------|-----|
|-h, --help|Help panel with the parameters and usage of Voidshells|-h or --help|
|**-i LHOST**| Ip of the host that will receive the connection|-i 192.168.1.1|
|**-p LPORT**|Port where the connection will be established|-p 1234| 
|**-o OS**|Operative system where the reverse shell will be executed|-o linux windows|
|**-l Language**|Language of the reverse shell|-l python php|
|*-s Linux_shell*|Linux shell type, supported ones: sh, bash, zsh |-s sh bash|
|*-pv Py_ver*|Add the version of python|-pv 3|
|*-c Encode*|Encode the payload in different formats|-c base64 url|
|*-n  N_encode* |Number of times to encode, default 1|-n 2|



 
