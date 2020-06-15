# Mover django model de um app para outro

Mover uma classe de um dos seus models de um `django app` para outro `django app` não é uma tarefa trivial. Você terá que modificar os arquivos gerados pelo comando `python3 manage.py makemigrations`. Tendo em vista, decidi salvar aqui um breve tutorial com o passo a passo pra fazer isso.

### Estrutura do projeto

Aqui abaixo está a estutura de diretório do projeto.

- `congif/ `
    - settings.py
    - wsgi.py
- `core_application/ `
    - `migrations/ `
        - **0001_initial.py**
    - admin.py
    - app.py
    - **models.py**
    - tests.py
    - views.py

Preste atenção aos dois arquivos em destaque. Temos o migrations inicial do app _core_aplication_ e o arquivo com os models ORM.

#### O arquivo models.py
Veja o arquivo `models.py`

```py
# models.py

from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)


class Person(models.Model):
    name = models.CharField(max_length=255)
```

Temos dois models: `Domain`, e `Person`. Dicidimos um dia que eles deve ser separados, cada em um sua aplição, e para isso criaremos uma nova aplicação: `accounts` com o camnando `python3 manage.py startapp accounts`


- `congif/ `
    - settings.py
    - wsgi.py
- `core_application/ `
    - `migrations/ `
        - 0001_initial.py
    - admin.py
    - app.py
    - models.py
    - tests.py
    - views.py
- `accounts/ `
    - `migrations/ `

    - admin.py
    - app.py
    - models.py
    - tests.py
    - views.py

### Gerando os migrations

O objetivo é mover o model `Person` para a aplicação `accounts`, dessa forma `core_aplication.Person --> accounts.Person`.

Primeiro criaremos um migration no app `core_aplication` para desvincular nosso model.

- `core_application/ `
    - `migrations/ `
        - 0001_initial.py
        - 0002_untrack_model_person.py

Pronto, criamos um arquivo de migrations onde podermos editar manualmente para criar uma estratégia para desvincular os models.

#### Desvincular o model

Veja como como deveremos fazer isso

```py
# 0002_untrack_model_person.py

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_aplications', '0001_initial'),
    ]

    database_operations = [
        migrations.AlterModelTable('Person', 'accounts_person')
    ]

    state_operations = [migrations.DeleteModel('Person')]

    operations = [
      migrations.SeparateDatabaseAndState(
        database_operations=database_operations,
        state_operations=state_operations)
    ]
```

O codigo acima renomeia o nome da tabela do model `Person`, porém essa renoação é feita a nivel de banco de dados, não altera o nome da tabela no código o ORM. Em segida é deletada a tabela do model `Person`, que tentará deletar uma tabela com o nome que não existe mais, o nome antigo, visto que a tabela foi renomeada, porém o codigo ainda possui o nome da tebala antiga.

#### Criar model da outra aplicação

Agora criaremos o model na nova aplição.

##### 1 - Cria classe do Model

No arquivo copie e cole o arquivo do `models.py` da aplicação que estamos vendo, para a nova aplição.

```py
# core_application.models.py

from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
```

```py
# accounts.models.py

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
```


##### 2 - Gerar novos migrations

Execute o comando de makemigrations para o novo model:

```bash
python3 manage.py makemigrations accounts
```

Em seguida edite o novo arquivo de migration gerado e adicione as dependencias corretamente, e altere o atributo de operations, veja abaixo:


```py
class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # .... outras dependencias

        # adicione a dependencia da migration que criamos anteriormente
        # no app core_aplication
        ('core_aplication', '0002_untrack_model_person')
    ]

    state_operations = [  # renomeio `operaionst para `state_operations`

        # oprations de Create gerado pelo
        # comando makemigrations accounts
        # com os campos do model, ou caso preferir,
        # que você tenha escrito.
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'accounts_person',
            },
        ),
    ]

    # alterere o atributo `operations` para utilizar o SeparateDatabaseAndState()
    # e passe como argumento o state_operations, onde criamos o model
    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations
        )
    ]
```

- [x] Model movido com sucesso!