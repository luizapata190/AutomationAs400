import os
from datetime import datetime

class AS400Reporter:
    """
    Componente reutilizable para reportar resultados de pruebas y gestionar evidencias.
    Permite centralizar estadísticas y visualización de resultados.
    """
    
    def __init__(self, evidence_dir: str = "evidence"):
        self.evidence_dir = evidence_dir
        self.results = [] # Lista de tuplas (test_name, status, evidence_list)
        self.start_time = datetime.now()
        
        if not os.path.exists(self.evidence_dir):
            os.makedirs(self.evidence_dir, exist_ok=True)

    def add_result(self, test_name: str, status: str, evidence: list = None, details: str = None):
        """
        Registra el resultado de un caso de prueba.
        
        Args:
            test_name (str): Nombre del caso de prueba.
            status (str): 'PASS' o 'FAIL'.
            evidence (list): Lista de nombres de archivos de imagen generados.
            details (str): Mensaje de error o log detallado (opcional).
        """
        self.results.append({
            'name': test_name,
            'status': status,
            'evidence': evidence or [],
            'details': details
        })

    def get_stats(self):
        """Retorna estadísticas básicas de la ejecución."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'success_rate': success_rate
        }

    def generate_console_report(self):
        """Imprime un reporte detallado y profesional en la consola."""
        stats = self.get_stats()
        
        print("\n" + "="*80)
        print("📊 REPORTE DE EJECUCIÓN AS400 AUTOMATION")
        print("="*80)
        print(f"Fecha/Hora:       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Directorio Ev:    {os.path.abspath(self.evidence_dir)}")
        print("-" * 80)
        print(f"Total Pruebas:    {stats['total']}")
        print(f"✅ Pasadas:       {stats['passed']}")
        print(f"❌ Fallidas:      {stats['failed']}")
        print(f"📈 Tasa de Éxito: {stats['success_rate']:.1f}%")
        print("="*80)
        
        for i, res in enumerate(self.results, 1):
            icon = "✅" if res['status'] == 'PASS' else "❌"
            print(f"{i}. {icon} {res['name']} [{res['status']}]")
            if res['evidence']:
                print(f"   📸 Evidencia: {', '.join(res['evidence'])}")
        
        print("="*80 + "\n")

    def save_summary_file(self, filename: str = "last_run_summary.txt"):
        """Guarda el reporte en un archivo de texto."""
        path = os.path.join(self.evidence_dir, filename)
        stats = self.get_stats()
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"REPORTE DE EJECUCIÓN - {datetime.now()}\n")
            f.write("="*40 + "\n")
            f.write(f"Total: {stats['total']} | Pasadas: {stats['passed']} | Fallidas: {stats['failed']}\n")
            f.write(f"Tasa de Éxito: {stats['success_rate']:.1f}%\n")
            f.write("-" * 40 + "\n")
            for res in self.results:
                f.write(f"[{res['status']}] {res['name']}\n")
                if res['evidence']:
                    f.write(f"  Ev: {', '.join(res['evidence'])}\n")
        return path

    def generate_html_report(self, filename: str = "reporte_visual.html"):
        """
        Genera un reporte HTML profesional con diseño moderno y evidencias integradas.
        """
        path = os.path.join(self.evidence_dir, filename)
        stats = self.get_stats()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte AS400 Automation</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --primary: #38bdf8;
            --success: #10b981;
            --fail: #ef4444;
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 2rem;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid #334155;
            padding-bottom: 1rem;
        }}
        h1 {{ margin: 0; font-size: 1.5rem; color: var(--primary); }}
        .timestamp {{ color: var(--text-muted); font-size: 0.9rem; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .stat-card {{
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #334155;
        }}
        .stat-value {{ font-size: 2rem; font-weight: 700; display: block; }}
        .stat-label {{ color: var(--text-muted); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1px; }}
        
        .test-case {{
            background: var(--card-bg);
            border-radius: 12px;
            margin-bottom: 1rem;
            overflow: hidden;
            border: 1px solid #334155;
        }}
        .test-header {{
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255,255,255,0.03);
        }}
        .status-badge {{
            padding: 4px 12px;
            border-radius: 99px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .status-PASS {{ background: rgba(16, 185, 129, 0.2); color: var(--success); }}
        .status-FAIL {{ background: rgba(239, 68, 68, 0.2); color: var(--fail); }}
        
        .test-details {{
            padding: 1rem 1.5rem;
            background: rgba(0,0,0,0.2);
            border-top: 1px solid #334155;
            font-size: 0.85rem;
            color: #cbd5e1;
            white-space: pre-wrap;
            font-family: 'Courier New', Courier, monospace;
        }}
        
        .evidence-grid {{
            padding: 1.5rem;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
        }}
        .img-container {{
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #334155;
            transition: transform 0.2s;
        }}
        .img-container:hover {{ transform: scale(1.05); cursor: pointer; }}
        .img-container img {{ width: 100%; display: block; }}
        .img-label {{
            background: #0f172a;
            padding: 4px 8px;
            font-size: 0.7rem;
            color: var(--text-muted);
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AS400 Automation Report</h1>
            <div class="timestamp">Ejecutado el: {now}</div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-value">{stats['total']}</span>
                <span class="stat-label">Total</span>
            </div>
            <div class="stat-card" style="border-left: 4px solid var(--success)">
                <span class="stat-value" style="color: var(--success)">{stats['passed']}</span>
                <span class="stat-label">Pasados</span>
            </div>
            <div class="stat-card" style="border-left: 4px solid var(--fail)">
                <span class="stat-value" style="color: var(--fail)">{stats['failed']}</span>
                <span class="stat-label">Fallidos</span>
            </div>
            <div class="stat-card">
                <span class="stat-value" style="color: var(--primary)">{stats['success_rate']:.1f}%</span>
                <span class="stat-label">Éxito</span>
            </div>
        </div>

        <div class="results-list">
        """
        
        for res in self.results:
            status_class = f"status-{res['status']}"
            html_template += f"""
            <div class="test-case">
                <div class="test-header">
                    <strong>{res['name']}</strong>
                    <span class="status-badge {status_class}">{res['status']}</span>
                </div>
            """
            
            # Nueva sección de Detalles/Logs
            if res.get('details'):
                html_template += f"""
                <div class="test-details">{res['details']}</div>
                """
                
            if res['evidence']:
                html_template += '<div class="evidence-grid">'
                for img in res['evidence']:
                    html_template += f"""
                    <div class="img-container">
                        <img src="{img}" alt="{img}">
                        <div class="img-label">{img}</div>
                    </div>
                    """
                html_template += '</div>'
            html_template += '</div>'
            
        html_template += """
        </div>
    </div>
</body>
</html>
        """
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_template)
        return path
