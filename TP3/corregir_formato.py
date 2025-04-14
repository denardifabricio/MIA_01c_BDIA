import os
import chardet



base_path = os.path.dirname(os.path.abspath(__file__))

# Leer el archivo con BOM y escribirlo sin BOM
input_file =  os.path.join(base_path, "Datos_Ejemplo_Neo.txt")
output_file = os.path.join(base_path,"Datos_Ejemplo_Neo_formateado.txt")



with open(input_file, "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result["encoding"]
    print(f"Codificación detectada: {encoding}")



try:
    content = raw_data.decode(encoding)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Archivo convertido a UTF-8 correctamente:", output_file)
except Exception as e:
    print("Error al convertir:", e)