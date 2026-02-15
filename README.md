# Vacinas Pets API

API REST para controle de vacinação de pets, com perfis **Clínica** e **Tutor**.

## Funcionalidades

- **Clínicas**: cadastram tutores, pets, vacinas e registram aplicações de vacina.
- **Tutores**: consultam apenas seus pets e o histórico de vacinação (somente leitura).
- Autenticação via **JWT** (obtenção e refresh de token).
- Multi-tenant: cada clínica vê apenas seus próprios dados.

## Requisitos

- Python 3.10+
- pip

## Instalação

```bash
# Criar e ativar ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/macOS

# Instalar dependências
pip install -r requirements.txt

# Migrar banco
python manage.py migrate

# Criar superusuário (opcional, para /admin)
python manage.py createsuperuser
```

## Executar

```bash
python manage.py runserver
```

- API: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/`

## Autenticação

1. Obter token: `POST /api/token/` com `username` e `password`.
2. Usar no header: `Authorization: Bearer <access>`.
3. Renovar: `POST /api/token/refresh/` com `refresh`.

## Endpoints principais

| Recurso           | Descrição                          |
|-------------------|------------------------------------|
| `GET /api/me/`    | Dados do usuário logado            |
| `/api/clinics/`   | Clínicas (apenas perfil clínica)   |
| `/api/tutors/`    | Tutores da clínica                 |
| `/api/pets/`      | Pets (clínica ou do tutor)        |
| `/api/vaccines/`  | Catálogo de vacinas                |
| `/api/clinic-vaccines/` | Vacinas da clínica          |
| `/api/vaccinations/`   | Registros de vacinação      |

As listagens usam paginação (20 itens por página).

## Docker

Requisitos: [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/).

**Imagem pronta no Docker Hub:** [carlosdiegofs/vacinas_pet](https://hub.docker.com/repository/docker/carlosdiegofs/vacinas_pet/general) — para rodar sem build: `docker run -d -p 8000:8000 carlosdiegofs/vacinas_pet:latest`. Detalhes no [DOCKER-GUIA.md](DOCKER-GUIA.md).

```bash
# Criar .env (opcional; use .env.example como base)
cp .env.example .env

# Subir a API (build local)
docker compose up -d --build

# Ver logs
docker compose logs -f web
```

- API: `http://localhost:8000/api/`
- Admin: `http://localhost:8000/admin/`

O banco SQLite fica persistido no volume (arquivo `db.sqlite3` na raiz do projeto). Para criar um superusuário após subir o container:

```bash
docker compose exec web python manage.py createsuperuser
```

Para parar:

```bash
docker compose down
```

## Variáveis de ambiente (opcional)

- `DJANGO_SECRET_KEY`: chave secreta (obrigatório em produção).
- `DJANGO_DEBUG`: `True`/`False` (padrão: True).
- `DJANGO_ALLOWED_HOSTS`: hosts permitidos, separados por vírgula.

## Licença

Uso interno / educacional.
