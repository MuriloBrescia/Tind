import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.exceptions import BadRequest
from agent import TindAgent

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar aplicação Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Inicializar o agente
agent = TindAgent()

def initialize_app():
    """Inicializar a aplicação."""
    logger.info("Aplicação Tind AI iniciando...")
    if not agent.model_content:
        logger.warning("Nenhum modelo carregado - usando geração de resposta padrão")

# Inicializar a aplicação na inicialização
initialize_app()

@app.errorhandler(404)
def not_found_error(error):
    """Tratar erros 404."""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Página não encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    """Tratar erros 500."""
    logger.error(f"Erro interno do servidor: {error}")
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Erro interno do servidor"), 500

@app.route("/")
def index():
    """Página principal com formulário de entrada de conversa."""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Erro ao renderizar página inicial: {e}")
        flash("Erro ao carregar a página. Por favor, tente novamente.", "error")
        return render_template("error.html", 
                             error_code=500, 
                             error_message="Erro ao carregar página"), 500

@app.route("/get_responses", methods=["POST"])
def get_responses():
    """Gerar respostas para o contexto fornecido."""
    try:
        # Validar entrada
        context = request.form.get("context", "").strip()
        
        if not context:
            flash("Por favor, digite o contexto da conversa.", "error")
            return redirect(url_for("index"))
        
        if len(context) > 1000:  # Limite razoável
            flash("Contexto muito longo. Mantenha abaixo de 1000 caracteres.", "error")
            return redirect(url_for("index"))
        
        # Gerar respostas
        logger.info(f"Gerando respostas para contexto: {context[:50]}...")
        responses = agent.generate_responses(context)
        filtered_responses = agent.filter_responses(responses)
        
        if not filtered_responses:
            flash("Desculpe, não consegui gerar respostas apropriadas. Tente novamente.", "error")
            return redirect(url_for("index"))
        
        return render_template("responses.html", 
                             context=context, 
                             responses=filtered_responses)
        
    except Exception as e:
        logger.error(f"Erro ao gerar respostas: {e}")
        flash("Ocorreu um erro ao gerar respostas. Tente novamente.", "error")
        return redirect(url_for("index"))

@app.route("/save_feedback", methods=["POST"])
def save_feedback():
    """Salvar feedback do usuário sobre as respostas."""
    try:
        # Validar entrada
        context = request.form.get("context", "").strip()
        responses = request.form.getlist("responses")
        best_response = request.form.get("best_response", "").strip()
        
        if not all([context, responses, best_response]):
            flash("Dados de feedback inválidos. Tente novamente.", "error")
            return redirect(url_for("index"))
        
        if best_response not in responses:
            flash("Seleção de resposta inválida. Tente novamente.", "error")
            return redirect(url_for("index"))
        
        # Salvar a conversa
        success = agent.save_conversation(context, responses, best_response)
        
        if success:
            flash("Obrigado pelo seu feedback! Sua contribuição ajuda a melhorar nossa IA.", "success")
            logger.info("Feedback salvo com sucesso")
        else:
            flash("Erro ao salvar feedback. Tente novamente.", "error")
            logger.error("Falha ao salvar feedback")
        
        return redirect(url_for("index"))
        
    except Exception as e:
        logger.error(f"Erro ao salvar feedback: {e}")
        flash("Ocorreu um erro ao salvar feedback. Tente novamente.", "error")
        return redirect(url_for("index"))

@app.route("/api/responses", methods=["POST"])
def api_get_responses():
    """Endpoint da API para obter respostas (JSON)."""
    try:
        data = request.get_json()
        
        if not data or "context" not in data:
            return jsonify({"erro": "Contexto é obrigatório"}), 400
        
        context = data["context"].strip()
        
        if not context:
            return jsonify({"erro": "Contexto não pode estar vazio"}), 400
        
        if len(context) > 1000:
            return jsonify({"erro": "Contexto muito longo (máximo 1000 caracteres)"}), 400
        
        # Gerar respostas
        responses = agent.generate_responses(context)
        filtered_responses = agent.filter_responses(responses)
        
        return jsonify({
            "contexto": context,
            "respostas": filtered_responses,
            "sucesso": True
        })
        
    except Exception as e:
        logger.error(f"Erro na API: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500

@app.route("/api/feedback", methods=["POST"])
def api_save_feedback():
    """Endpoint da API para salvar feedback (JSON)."""
    try:
        data = request.get_json()
        
        required_fields = ["context", "responses", "best_response"]
        if not all(field in data for field in required_fields):
            return jsonify({"erro": "Campos obrigatórios faltando"}), 400
        
        context = data["context"].strip()
        responses = data["responses"]
        best_response = data["best_response"].strip()
        
        if not all([context, responses, best_response]):
            return jsonify({"erro": "Todos os campos devem estar preenchidos"}), 400
        
        if best_response not in responses:
            return jsonify({"erro": "Melhor resposta deve ser uma das respostas fornecidas"}), 400
        
        # Salvar a conversa
        success = agent.save_conversation(context, responses, best_response)
        
        if success:
            return jsonify({"sucesso": True, "mensagem": "Feedback salvo com sucesso"})
        else:
            return jsonify({"erro": "Falha ao salvar feedback"}), 500
        
    except Exception as e:
        logger.error(f"Erro no feedback da API: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500

@app.route("/health")
def health_check():
    """Endpoint de verificação de saúde."""
    return jsonify({
        "status": "saudável",
        "modelo_carregado": agent.model_content is not None
    })

@app.route("/stats")
def stats():
    """Página simples de estatísticas mostrando contagem de dados de treinamento."""
    try:
        training_data = agent._load_training_data()
        return render_template("stats.html", 
                             conversation_count=len(training_data))
    except Exception as e:
        logger.error(f"Erro ao carregar estatísticas: {e}")
        flash("Erro ao carregar estatísticas.", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Iniciando Tind AI na porta {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
