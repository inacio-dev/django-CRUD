# CRUD em Django

Este projeto implementa um CRUD (Create, Read, Update, Delete) utilizando **Django**, um framework web robusto e popular para Python. A aplicação segue as melhores práticas para desenvolvimento web, com suporte para APIs RESTful e integração fácil com bancos de dados.

## O que é Django?

**Django** é um framework de alto nível para desenvolvimento rápido de aplicações web, focado na simplicidade e reutilização de componentes. Com uma comunidade ampla e recursos integrados, Django facilita o desenvolvimento de aplicações robustas e escaláveis.

Principais características:

- **Rápido**: Desenvolvimento acelerado com menos código.
- **Seguro**: Proteção integrada contra ataques como CSRF, SQL Injection, e XSS.
- **Escalável**: Adequado para projetos de qualquer tamanho.
- **Completo**: Inclui ORM, sistema de autenticação, e muito mais.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
django-CRUD-main/
├── api/                 # Endpoints e APIs RESTful
├── apps/                # Aplicativos customizados do Django
├── core/                # Configurações centrais do projeto
├── manage.py            # Gerenciador do projeto Django
├── requirements.txt     # Dependências do projeto
├── Dockerfile           # Configuração para container Docker
├── docker-compose.yml   # Orquestração de contêineres Docker
└── entrypoint.sh        # Script de inicialização para Docker
```

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados:

- **Python 3.12+**
- **PostgreSQL** ou outro banco de dados compatível
- **Docker** e **Docker Compose** (opcional, mas recomendado)

## Configuração e Execução

### 1. Clone este repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd django-CRUD-main
```

### 2. Configure o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate # No Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Antes de iniciar o projeto, configure as variáveis de ambiente. Um arquivo `.env` é necessário para armazenar essas variáveis, garantindo uma configuração consistente e segura.

Aqui está um exemplo do arquivo `.env`:

```env
URL=https://localhost:8000
COOKIE_DOMAIN=localhost
BASE_URL=${URL}/
BUCKET_URL=

SECRET_KEY=
DEBUG=True
VERSION=v1

FRONTEND_URL=
ALLOWED_HOSTS=localhost
CORS_ALLOWED_ORIGINS=${URL},${FRONTEND_URL}
CSRF_TRUSTED_ORIGINS=${CORS_ALLOWED_ORIGINS}

# Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_CONN_MAX_AGE=600
DB_POOL_SIZE=5
DB_SCHEMA=api

# Celery
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=rpc://
CELERY_NUM_CONTAINERS=7
CELERY_CPU_CORE_MULTIPLIER=1

# Redis
REDIS_URL="redis://redis:6379/1"
CACHE_TIMEOUT=900

# Email
SENDGRID_API_KEY=
EMAIL_SENDER=

# Bucket
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

A aplicação estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Usando o Docker (opcional)

Para rodar toda a aplicação com Docker:

1. **Build e inicialização dos serviços**:

   ```bash
   docker-compose up --build
   ```

2. **Acesse a aplicação**:
   Acesse [http://localhost:8000](http://localhost:8000).

## Endpoints disponíveis

A API inclui os seguintes endpoints principais:

- **GET** `/items/`: Lista todos os itens.
- **POST** `/items/`: Cria um novo item.
- **GET** `/items/{id}/`: Detalhes de um item pelo ID.
- **PUT** `/items/{id}/`: Atualiza um item pelo ID.
- **DELETE** `/items/{id}/`: Exclui um item pelo ID.

## Testes

Para executar os testes automatizados:

```bash
python manage.py test
```

Certifique-se de configurar um banco de dados para os testes no arquivo `.env`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. Este projeto segue o [Código de Conduta](https://www.contributor-covenant.org/).
