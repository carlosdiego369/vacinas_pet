# Guia: rodar Vacinas Pets com Docker

Siga estes passos **nessa ordem**.

---

## Imagem no Docker Hub

A API também está disponível como imagem pronta no **Docker Hub**. Quem não quiser fazer build pode rodar assim:

**Imagem:** [carlosdiegofs/vacinas_pet](https://hub.docker.com/repository/docker/carlosdiegofs/vacinas_pet/general)

```powershell
docker run -d -p 8000:8000 --name vacinas_pets_web carlosdiegofs/vacinas_pet:latest
```

- API: **http://localhost:8000/api/**
- Admin: **http://localhost:8000/admin/**

Para criar usuário admin:  
`docker exec -it vacinas_pets_web python manage.py createsuperuser`

Para parar: `docker stop vacinas_pets_web`  
Para remover: `docker rm vacinas_pets_web`

*(Quem for desenvolver ou alterar o código deve usar o fluxo abaixo com build local.)*

---

## 1. Abrir o Docker Desktop

- No Windows: abra **Docker Desktop** pelo menu Iniciar.
- Espere o ícone da bandeja indicar que está rodando (às vezes leva 1–2 minutos).
- Só continue quando o Docker estiver **Running**.

---

## 2. Abrir o terminal na pasta do projeto

- Abra o **PowerShell** ou **Prompt de Comando**.
- Vá até a pasta do projeto:

```powershell
cd c:\Projetos\vacinas_pets
```

---

## 3. Fazer o build (criar a imagem)

Esse comando baixa a imagem do Python e instala as dependências. Na primeira vez pode levar alguns minutos.

```powershell
docker compose build
```

Quando terminar, deve aparecer algo como: **"Successfully built"** ou **"Successfully tagged"**.

---

## 4. Subir a API (iniciar o container)

```powershell
docker compose up -d
```

O `-d` faz rodar em segundo plano. A API sobe na porta **8000**.

---

## 5. Conferir se está rodando

- Abra o navegador em: **http://localhost:8000/api/**
- Deve aparecer uma tela de API (pode pedir login ou listar recursos).
- Admin: **http://localhost:8000/admin/**

---

## 6. Criar um usuário admin (opcional)

Para acessar o `/admin/` e criar clínicas/usuários:

```powershell
docker compose exec web python manage.py createsuperuser
```

Informe **username**, **email** e **senha** quando pedir.

---

## Comandos úteis

| O que fazer              | Comando                    |
|--------------------------|----------------------------|
| Ver logs da API          | `docker compose logs -f web` |
| Parar a API              | `docker compose down`      |
| Subir de novo            | `docker compose up -d`     |
| Rebuild após mudar código| `docker compose up -d --build` |

---

## Se der erro

- **"Docker Desktop is unable to start"**  
  Abra o **Docker Desktop** e espere ele iniciar por completo antes de rodar os comandos.

- **Porta 8000 já em uso**  
  Altere no `docker-compose.yml` a linha `"8000:8000"` para `"8001:8000"` e acesse **http://localhost:8001/api/**.

- **Erro de permissão no banco**  
  Na pasta do projeto, crie o arquivo do banco (se ainda não existir):
  ```powershell
  New-Item -ItemType File -Path db.sqlite3 -Force
  ```
  Depois rode de novo: `docker compose up -d`.

- **"Web" fica em loading ou container reiniciando / aviso de migrações**  
  Pode ser migração pendente. Pare o container, reconstrua a imagem e suba de novo para aplicar as migrações:
  ```powershell
  docker compose down
  docker compose up -d --build
  ```
  Aguarde ~30 segundos e confira de novo em http://localhost:8000/admin/
