#!/usr/bin/env python3
"""
Módulo de fine-tuning para Tind AI

Este módulo lida com o processo de fine-tuning para o modelo de IA conversacional.
Atualmente implementa uma simulação de fine-tuning para propósitos de desenvolvimento.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes - caminhos relativos à raiz do projeto
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(_project_root, "models")
MODEL_FILE = "model.txt"
TRAINING_DATA_PATH = os.path.join(_project_root, "data", "training_data.json")
MODEL_METADATA_FILE = "model_metadata.json"

class ModelTrainer:
    """Lida com operações de treinamento e fine-tuning do modelo."""
    
    def __init__(self, model_dir: str = MODEL_DIR):
        """Inicializar o treinador com diretório do modelo."""
        self.model_dir = Path(model_dir)
        self.model_path = self.model_dir / MODEL_FILE
        self.metadata_path = self.model_dir / MODEL_METADATA_FILE
        
    def load_training_data(self) -> List[Dict[str, Any]]:
        """Carregar dados de treinamento do arquivo JSON."""
        try:
            if Path(TRAINING_DATA_PATH).exists():
                with open(TRAINING_DATA_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Carregados {len(data)} exemplos de treinamento")
                    return data
            else:
                logger.warning("Nenhum dado de treinamento encontrado")
                return []
        except Exception as e:
            logger.error(f"Erro ao carregar dados de treinamento: {e}")
            return []
    
    def analyze_training_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisar dados de treinamento para extrair insights."""
        if not data:
            return {"total_examples": 0, "contexts": [], "responses": []}
        
        contexts = [item.get('context', '') for item in data]
        all_responses = []
        best_responses = [item.get('best_response', '') for item in data]
        
        for item in data:
            all_responses.extend(item.get('responses', []))
        
        analysis = {
            "total_examples": len(data),
            "unique_contexts": len(set(contexts)),
            "total_responses": len(all_responses),
            "unique_responses": len(set(all_responses)),
            "avg_context_length": sum(len(c) for c in contexts) / len(contexts) if contexts else 0,
            "avg_response_length": sum(len(r) for r in all_responses) / len(all_responses) if all_responses else 0,
            "recent_examples": len([item for item in data if 'timestamp' in item]),
        }
        
        return analysis
    
    def create_model_metadata(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Criar metadados para o modelo treinado."""
        return {
            "model_version": f"tind-v{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "training_timestamp": datetime.now().isoformat(),
            "training_data_analysis": analysis,
            "model_type": "gerador_respostas_conversacionais",
            "framework": "simulacao_tind_ai",
            "capabilities": [
                "entendimento_contexto",
                "geracao_respostas",
                "adaptacao_tom",
                "filtragem_conteudo"
            ]
        }
    
    def fine_tune_model(self) -> bool:
        """
        Fazer fine-tuning do modelo com dados de treinamento disponíveis.
        
        Returns:
            bool: True se o fine-tuning foi bem-sucedido, False caso contrário.
        """
        try:
            logger.info("Iniciando processo de fine-tuning...")
            
            # Garantir que o diretório do modelo existe
            self.model_dir.mkdir(exist_ok=True)
            
            # Carregar e analisar dados de treinamento
            training_data = self.load_training_data()
            analysis = self.analyze_training_data(training_data)
            
            if analysis["total_examples"] == 0:
                logger.warning("Nenhum dado de treinamento disponível - criando modelo base")
                model_content = "Modelo base Tind AI - ainda sem dados de treinamento."
            else:
                logger.info(f"Treinando com {analysis['total_examples']} exemplos")
                
                # Simular melhoria do modelo baseada nos dados de treinamento
                improvement_score = min(analysis["total_examples"] * 10, 100)
                model_content = f"""Modelo Tind AI (Treinado)
Exemplos de Treinamento: {analysis['total_examples']}
Contextos Únicos: {analysis['unique_contexts']}
Melhoria do Modelo: {improvement_score}%
Última Atualização: {datetime.now().isoformat()}

Este modelo foi treinado com feedback real de usuários para fornecer melhores respostas de conversa.
Áreas de foco do treinamento:
- Entendimento de contexto e adequação das respostas
- Correspondência de tom e inteligência emocional
- Segurança de conteúdo e filtragem
- Fluxo natural de conversa
"""
            
            # Salvar o modelo
            with open(self.model_path, 'w', encoding='utf-8') as f:
                f.write(model_content)
            
            # Salvar metadados
            metadata = self.create_model_metadata(analysis)
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Fine-tuning concluído! Modelo salvo em {self.model_path}")
            logger.info(f"Metadados do modelo salvos em {self.metadata_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro durante o fine-tuning: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Obter informações sobre o modelo atual."""
        try:
            if self.metadata_path.exists():
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"status": "Nenhum metadado de modelo encontrado"}
        except Exception as e:
            logger.error(f"Erro ao ler metadados do modelo: {e}")
            return {"error": str(e)}
    
    def evaluate_model(self) -> Dict[str, Any]:
        """Avaliar o desempenho do modelo atual."""
        training_data = self.load_training_data()
        analysis = self.analyze_training_data(training_data)
        
        # Métricas de avaliação simples baseadas nos dados de treinamento
        if analysis["total_examples"] == 0:
            quality_score = 0
            readiness = "Não Pronto"
        elif analysis["total_examples"] < 5:
            quality_score = 25
            readiness = "Treinamento Inicial"
        elif analysis["total_examples"] < 10:
            quality_score = 60
            readiness = "Em Desenvolvimento"
        else:
            quality_score = min(80 + (analysis["total_examples"] - 10) * 2, 95)
            readiness = "Pronto para Produção"
        
        return {
            "quality_score": quality_score,
            "readiness_status": readiness,
            "training_examples": analysis["total_examples"],
            "model_exists": self.model_path.exists(),
            "metadata_exists": self.metadata_path.exists()
        }

def main():
    """Função principal para uso em CLI."""
    trainer = ModelTrainer()
    
    print("🤖 Treinador de Modelo Tind AI")
    print("=" * 40)
    
    # Mostrar status atual do modelo
    evaluation = trainer.evaluate_model()
    print(f"Status Atual do Modelo: {evaluation['readiness_status']}")
    print(f"Pontuação de Qualidade: {evaluation['quality_score']}%")
    print(f"Exemplos de Treinamento: {evaluation['training_examples']}")
    print()
    
    # Realizar fine-tuning
    print("Iniciando processo de fine-tuning...")
    success = trainer.fine_tune_model()
    
    if success:
        print("✅ Fine-tuning concluído com sucesso!")
        
        # Mostrar avaliação atualizada
        new_evaluation = trainer.evaluate_model()
        print(f"Pontuação de Qualidade Atualizada: {new_evaluation['quality_score']}%")
        print(f"Status do Modelo: {new_evaluation['readiness_status']}")
        
        # Mostrar informações do modelo
        model_info = trainer.get_model_info()
        if "model_version" in model_info:
            print(f"Versão do Modelo: {model_info['model_version']}")
    else:
        print("❌ Fine-tuning falhou. Verifique os logs para detalhes.")

if __name__ == "__main__":
    main()
