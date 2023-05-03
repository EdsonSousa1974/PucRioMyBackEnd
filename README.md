# Minha API

Este pequeno projeto faz parte do MVP da  **Puc-Rio - Sprint I  - Do curso de pós graduação em Engenharia de Software** 

Este projeto visa implementar um pequeno controle financeiro e pessoal. O famoso "Pai faz o pix". Porém, nesta primeira fase será feito apenas um simples cadastro de pessoa.

---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

# python -m pip install --user virtualenv
# python -m venv env

```
(env)$ pip install -r prj_back\requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
