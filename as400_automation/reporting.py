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

    def add_result(self, test_name: str, status: str, evidence: list = None):
        """
        Registra el resultado de un caso de prueba.
        
        Args:
            test_name (str): Nombre del caso de prueba.
            status (str): 'PASS' o 'FAIL'.
            evidence (list): Lista de nombres de archivos de imagen generados.
        """
        self.results.append({
            'name': test_name,
            'status': status,
            'evidence': evidence or []
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
