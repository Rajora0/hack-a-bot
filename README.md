# API de Exemplo

Esta aplicação utiliza a API GPT-3.5 da OpenAI para analisar e fornecer informações sobre um texto enviado pelo usuário. A aplicação é baseada na linguagem Python e utiliza o micro-framework Flask para criar uma API e uma interface web simples.

## Requisitos

- Python 3.7+
- Flask
- Flask-RESTful
- Flask-Swagger-UI
- OpenAI

## Instalação

1. Faça download dos arquivos.

2. Entre no diretório do projeto:

```
cd projeto_glard
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Configure a variável de ambiente `OPENAI_API_KEY` com sua chave de API da OpenAI:

- No Linux ou macOS:

```bash
export OPENAI_API_KEY="sua_chave_de_api_aqui"
```

- No Windows (PowerShell):

```powershell
$env:OPENAI_API_KEY = "sua_chave_de_api_aqui"
```

5. Execute a aplicação:

```
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

## Uso

A aplicação possui duas rotas principais:

1. A rota principal (`/`) exibe um formulário onde o usuário pode inserir um texto. Após o envio, a aplicação exibirá informações sobre o texto, como resumo, identificação do problema, análise de sentimento, tópicos relevantes e sugestão de solução.

2. A rota `/api/dados/<string:texto>` recebe um texto como parâmetro e retorna as informações em formato JSON.

Além disso, a aplicação possui uma documentação gerada pelo Swagger UI, que pode ser acessada em `/swagger`.

## Contribuindo

Se você encontrou algum erro ou deseja propor melhorias, sinta-se à vontade.
