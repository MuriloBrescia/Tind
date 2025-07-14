import json
import logging
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import threading

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes - caminhos relativos à raiz do projeto
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH = os.path.join(_project_root, "models", "model.txt")
TRAINING_DATA_PATH = os.path.join(_project_root, "data", "training_data.json")
OFFENSIVE_WORDS = ["ódio", "matar", "morrer", "machucar", "violência", "hate", "kill", "die", "hurt", "violence"]

# Trava de thread para operações de arquivo seguras
file_lock = threading.Lock()

class TindAgent:
    """Agente de IA para gerar respostas de conversa e lidar com feedback do usuário."""
    
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        """Inicializar o agente com um modelo."""
        self.model_path = Path(model_path)
        self.model_content = self._load_model()
        
    def _load_model(self) -> Optional[str]:
        """Carregar modelo do arquivo com tratamento adequado de erros."""
        try:
            if not self.model_path.exists():
                logger.warning(f"Arquivo do modelo não encontrado em {self.model_path}")
                return None
                
            with open(self.model_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                logger.info(f"Modelo carregado com sucesso de {self.model_path}")
                return content
                
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            return None

    def generate_responses(self, context: str, num_responses: int = 5) -> List[str]:
        """Gerar respostas baseadas no contexto com lógica aprimorada."""
        if not context or not context.strip():
            return ["Eu adoraria conversar! O que está pensando?"]
            
        context_lower = context.lower().strip()
        
        # Geração de resposta mais sofisticada baseada no contexto
        if any(word in context_lower for word in ["triste", "down", "chateado", "deprimido", "sad", "upset", "depressed"]):
            responses = [
                "Sinto muito saber disso. Há algo que eu possa fazer para ajudar?",
                "É normal se sentir triste às vezes. Estou aqui para você.",
                "Mandando um abraço virtual. 🤗",
                "Estou aqui para te ouvir se quiser conversar sobre isso.",
                "Lembre-se de que esse sentimento vai passar. Você é mais forte do que imagina.",
            ]
        elif any(word in context_lower for word in ["olá", "oi", "hey", "hello", "hi"]):
            responses = [
                "Oi! Que bom te conhecer! Como está sendo seu dia?",
                "Hey! Você parece interessante - o que te trouxe aqui hoje?",
                "Olá! Estava pensando que esta conversa precisava de alguém como você.",
                "Oi! Tenho que dizer, você tem um timing perfeito. E aí?",
                "Hey! Pronto para uma conversa incrível?",
            ]
        elif any(word in context_lower for word in ["feliz", "bom", "ótimo", "incrível", "happy", "good", "great", "awesome"]):
            responses = [
                "Que maravilhoso saber disso! Sua energia positiva é contagiante.",
                "Adoro seu entusiasmo! O que está te deixando tão feliz?",
                "Seu bom humor acabou de melhorar meu dia também!",
                "Isso é incrível! Adoraria saber mais sobre o que está indo bem.",
                "Sua felicidade é contagiosa - continue espalhando essas boas vibrações!",
            ]
        else:
            # Iniciadores de conversa padrão
            responses = [
                "Isso é interessante! Me conta mais sobre isso.",
                "Acho isso fascinante. Qual é sua opinião sobre isso?",
                "Você tem uma perspectiva única. Adoraria ouvir mais.",
                "Isso chamou minha atenção. O que te fez pensar nisso?",
                "Ponto interessante! Como você chegou a essa conclusão?",
            ]
        
        # Garantir que retornamos o número solicitado de respostas
        while len(responses) < num_responses:
            responses.extend(responses[:num_responses - len(responses)])
            
        return responses[:num_responses]

    def filter_responses(self, responses: List[str]) -> List[str]:
        """Filtrar respostas potencialmente ofensivas."""
        filtered_responses = []
        
        for response in responses:
            if any(word in response.lower() for word in OFFENSIVE_WORDS):
                filtered_responses.append("Prefiro manter nossa conversa positiva e respeitosa.")
                logger.warning(f"Resposta ofensiva filtrada: {response}")
            else:
                filtered_responses.append(response)
                
        return filtered_responses

    def save_conversation(self, context: str, responses: List[str], best_response: str) -> bool:
        """Salvar dados da conversa com segurança de thread e tratamento de erros."""
        if not context or not responses or not best_response:
            logger.error("Dados de conversa inválidos fornecidos")
            return False
            
        conversation_data = {
            "context": context.strip(),
            "responses": responses,
            "best_response": best_response.strip(),
            "timestamp": self._get_timestamp()
        }
        
        try:
            with file_lock:
                # Garantir que o diretório de dados existe
                data_dir = Path(TRAINING_DATA_PATH).parent
                data_dir.mkdir(exist_ok=True)
                
                # Carregar dados existentes ou criar nova lista
                existing_data = self._load_training_data()
                existing_data.append(conversation_data)
                
                # Escrever de volta para o arquivo
                with open(TRAINING_DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
                    
                logger.info("Dados da conversa salvos com sucesso")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao salvar conversa: {e}")
            return False

    def _load_training_data(self) -> List[Dict[str, Any]]:
        """Carregar dados de treinamento existentes ou retornar lista vazia."""
        try:
            if Path(TRAINING_DATA_PATH).exists():
                with open(TRAINING_DATA_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar dados de treinamento: {e}")
            
        return []

    def _get_timestamp(self) -> str:
        """Obter timestamp atual para rastreamento de dados."""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_user_feedback_cli(self, responses: List[str]) -> Optional[str]:
        """Obter feedback do usuário via interface de linha de comando."""
        print("\nPor favor, escolha a melhor resposta:")
        for i, response in enumerate(responses, 1):
            print(f"{i}. {response}")
        print("0. Nenhuma das opções acima")

        while True:
            try:
                choice = input("\nDigite sua escolha (0-{}): ".format(len(responses)))
                choice_num = int(choice)
                
                if choice_num == 0:
                    return None
                elif 1 <= choice_num <= len(responses):
                    return responses[choice_num - 1]
                else:
                    print(f"Por favor, digite um número entre 0 e {len(responses)}")
                    
            except (ValueError, KeyboardInterrupt):
                print("Entrada inválida. Por favor, digite um número.")
                continue

def main():
    """Função principal para uso em CLI."""
    agent = TindAgent()
    
    if not agent.model_content:
        print("Aviso: Nenhum modelo carregado. Usando geração de resposta padrão.")
    
    print("Bem-vindo ao Tind AI! (Digite 'sair' para encerrar)")
    
    while True:
        try:
            context = input("\nDigite o contexto da conversa: ").strip()
            
            if context.lower() in ['sair', 'exit', 'quit', 'q']:
                print("Até logo!")
                break
                
            if not context:
                print("Por favor, digite algum contexto.")
                continue
                
            # Gerar e filtrar respostas
            responses = agent.generate_responses(context)
            filtered_responses = agent.filter_responses(responses)
            
            # Obter feedback do usuário
            best_response = agent.get_user_feedback_cli(filtered_responses)
            
            if best_response:
                success = agent.save_conversation(context, filtered_responses, best_response)
                if success:
                    print("✅ Feedback salvo com sucesso!")
                else:
                    print("❌ Erro ao salvar feedback.")
            else:
                print("Nenhuma resposta selecionada.")
                
        except KeyboardInterrupt:
            print("\nAté logo!")
            break
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            print("Ocorreu um erro. Tente novamente.")

if __name__ == "__main__":
    main()
