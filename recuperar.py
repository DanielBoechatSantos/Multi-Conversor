import os

# Substitua "X:" pela letra do seu cartão SD
drive_letter = "F:"

# Comando para reparar o sistema de arquivos
cmd = f"chkdsk {drive_letter} /f"

# Executa o comando no terminal
os.system(cmd)
