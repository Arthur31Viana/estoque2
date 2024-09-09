# estoque2

- Sistema de Entrada e Saída de Estoque de Merenda para Escolas

# Instalação:
- Criar pasta onde o projeto irá ficar
- Abrir terminal dentro da pasta e inciar o repositório git digitando git init
- Fazer um git clone dentro da pasta que criou
- Criar e Ativar Ambiente Virtual na raiz do projeto
- Instalar dependências pelo terminal executando: pip install -r requirements.txt
- Executar env_gen.py pelo terminal usando: python contrib/env_gen.py
- Executar migrações das Tabelas para o Banco de Dados pelo terminal usando: python manage.py migrate
- Criar Super Usuário pelo terminal com: python manage.py createsuperuser <usuario>
- No terminal, executar: python manage.py runserver, para iniciar o projeto
