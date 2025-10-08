import cv2
import numpy as np

# Configuración inicial
cap = cv2.VideoCapture(0)
canvas = None
estela = []
max_estela_length = 30

# Solo 4 colores en la paleta
colores = [
    (0, 0, 255),    # Rojo - 1
    (0, 255, 0),    # Verde - 2  
    (255, 0, 0),    # Azul - 3
    (0, 255, 255),  # Amarillo - 4
]
nombres_colores = ['Rojo', 'Verde', 'Azul', 'Amarillo']
color_actual = 0  # Empieza con Rojo

# Rangos HSV más amplios para mejor detección
rangos_deteccion = {
    0: {  # Rojo
        'lower': np.array([0, 100, 100]),
        'upper': np.array([10, 255, 255]),
        'lower2': np.array([160, 100, 100]),
        'upper2': np.array([180, 255, 255])
    },
    1: {  # Verde
        'lower': np.array([35, 50, 50]),
        'upper': np.array([85, 255, 255])
    },
    2: {  # Azul
        'lower': np.array([90, 50, 50]),
        'upper': np.array([130, 255, 255])
    },
    3: {  # Amarillo
        'lower': np.array([15, 50, 50]),
        'upper': np.array([35, 255, 255])
    }
}

def dibujar_paleta(frame):
    altura_barra = 60
    ancho_total = frame.shape[1]
    ancho_color = ancho_total // len(colores)
    
    # Calcular margen para centrar
    margen = (ancho_total - (ancho_color * len(colores))) // 2
    
    for i, color in enumerate(colores):
        x_inicio = margen + i * ancho_color
        x_fin = margen + (i + 1) * ancho_color
        
        # Dibujar el color de la paleta
        cv2.rectangle(frame, (x_inicio, 0), (x_fin, altura_barra), color, -1)
        
        # Resaltar el color actual
        if i == color_actual:
            cv2.rectangle(frame, (x_inicio, 0), (x_fin, altura_barra), (255, 255, 255), 4)
        
        # Mostrar número del color centrado
        centro_x = x_inicio + ancho_color // 2
        centro_y = altura_barra // 2 + 5
        
        text_color = (0, 0, 0) if i == 3 else (255, 255, 255)
        cv2.putText(frame, str(i+1), (centro_x - 8, centro_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)

def detectar_color(frame, color_idx):
    """Detecta un color específico"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    rango = rangos_deteccion[color_idx]
    
    # Crear máscara
    mask1 = cv2.inRange(hsv, rango['lower'], rango['upper'])
    
    if 'lower2' in rango:
        mask2 = cv2.inRange(hsv, rango['lower2'], rango['upper2'])
        mask = mask1 + mask2
    else:
        mask = mask1
    
    # Mejorar la máscara
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(max_contour)
        if area > 100:  # Área mínima reducida
            M = cv2.moments(max_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return (cx, cy, area)
    
    return None

def verificar_cambio_color(centro_verde):
    global color_actual
    if centro_verde is None:
        return False
    
    x, y, area = centro_verde
    altura_barra = 60
    ancho_total = frame.shape[1]
    ancho_color = ancho_total // len(colores)
    margen = (ancho_total - (ancho_color * len(colores))) // 2
    
    # Verificar si está tocando la paleta
    if y < altura_barra + 50:
        color_index = (x - margen) // ancho_color
        if 0 <= color_index < len(colores):
            if color_index != color_actual:
                color_actual = color_index
                print(f"🎨 CAMBIO EXITOSO: Ahora detectando {nombres_colores[color_actual]}")
                return True
    return False

def desvanecer_estela():
    global canvas
    if canvas is not None:
        fade_mask = np.ones(canvas.shape, dtype=np.float32) * 0.98
        canvas = (canvas * fade_mask).astype(np.float32)

# Inicializar
ret, frame = cap.read()
if ret:
    canvas = np.zeros_like(frame, dtype=np.float32)

print("🎨 INICIADO - Usa objeto VERDE para tocar paleta")
print("1: Rojo, 2: Verde, 3: Azul, 4: Amarillo")

# Variables de estado
modo_seleccion = True  # Empieza en modo selección
ultimo_centro = None
frames_sin_deteccion = 0
cambio_confirmado = False  # Nueva variable para confirmar cambios

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    dibujar_paleta(frame)
    
    if modo_seleccion:
        # MODO SELECCIÓN: Solo busca VERDE para cambiar color
        centro_verde = detectar_color(frame, 1)  # Verde es índice 1
        
        if centro_verde:
            x, y, area = centro_verde
            cv2.circle(frame, (x, y), 25, (0, 255, 0), 3)
            cv2.putText(frame, "SELECTOR", (x+30, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Verificar si toca paleta
            if verificar_cambio_color(centro_verde):
                modo_seleccion = False  # Cambiar a modo dibujo
                cambio_confirmado = True  # Confirmar que se hizo un cambio
                estela.clear()
                frames_sin_deteccion = 0
                print(f"✅ Modo DIBUJO activado: {nombres_colores[color_actual]}")
        
        # MOSTRAR SOLO EN MODO SELECCIÓN
        status_text = "MODO SELECCION: Usa VERDE en paleta"
        status_color = (0, 255, 0)
    
    else:
        # MODO DIBUJO: Solo busca el COLOR ACTUAL seleccionado
        centro_color = detectar_color(frame, color_actual)
        
        if centro_color:
            x, y, area = centro_color
            cv2.circle(frame, (x, y), 20, colores[color_actual], 3)
            cv2.circle(frame, (x, y), 5, colores[color_actual], -1)
            cv2.putText(frame, f"DIBUJANDO {nombres_colores[color_actual]}", (x+30, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, colores[color_actual], 2)
            
            # Dibujar si está en área de dibujo
            if y > 80:
                estela.append((x, y))
                if len(estela) > max_estela_length:
                    estela.pop(0)
                
                # Dibujar estela
                if len(estela) >= 2:
                    for i in range(1, len(estela)):
                        thickness = max(3, int(6 * (1 - (i / len(estela)))))
                        cv2.line(canvas, estela[i-1], estela[i], colores[color_actual], thickness)
            
            ultimo_centro = centro_color
            frames_sin_deteccion = 0
        
        else:
            frames_sin_deteccion += 1
            # Si no detecta el color por muchos frames, mostrar mensaje pero NO volver a selección
            if frames_sin_deteccion < 30 and ultimo_centro:  # 30 frames de tolerancia
                x, y, area = ultimo_centro
                cv2.putText(frame, f"BUSCANDO {nombres_colores[color_actual]}...", 
                           (x+30, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colores[color_actual], 2)
        
        # SOLO volver a modo selección si el VERDE toca EXPLÍCITAMENTE la paleta DESPUÉS de un cambio confirmado
        centro_verde = detectar_color(frame, 1)
        if centro_verde and cambio_confirmado:
            x, y, area = centro_verde
            # Solo cambiar si el verde toca la parte superior de la pantalla (paleta)
            if y < 100:  
                modo_seleccion = True
                cambio_confirmado = False  # Resetear para el próximo ciclo
                print("🔄 Volviendo a MODO SELECCION")
                cv2.putText(frame, "CAMBIO DETECTADO", (x+30, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # EN MODO DIBUJO NO MOSTRAR NADA EN LA PARTE INFERIOR
        status_text = ""  # Vacío en modo dibujo
        status_color = (0, 0, 0)
    
    # Desvanecer
    desvanecer_estela()
    
    # Mostrar resultado
    canvas_uint8 = np.clip(canvas, 0, 255).astype(np.uint8)
    result = cv2.addWeighted(frame, 0.8, canvas_uint8, 0.7, 0)
    
    # Solo mostrar texto del estado si estamos en modo selección
    if modo_seleccion:
        cv2.putText(result, status_text, (10, result.shape[0]-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    
    cv2.imshow('🎨 Pintor - VERDE para cambiar color', result)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros_like(frame, dtype=np.float32)
        estela = []
        print("🧹 Limpiado")
    elif key == ord('s'):
        modo_seleccion = True
        cambio_confirmado = False
        print("🔄 Forzado modo seleccion")

cap.release()
cv2.destroyAllWindows()