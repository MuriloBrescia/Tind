#!/usr/bin/env python3
"""
Executador da Aplicação Tind AI

Este script fornece uma maneira fácil de executar a aplicação Tind AI a partir da raiz do projeto.
Ele lida com a configuração de caminhos e fornece diferentes modos de execução.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Função principal do executador."""
    # Garantir que estamos na raiz do projeto
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Adicionar src ao caminho do Python
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    print("🚀 Iniciando Aplicação Tind AI...")
    print("=" * 40)
    
    # Verificar se o Flask está disponível
    try:
        import flask
        print(f"✅ Flask {flask.__version__} encontrado")
    except ImportError:
        print("❌ Flask não encontrado. Instalando...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "werkzeug"])
            print("✅ Flask instalado com sucesso")
        except subprocess.CalledProcessError:
            print("❌ Falha ao instalar Flask. Por favor, instale manualmente:")
            print("   pip install flask werkzeug")
            return 1
    
    # Importar e executar a aplicação
    try:
        from src.app import app
        print("✅ Aplicação carregada com sucesso")
        print("🌐 Iniciando servidor web...")
        print("📱 Abra seu navegador em: http://localhost:5000")
        print("⚠️  Pressione Ctrl+C para parar o servidor")
        print("=" * 40)
        
        # Executar a aplicação Flask
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())