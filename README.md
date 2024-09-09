# estoque2

- Sistema de Entrada e Saída de Estoque de Merenda para Escolas


# Instalação:
1. **Clonar Repositório:**
- Execute o comando:
'''bash git clone https://github.com/Arthur31Viana/estoque2.git'''


2. **Entre na Pasta do Projeto**
- '''cd estoque2'''


3. **Criar e Ativar o Ambiente Virtual na Raiz do Projeto:**
- Para Criar o Ambiente Virtual: 
'''bash python -m venv .venv'''

- Para Ativar o Ambiente Virtual: 
- No Windows: 
 '''venv\Scripts\activate'''

- No macOS/Linux: 
'''source .venv/bin/activate'''


4. **Instalar as dependências do Projeto:**
- Execute o Comando no Terminal: '''pip install -r requirements.txt'''


5. **Gerar as Variáveis de Ambiente (Caso Tenha um Script `env_gen.py`):**
- Execute o Comando: '''bash python contrib/env_gen.py'''


6. **Executar as Migrações para Criar as Tabelas no Banco de Dados:**
- Execute o Comando: '''bash python manage.py migrate'''


7. **Criar SuperUsuário para o Painel Administrativo:**
- Execute o Comando: '''bash manage.py createsuperuser'''


8. **Iniciar o Servidor de Desenvolvimento:**
- Execute o Comando: '''bash python manage.py runserver'''
