1. **Clonar o repositório:**
- Execute o comando:
```bash 
git clone https://github.com/Arthur31Viana/estoque2.git
```

2. Entre na pasta do projeto
```bash 
cd estoque2
```

3. **Criar e ativar o ambiente virtual na raiz do projeto:**
- Para criar o ambiente virtual: 
```bash 
python -m venv .venv
```

- Para ativar o ambiente virtual: 
  - No Windows:
  ```bash 
  .venv\Scripts\activate
  ```

  - No macOS/Linux:
  ```bash 
  source .venv/bin/activate
  ```

4. **Instalar as dependências do projeto:**
- Execute o comando no terminal:
```bash 
pip install -r requirements.txt
```

5. **Gerar as variáveis de ambiente (caso tenha um script `env_gen.py`):**
- Execute o Comando:
```bash 
python contrib/env_gen.py
```

6. **Executar as migrações para criar as tabelas no banco de dados:**
- Execute o Comando:
```bash 
python manage.py migrate
```

7. **Criar superusuário para o painel administrativo:**
- Execute o Comando:
```bash 
python manage.py createsuperuser
```

8. **Iniciar o servidor de desenvolvimento:**
- Execute o Comando:
```bash 
python manage.py runserver
```