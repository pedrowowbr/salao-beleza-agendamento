# Cabeleleila Leila - Sistema de Agendamentos

Sistema web desenvolvido em Django para controle de agendamentos de um salão de beleza.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.12**
* **Django 6.0.6**
* **python-dotenv 1.2.2**
* **SQLite**
* **HTML5 / CSS3**
* **Bootstrap 5**
* **Django Templates**

> As demais dependências (`asgiref`, `sqlparse`, `tzdata`) são instaladas automaticamente junto com o Django.

---

## 🚀 Funcionalidades

* Cadastro e login de clientes.
* Área da Leila com acesso administrativo.
* Criação de agendamentos online.
* Seleção de um ou mais serviços por agendamento.
* Sugestão de edição quando já existir agendamento na mesma semana.
* Controle de status dos agendamentos.
* Visualização de histórico.
* Edição e exclusão de clientes, serviços e agendamentos pela equipe de staff.

---

## 💻 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto localmente:

### 1. Clonar o repositório e acessar a pasta

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

Abra o `.env` e preencha o `SECRET_KEY` com uma chave própria. Você pode gerar uma com:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Rode as migrações do banco de dados

```bash
python manage.py migrate
```

### 6. Crie o usuário administrador (Staff)

```bash
python manage.py createsuperuser
```

### 7. Execute o servidor local

```bash
python manage.py runserver
```

Agora, basta abrir o seu navegador e acessar o sistema através do endereço:

👉 http://127.0.0.1:8000/

---

## 🔗 Acessos Principais

| Tela | Caminho na URL |
|---|---|
| Cadastro de cliente | `/accounts/registrar/` |
| Login de cliente | `/accounts/login/` |
| Agendamentos | `/agendamentos/` |
| Dashboard interno | `/dashboard/` |
| Área da Leila (Admin) | `/admin/` |

---

## 🧪 Testes

O projeto possui uma suíte de testes unitários organizada na pasta `tests/`, espelhando a estrutura dos apps (`agendamentos`, `clientes`, `servicos`).

Para executar todos os testes:

```bash
python manage.py test
```

Para executar os testes de um app específico:

```bash
python manage.py test tests.agendamentos
python manage.py test tests.clientes
python manage.py test tests.servicos
```

O que está cobrido:

* Regra de negócio que impede alteração de agendamento com menos de 2 dias de antecedência.
* Sugestão de agendamento na mesma semana para o mesmo cliente.
* Permissões de acesso (staff x cliente) em todas as views de agendamentos, clientes e serviços.
* Criação e edição de clientes com usuário de login vinculado.
* CRUD completo de serviços.

---

## 📌 Observações Técnicas

* **Banco de Dados:** O banco utilizado no desenvolvimento foi o SQLite (padrão do Django), não sendo necessária nenhuma configuração externa de banco.
* **Níveis de Acesso:** O sistema separa rigidamente o acesso entre cliente e staff.
* **Privacidade:** Clientes visualizam apenas e exclusivamente os seus próprios agendamentos.
* **Gestão:** A Leila (como staff) possui controle total para gerenciar clientes, serviços, agendamentos e alteração de status através do painel.
* **Arquitetura:** A aplicação foi devidamente estruturada utilizando o padrão de apps do Django, facilitando futuras manutenções e escalabilidade.
