# Documentação do Projeto

Bem-vindo à documentação do projeto! Aqui você encontrará uma visão detalhada da estrutura de pastas e da lógica utilizada, facilitando o entendimento sobre a arquitetura e as decisões de desenvolvimento.

## Estrutura de Pastas

O projeto está configurado para rodar em **Docker**, por isso, todas as aplicações e configurações principais estão contidas na pasta `django_app`. Quando mencionarmos "raiz" ao longo desta documentação, estaremos nos referindo à pasta `django_app`.

### Diretório do Projeto

Dentro da pasta `django_app`, cada projeto e aplicação Django será criado diretamente na raiz, facilitando a organização e manutenção.

### Testes Unitários

Para cada aplicação criada, é fundamental incluir testes unitários. Lembre-se de que os nomes dos arquivos de teste devem ser **claros e autoexplicativos**, mesmo que isso os torne um pouco longos. Nomes descritivos facilitam a compreensão do propósito de cada teste, melhorando a manutenção e o entendimento do código por outros desenvolvedores.

### Estrutura de Templates e Arquivos Estáticos

A estrutura das pastas de templates e arquivos estáticos (`static`) segue uma lógica que facilita a organização e reutilização de componentes.

#### Estrutura do Diretório Static

A pasta `static` é obrigatória no Django e organiza os arquivos estáticos em subpastas específicas para cada tipo de recurso. A estrutura segue o seguinte padrão:

```
static/
└── base/
    ├── css/
    ├── img/
    ├── js/
    └── sass/
```

- **base**: Essa pasta serve como um repositório de funcionalidades ou estilos que podem ser reaproveitados por vários aplicativos dentro do projeto.
- **css, img, js, sass**: Cada uma dessas subpastas contém recursos específicos para estilização, imagens, scripts JavaScript e arquivos de pré-processamento CSS, respectivamente.

#### Organização dos Arquivos Estáticos

Cada aplicação terá sua própria estrutura dentro de `static`, onde o nome da subpasta será correspondente ao nome da aplicação. Isso permite que os arquivos estáticos fiquem bem organizados e relacionados diretamente ao contexto de cada aplicação.

### Boas Práticas

- **Nomeação de Arquivos**: Use nomes descritivos para facilitar o entendimento do conteúdo de cada arquivo, especialmente nos testes unitários.
- **Reutilização de Funcionalidades**: Arquivos e recursos na pasta `base` devem ser genéricos e reutilizáveis para facilitar o compartilhamento de funcionalidades entre aplicações.

Consulte a lista de autores em [authors.md](./AUTHORS.md).
