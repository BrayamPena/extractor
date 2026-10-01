import os

def extraer_jpg_puro(ruta_entrada, ruta_salida):
    try:
        with open(ruta_entrada, 'rb') as f:
            datos = f.read()
        
        # Una imagen JPG real de cámara empieza con \xFF\xD8\xFF y termina con \xFF\xD9
        cabecera_jpg = b'\xff\xd8\xff'
        fin_jpg = b'\xff\xd9'
        
        # Buscamos la cabecera JPG saltándonos el logo falso de Keepsafe del inicio (primeros 100 bytes)
        inicio = datos.find(cabecera_jpg, 100)
        
        if inicio == -1:
            # Si no la encuentra, buscamos desde el byte 32 por si acaso
            inicio = datos.find(cabecera_jpg, 32)
            
        if inicio != -1:
            # Buscamos el final de la imagen a partir de donde empezó
            final = datos.find(fin_jpg, inicio)
            
            if final != -1:
                # Extraemos el bloque exacto de la foto original
                foto_limpia = datos[inicio:final+2]
            else:
                # Si el final no se encuentra limpio, extraemos todo el resto del archivo
                foto_limpia = datos[inicio:]
                
            with open(ruta_salida, 'wb') as f_out:
                f_out.write(foto_limpia)
            print(f"[+] ¡ÉXITO! Foto extraída directamente en: {ruta_salida}")
            return True
        else:
            # Intentemos buscar un formato PNG por si era una captura de pantalla oculta
            inicio_png = datos.find(b'\x89PNG', 32)
            if inicio_png != -1:
                with open(ruta_salida.replace('.jpg', '.png'), 'wb') as f_out:
                    f_out.write(datos[inicio_png:])
                print(f"[+] ¡ÉXITO! Captura PNG encontrada y extraída en: {ruta_salida.replace('.jpg', '.png')}")
                return True
                
            print(f"[-] No se encontró estructura de imagen oculta en: {ruta_entrada}")
            return False
            
    except Exception as e:
        print(f"[-] Error al procesar {ruta_entrada}: {e}")
        return False

# Procesar todos los archivos de la carpeta
carpeta_actual = os.getcwd()
archivos = [f for f in os.listdir(carpeta_actual) if f.endswith('.jpg') or f.endswith('.ksd')]

print(f"Escaneando {len(archivos)} archivos en busca de imágenes reales...")
contador = 0

for ARCHIVO in archivos:
    if ARCHIVO.startswith("FOTO_REAL_"):
        continue
    nombre_salida = f"FOTO_REAL_{ARCHIVO}.jpg"
    if extraer_jpg_puro(ARCHIVO, nombre_salida):
        contador += 1

print(f"\nProceso terminado. Se rescataron {contador} imágenes originales.")

