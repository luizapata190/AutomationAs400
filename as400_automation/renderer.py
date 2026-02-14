import os
from PIL import Image, ImageDraw, ImageFont

class AS400Renderer:
    """
    Renderiza el texto de una pantalla 5250 (24x80) a una imagen PNG profesional.
    Simula la estética de una terminal real con colores.
    """
    
    def __init__(self, font_size=18):
        self.rows = 24
        self.cols = 80
        self.font_size = font_size
        # Ajuste fino para fuentes monoespaciadas
        self.char_width = font_size // 2 + 1
        self.line_height = font_size + 2
        
        # Paleta de colores extendida 5250
        self.colors = {
            "BLACK": (0, 0, 0),
            "GREEN": (0, 255, 0),
            "WHITE": (255, 255, 255),
            "RED": (255, 0, 0),
            "CYAN": (0, 255, 255),
            "YELLOW": (255, 255, 0),
            "MAGENTA": (255, 0, 255),
            "BLUE": (0, 0, 255)
        }
        
        # Intentar cargar una fuente monoespaciada
        try:
            # Fuentes comunes en Windows que se ven bien
            font_names = ["consola.ttf", "lucon.ttf", "cour.ttf"]
            self.font = None
            for name in font_names:
                try:
                    self.font = ImageFont.truetype(name, self.font_size)
                    break
                except:
                    continue
            if not self.font:
                self.font = ImageFont.load_default()
        except:
            self.font = ImageFont.load_default()

    def _get_char_color(self, line_text, row_idx):
        """Heurística básica para asignar colores según el contenido (simulado)"""
        line_upper = line_text.upper()
        
        # Títulos principales
        if row_idx == 0 or "WELCOME" in line_upper:
            return self.colors["YELLOW"]
        
        # Etiquetas de campos
        if ":" in line_text or "USER NAME" in line_upper or "PASSWORD" in line_upper:
            return self.colors["CYAN"]
            
        # Banners decorativos
        if "====" in line_text:
            return self.colors["MAGENTA"]
            
        # Mensajes de sistema/copyright
        if "(C) COPYRIGHT" in line_upper or "F3=" in line_upper:
            return self.colors["WHITE"]
            
        # Por defecto verde terminal
        return self.colors["GREEN"]

    def render_to_image(self, screen_text, output_path):
        """
        Convierte texto de pantalla a imagen PNG con colores.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Dimensiones de la imagen con margen
        width = self.cols * self.char_width + 40
        height = self.rows * self.line_height + 40
        
        img = Image.new('RGB', (width, height), color=self.colors["BLACK"])
        draw = ImageDraw.Draw(img)
        
        # Procesar líneas
        lines = screen_text.split('\n')
        
        for r in range(min(len(lines), self.rows)):
            line = lines[r]
            y = 20 + r * self.line_height
            
            line_color = self._get_char_color(line, r)
            
            # Dibujar línea
            # Para mayor fidelidad, podríamos procesar cada carácter, 
            # pero por ahora línea por línea es eficiente y se ve bien.
            # Limpiar caracteres irrelevantes (controles que no quitamos antes)
            clean_line = "".join([c if ord(c) >= 32 else " " for c in line])
            
            # Si la línea tiene un patrón de banner (Magenta en la captura del usuario)
            if "======" in clean_line:
                # Dibujar fondo magenta para esa línea (opcional)
                # draw.rectangle([20, y, width-20, y+self.line_height], fill=self.colors["MAGENTA"])
                pass

            draw.text((20, y), clean_line, font=self.font, fill=line_color)
                    
        # Borde de la pantalla
        draw.rectangle([5, 5, width-5, height-5], outline=self.colors["BLUE"], width=1)
        
        img.save(output_path)
        return output_path
