# Watson Logs to Analytics 

Projeto destinado à captura dos logs de interações entre usuários finais e algum Watson Assistant.


## Início

Com uma versão maior do que a **3.5 do Python**, é aconselhável, além da instalação dos `requirements` do projeto, fazer a exportação de duas variáveis de ambiente, `WATSON_WORKSPACE_ID` e `WATSON_IAM_APIKEY` com os valores respectivos ao seu Serviço do Watson. 

Caso estas não sejam definidas, é necessário passá-las no ato da chamada das funções `get_assistant` e `get_logs`.

Para executar a aplicação, basta fazer chamada do arquivo `main.py`.

O processamento será adicionado à uma pasta, que será criada se não existir, chamada de **processing**, sucedida da data e hora do processamento.


### Instalação

Para fazer a instalação das dependências do projeto, é interessante a utilização de alguma biblioteca para **virtualização de ambientes** (p.e. virtualenv). Para instalar as dependências, execute:

```
pip install -r requirements.txt
```

## Autores

* **Eduardo Pereira** - *Dev*