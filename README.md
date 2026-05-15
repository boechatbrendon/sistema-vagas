# Sistema de Sorteio de Vagas - Condomínio Premium

Sistema moderno e profissional para sorteio de vagas de garagem desenvolvido com Flask + TailwindCSS.

## 🎨 Características

- **Interface Dark Premium** - Design moderno estilo SaaS
- **TailwindCSS** - Framework CSS via CDN
- **HeroIcons** - Ícones modernos
- **Glassmorphism** - Efeitos visuais elegantes
- **Responsivo** - Funciona em todos os dispositivos
- **Transparente** - Processo de sorteio auditável

## 🚀 Tecnologias

- Python 3.8+
- Flask 3.0
- TailwindCSS (CDN)
- HeroIcons
- HTML5 + Jinja2

## 📦 Instalação

1. **Clone ou navegue até o diretório do projeto**

```bash
cd sistema_vagas
```

2. **Instale as dependências**

```bash
pip install -r requirements.txt
```

## ▶️ Como Rodar

1. **Execute o servidor Flask**

```bash
python app.py
```

2. **Abra o navegador e acesse**

```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
sistema_vagas/
├── app.py                 # Aplicação Flask principal
├── vagas.json            # Dados das vagas
├── apartamentos.json     # Dados dos apartamentos
├── vagas.py              # Script original de sorteio
├── requirements.txt      # Dependências Python
├── templates/            # Templates HTML
│   ├── base.html        # Template base
│   ├── index.html       # Tela inicial
│   ├── vagas.html       # Tela de vagas
│   ├── unidades.html    # Tela de unidades
│   ├── sortear.html     # Tela de sorteio
│   └── resultados.html  # Tela de resultados
└── static/              # Arquivos estáticos (vazio - usa CDN)
```

## 🎯 Funcionalidades

### Telas Disponíveis

1. **Início** (`/`) - Dashboard com estatísticas gerais
2. **Vagas** (`/vagas`) - Listagem de todas as vagas organizadas
3. **Unidades** (`/unidades`) - Listagem de apartamentos por bloco
4. **Sortear** (`/sortear`) - Execução do sorteio
5. **Resultados** (`/resultados`) - Visualização dos resultados

### Regras do Sorteio

O sistema executa o sorteio em 3 etapas:

1. **1º Sorteio - PCD**
   - Vagas reservadas para pessoas com deficiência
   - Prioridade máxima

2. **2º Sorteio - Descobertas**
   - Vagas descobertas para unidades específicas
   - Unidades finais 1 e 8 (exceto 48)

3. **3º Sorteio - Geral**
   - Vagas SS2/SS3 por bloco (A e B)
   - Ampla concorrência para vagas restantes

## 🎨 Design System

### Paleta de Cores

- **Fundo Principal**: `bg-slate-950` (#020617)
- **Cards**: `bg-slate-800/30` com glassmorphism
- **Primária (Emerald)**: Ações positivas, sistema
- **Secundária (Purple)**: Sorteios, destaques
- **Informativa (Blue)**: Informações, orientações
- **Aviso (Amber)**: PCD, atenção
- **Erro (Red)**: Erros, bloqueios

### Componentes

- Cards com glassmorphism
- Bordas suaves e arredondadas
- Hover elegante com transições
- Badges coloridas
- Ícones HeroIcons
- Grid responsivo

## 📝 API Endpoints

- `GET /` - Tela inicial
- `GET /vagas` - Listagem de vagas
- `GET /unidades` - Listagem de unidades
- `GET /sortear` - Tela de sorteio
- `POST /api/executar-sorteio` - Executa o sorteio
- `GET /resultados` - Visualiza resultados
- `POST /api/limpar-resultado` - Limpa resultado atual

## 🔧 Customização

### Modificar Dados

- Edite `vagas.json` para alterar as vagas
- Edite `apartamentos.json` para alterar as unidades

### Personalizar Visual

- Modifique as classes TailwindCSS nos templates
- Ajuste as cores no arquivo `base.html`
- Customize os ícones usando HeroIcons

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:

- Desktop (1920px+)
- Laptop (1024px+)
- Tablet (768px+)
- Mobile (320px+)

## 🛡️ Segurança

- Sorteio com aleatoriedade via `random.shuffle()`
- Validação de dados no backend
- Tratamento de erros
- Sistema stateless (sem armazenamento de sessão)

## 📄 Licença

Sistema desenvolvido para uso interno do condomínio.

## 👨‍💻 Desenvolvimento

Desenvolvido com:
- Flask (Python)
- TailwindCSS
- HeroIcons
- HTML5 + Jinja2

---

**© 2026 Sistema de Sorteio de Vagas - Condomínio Premium**
