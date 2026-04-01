# fintrack
FinTrack – Personal finance tracker

## Architecture

```
backend/app/
├── api/              # Camada de entrada HTTP. Recebe as requisições, valida com schemas
│   │                 # e delega para os services. Não contém lógica de negócio.
│   ├── router.py
│   └── routes/
│       ├── auth.py
│       ├── health.py
│       ├── transaction.py
│       └── report.py
├── services/         # Camada de negócio. Contém as queries ao banco e as regras da
│   │                 # aplicação. Lança exceções de domínio que as rotas convertem em HTTP.
│   ├── auth_service.py
│   ├── transaction_service.py
│   ├── report_service.py
│   └── exceptions.py
├── models/           # Definição das tabelas via SQLAlchemy ORM. Também contém os enums
│   │                 # e constantes de domínio usados por cada entidade.
│   ├── user.py
│   ├── transaction.py
│   └── budget.py
├── schemas/          # Schemas Pydantic que definem o contrato da API: o que entra
│   │                 # (request) e o que sai (response) em cada endpoint.
│   ├── auth.py
│   ├── transaction.py
│   ├── report.py
│   └── budget.py
└── core/             # Infraestrutura compartilhada entre todas as camadas: conexão com
    │                 # o banco, variáveis de ambiente, segurança (JWT/bcrypt) e dependências.
    ├── db.py
    ├── settings.py
    ├── security.py
    └── dependencies.py
```
