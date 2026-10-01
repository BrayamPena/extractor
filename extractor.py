import os
import zlib

def reparar_archivo(ruta_entrada, ruta_salida):
    try:
        with open(ruta_entrada, 'rb') as f:
            datos = f.read()
        
        # El logo PNG suele ocupar los primeros bytes.
        # Buscamos las firmas de compresión Zlib comunes (78 01, 78 9C, 78 DA)
        firmas_zlib = [b'\x78\x01', b'\x78\x9c', b'\x78\xda']
        
        inicio_zlib = -1
        for firma in firmas_zlib:
            # Empezamos a buscar después del byte 32 para saltarnos el logo PNG básico
            pos = datos.find(firma, 32)
            if pos != -1:
                inicio_zlib = pos
                break 
                
        if inicio_zlib == -1:
            print(f"[-] No se encontró compresión válida en: {ruta_entrada}")
            return False

        # Intentamos descomprimir el bloque a partir de la firma encontrada
        try:
            datos_descomprimidos = zlib.decompress(datos[inicio_zlib:])
            with open(ruta_salida, 'wb') as f_out:
                f_out.write(datos_descomprimidos)
            print(f"[+] ¡ÉXITO! Recuperado: {ruta_salida}")
            return True
        except zlib.error:
            # Si falla el header estricto, intentamos con modo raw (ignora los bytes del header zlib)
            try:
                datos_descomprimidos = zlib.decompress(datos[inicio_zlib:], -zlib.MAX_WBITS)
                with open(ruta_salida, 'wb') as f_out:
                    f_out.write(datos_descomprimidos)
                print(f"[+] ¡ÉXITO (Modo Raw)! Recuperado: {ruta_salida}")
                return True
            except Exception as e:
                print(f"[-] Error al descomprimir {ruta_entrada}: {e}")
                return False
    except Exception as e:
        print(f"[-] No se pudo leer {ruta_entrada}: {e}")
        return False

# Procesar todos los archivos .jpg o .ksd de la carpeta actual
carpeta_actual = os.getcwd()
archivos = [f for f in os.listdir(carpeta_actual) if f.endswith('.jpg') or f.endswith('.ksd')]

print(f"Encontrados {len(archivos)} archivos para procesar...")
contador = 0

for ARCHIVO in archivos:
    # Evitar procesar los ya recuperados
    if ARCHIVO.startswith("RECUPERADA_"):
        continue
    nombre_salida = f"RECUPERADA_{ARCHIVO}.jpg"
    if reparar_archivo(ARCHIVO, nombre_salida):
        contador += 1

print(f"\nProceso terminado. Se recuperaron exitosamente {contador} fotos.")
