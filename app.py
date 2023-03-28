from gpt import text_suporte

from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

# Configuração do Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Exemplo"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Rota para a página estática com o formulário
@app.route('/', methods=['GET', 'POST'], endpoint='submit_form')
def index():
    resultado = None
    if request.method == 'POST':
    
        campo_texto = request.form['campo_texto']
        
        resultado_api = text_suporte(campo_texto)

        # Aqui você pode fazer a chamada para a API e obter os dados em JSON
        resultado = {
            "texto_enviado": campo_texto,      	
            "resume": resultado_api["resume"],
            "problem_identification": resultado_api["problem_identification"],
            "sentiment_analysis": resultado_api["sentiment_analysis"],
            "relevant_topics": resultado_api["relevant_topics"],
            "solution_suggestion": resultado_api["solution_suggestion"],
            "template_response": resultado_api["template_response"]
        }
        
    return render_template('index.html', resultado=resultado)

# Rota para a API que retorna os dados em JSON
class DadosAPI(Resource):
    def get(self, texto):
        return text_suporte(texto)

api.add_resource(DadosAPI, '/api/dados/<string:texto>')

if __name__ == '__main__':
    app.run(debug=True)
