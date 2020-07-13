# Django Rest UrlField com vários lookups

As vezes suas url pode ter vários lookups que precisem ser acessado para ser mondata e achada pelo `reverse` do Django. Um exemplo de URL com tal comportamente é o seguinte exemplo:

`https://www.domain.com/api/school/20/teacher/100/class/10/students/`


A URL acima possui **3 lookups field**: 20, 100 e 10.

ou ainda uma URL sem lookup algum, como:

`https://www.domain.com/api/login/`

Para adicionar um campo de URL, ao seu serializer, que seja capaz de gerar as seguinte urls será preciso alguns passos a mais.

## Definindo a URL

Primeiro vamos registrar nossa URL acima no arquivos `urls.py`

```py
# urls.py

from django.urls import path
from .viws import MyView

url = 'api/school/<int:id_school>/teacher/<int:id_teacher>/class/<int:id_class>/students/'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path(url, MyView.as_view(), name='students-view')
]
```

A URL acima tem os seguintes lookups keys:

- `id_school`: int
- `id_teacher`: int
- `id_class`: int


## Criando nosso Field

Agora criaremos um Field dos customoizado do Django Rest que receberá a instância do model e irá chamar um método para criar os lookups da URL.


#### Reverse de uma URL com vários lookups

```py
# serializers.py
from rest_framework import serializers
from rest_framework.reverse import reverse


class UrlPatternsField(serializers.HyperlinkedIdentityField):
        def get_url(self, obj, view_name, request, format):
        kwargs = {}

        # nome do método que deve ser implementado para
        # gerar os lookups da URL
        # ex: suponha que o field_name seja `esola`
        # o nome do método será: `get_lookups_fields_escola`
        method_name = 'get_lookups_fields_{}'.format(field_name)

        # pega o método, se existir. 
        # Caso contrário o valor retornado é None
        multiple_lookups_fields = getattr(self.parent, method_name, None)
        if multiple_lookups_fields:
            # já que existe um método, passaremos o objeto
            # para que ele possa gerar os lookups a partir do
            # objeto
            kwargs = multiple_lookups_fields(obj)

        return reverse(view_name, request=request, kwargs=kwargs, format=format)
```

Pronto, field criado, agora devemos implementar no nosso serializer.

```py
# serializers.py


class ClassSerializer(serializer.ModelSerializer):
    students_url = UrlPatternsField(view_name='students-view')
    # note que o nome do field deve ser adicionar ao nome do metodo
    # nesse caso será `get_lookups_fields_students_url`

    class Meta:
        model = ClassModel
        fields = '__all__'

    def get_lookups_fields_students_url(self, obj):
        # retornamos um dict com os lookups necessários para
        # monstar a URL
        return {
            'id_school': obj.school.id,
            'id_teacher': obj.teacher.id,
            'id_class': obj.id
        }
```


#### Reverse de uma URL sem lookup

Muito simple, não implementamos o método que retorna os lookups ou retornamos um dicionário vazio.

```py
# serializers.py


class EntryPointSerializer(serializer.ModelSerializer):
    login = UrlPatternsField(view_name='login')
    # a url nao precisa de lookups, portanto nao implementamos o metodos
    home = UrlPatternsField(view_name='home')
    # a url nao precisa de lookups, portanto nao implementamos o metodos

    class Meta:
        model = EntryModel
        fields = '__all__'
```