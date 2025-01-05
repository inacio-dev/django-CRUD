#!/bin/bash

# Define a senha do banco de dados
export PGPASSWORD=$DB_PASSWORD

# Conecta ao banco de dados e cria o schema se ele não existir
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -p $DB_PORT -c "DO \$\$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = '$DB_SCHEMA') THEN
      EXECUTE 'CREATE SCHEMA \"$DB_SCHEMA\"';
   END IF;
END
\$\$;"

# Executa as migrações do Django
python manage.py makemigrations --no-input
python manage.py migrate

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Executa os testes
python manage.py test --noinput --keepdb