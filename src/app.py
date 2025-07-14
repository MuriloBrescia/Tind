import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.exceptions import BadRequest
from agent import TindAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Initialize the agent
agent = TindAgent()

def initialize_app():
    """Initialize the application."""
    logger.info("Tind AI application starting...")
    if not agent.model_content:
        logger.warning("No model loaded - using default response generation")

# Initialize the app on startup
initialize_app()

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

@app.route("/")
def index():
    """Main page with conversation input form."""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Error rendering index page: {e}")
        flash("Error loading the page. Please try again.", "error")
        return render_template("error.html", 
                             error_code=500, 
                             error_message="Error loading page"), 500

@app.route("/get_responses", methods=["POST"])
def get_responses():
    """Generate responses for given context."""
    try:
        # Validate input
        context = request.form.get("context", "").strip()
        
        if not context:
            flash("Please enter some conversation context.", "error")
            return redirect(url_for("index"))
        
        if len(context) > 1000:  # Reasonable limit
            flash("Context is too long. Please keep it under 1000 characters.", "error")
            return redirect(url_for("index"))
        
        # Generate responses
        logger.info(f"Generating responses for context: {context[:50]}...")
        responses = agent.generate_responses(context)
        filtered_responses = agent.filter_responses(responses)
        
        if not filtered_responses:
            flash("Sorry, I couldn't generate appropriate responses. Please try again.", "error")
            return redirect(url_for("index"))
        
        return render_template("responses.html", 
                             context=context, 
                             responses=filtered_responses)
        
    except Exception as e:
        logger.error(f"Error generating responses: {e}")
        flash("An error occurred while generating responses. Please try again.", "error")
        return redirect(url_for("index"))

@app.route("/save_feedback", methods=["POST"])
def save_feedback():
    """Save user feedback on responses."""
    try:
        # Validate input
        context = request.form.get("context", "").strip()
        responses = request.form.getlist("responses")
        best_response = request.form.get("best_response", "").strip()
        
        if not all([context, responses, best_response]):
            flash("Invalid feedback data. Please try again.", "error")
            return redirect(url_for("index"))
        
        if best_response not in responses:
            flash("Invalid response selection. Please try again.", "error")
            return redirect(url_for("index"))
        
        # Save the conversation
        success = agent.save_conversation(context, responses, best_response)
        
        if success:
            flash("Thank you for your feedback! Your input helps improve our AI.", "success")
            logger.info("Feedback saved successfully")
        else:
            flash("Error saving feedback. Please try again.", "error")
            logger.error("Failed to save feedback")
        
        return redirect(url_for("index"))
        
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        flash("An error occurred while saving feedback. Please try again.", "error")
        return redirect(url_for("index"))

@app.route("/api/responses", methods=["POST"])
def api_get_responses():
    """API endpoint for getting responses (JSON)."""
    try:
        data = request.get_json()
        
        if not data or "context" not in data:
            return jsonify({"error": "Context is required"}), 400
        
        context = data["context"].strip()
        
        if not context:
            return jsonify({"error": "Context cannot be empty"}), 400
        
        if len(context) > 1000:
            return jsonify({"error": "Context too long (max 1000 characters)"}), 400
        
        # Generate responses
        responses = agent.generate_responses(context)
        filtered_responses = agent.filter_responses(responses)
        
        return jsonify({
            "context": context,
            "responses": filtered_responses,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/feedback", methods=["POST"])
def api_save_feedback():
    """API endpoint for saving feedback (JSON)."""
    try:
        data = request.get_json()
        
        required_fields = ["context", "responses", "best_response"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        context = data["context"].strip()
        responses = data["responses"]
        best_response = data["best_response"].strip()
        
        if not all([context, responses, best_response]):
            return jsonify({"error": "All fields must be non-empty"}), 400
        
        if best_response not in responses:
            return jsonify({"error": "Best response must be one of the provided responses"}), 400
        
        # Save the conversation
        success = agent.save_conversation(context, responses, best_response)
        
        if success:
            return jsonify({"success": True, "message": "Feedback saved successfully"})
        else:
            return jsonify({"error": "Failed to save feedback"}), 500
        
    except Exception as e:
        logger.error(f"API feedback error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": agent.model_content is not None
    })

@app.route("/stats")
def stats():
    """Simple stats page showing training data count."""
    try:
        training_data = agent._load_training_data()
        return render_template("stats.html", 
                             conversation_count=len(training_data))
    except Exception as e:
        logger.error(f"Error loading stats: {e}")
        flash("Error loading statistics.", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Tind AI on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
