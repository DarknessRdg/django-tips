# Imagens com Django e Django Rest Framework

Ajustes para usar corretamento imagem com Django e o Django Rest Framework

## Imagens com Django

Antes de tudo é preciso fazer alguns ajuses na aplicação para utilizar as 
imagens da maneira correta com o django.

1. Adicionar `MEDIA_URL` e `MEDIA_ROOT` no arquivo **settings.py**
2. Adicionar `MEDIA_URL` e `MEDIA_ROOT` nas urlpatterns do arquivo **urls.py** do project.

### Settings.py

Adicione as seguinte variáveis de configuração no seu settings:

```python
MEDIA_URL = '/pasta_para_guardar_arquivos/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'pasta_para_guardar_arquivos')
```

* **MEDIA_URL**: nome da pasta onde será guardada as imagens, os vídeos e os arquivos
que forem feito upload para o repositório.
* **MEDIA_ROOT**: caminho absoluto para a pasta MEDIA_URL

O seu repositório ficará com a seguinte estrutura

```json
- repositorio
   
    - projeto
        - settings.py
        ...
   
    - app
        - models.py
        ...
   
    - pasta_para_guardar_arquivos
        ...
    
    - manage.py
```

Onde `pasta_para_guardar_arquivos` será o diretório para armazenar todos os arquivos que forem
feito upload.

### Urls.py

Concatene com a lista o seguintes comando:

`static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`

Veja:
```python

# importa funcao static do django
from django.conf.urls.static import static  

# importa as variaveis do arquivo settings.py
from django.conf import settings  

urlpatterns = [
    path('', views),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# concatena as rotas para acessar as imagens no servidor
```

### Models.py

Adicionar campo de imagem ao Model

```python
from django.db import models


class ModelComImagem(models.Model):
    imagem = models.ImageField(upload_to='pasta_das_imagens/')
```

o atributo `upload_to` recebe como parâmetro uma string com o nome da pasta de destino. Esta pasta será
localizada dentro da pasta `MEDIA_URL` configurada nos [settings.py](#settingspy). 

Ao salvar uma imagem você terá o seguinte diretório:

```json
- repositorio
   
    - projeto
        - settings.py
        ...
   
    - app
        - models.py
        ...
   
    - pasta_para_guardar_arquivos
        - pasta_das_imagens
            - imagem1.jpg
        ...
    
    - manage.py
```

Já que a string será concatenada com a `MEDIA_URL`, é possível criar subdiretórios para `upload_to`.
Por exemplo, imagine que sejam imagens de perfil do usuário, você pode fazer da seguinte forma:
 
```python
from django.db import models


class ModelComImagem(models.Model):
    imagem = models.ImageField(upload_to='perfil/pasta_das_imagens/')
```

Agora, ao salvar você terá o seguinte diretório:


```json
- repositorio

    - projeto
        - settings.py
        ...
   
    - app
        - models.py
        ...
   
    - pasta_para_guardar_arquivos
        - perfil
            - pasta_das_imagens
                - imagem1.jpg
                ...
        ...
    
    - manage.py
```