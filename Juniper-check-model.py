import os
import sys
import paramiko


def obtener_modelo_switch(ip, usuario, password):
    try:
        cliente = paramiko.SSHClient()
        cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente.connect(ip, username=usuario, password=password, timeout=5)

        stdin, stdout, stderr = cliente.exec_command('cli -c "show chassis hardware | match Chassis"')
        salida = stdout.read().decode()
        cliente.close()

        if "Chassis" in salida:
            modelo = salida.split("Chassis")[1].strip()
            return modelo
        else:
            return "Chassis no encontrado"

    except Exception as e:
        return f"Error: {str(e)}"

def obtener_ruta_ips():
    ruta = input("Pegá la ruta completa del archivo ips.txt:\n> ").strip()

    if not os.path.exists(ruta):
        print(f"\n❌ Archivo no encontrado en la ruta: {ruta}")
        input("Presioná ENTER para cerrar...")
        sys.exit(1)

    return ruta

def main():
    usuario = input("Usuario SSH:")
    password = input("Password SSH:")

    ruta_ips = obtener_ruta_ips()

    with open(ruta_ips, "r") as f:
        ips = [line.strip() for line in f.readlines() if line.strip()]

    with open("resultados.txt", "w") as salida:
        for ip in ips:
            print(f"Conectando a {ip}...")
            modelo = obtener_modelo_switch(ip, usuario, password)
            resultado = f"{ip} --> {modelo}"
            print(resultado)
            
            salida.write(resultado + "\n")




if __name__ == "__main__":
    main()
