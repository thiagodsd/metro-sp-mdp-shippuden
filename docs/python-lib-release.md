# release python lib via github

notas de como montar lib python e publicar direto nas releases do github
(pq github packages não suporta python, descobri na marra)

## estrutura mínima

```
minha-lib/
├── src/
│   └── minha_lib/
│       ├── __init__.py
│       └── codigo.py
├── pyproject.toml
└── README.md
```

importante: usar `src/` pra evitar problemas de import

## pyproject.toml

o essencial pra funcionar:

```toml
[project]
name = "minha-lib"
version = "0.1.0"
description = "o que isso faz"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/minha_lib"]
```

metadata extra se quiser deixar bonito:
- `license = {text = "MIT"}`
- `authors = [{name = "Nome", email = "email@example.com"}]`
- `[project.urls]` com Repository, Issues, etc

## workflow github actions

criar `.github/workflows/release-python.yml`:

```yaml
name: release python lib
on:
  push:
    tags: ['v*']
permissions:
  contents: write
jobs:
  build-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install build hatchling
      - run: python -m build
      - uses: softprops/action-gh-release@v1
        with:
          files: dist/*
```

bem mais simples que fazer upload pro pypi

## testar build local

antes de fazer release, sempre testar:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install build hatchling
python -m build
```

vai gerar em `dist/`:
- `.whl` (wheel) - formato binário
- `.tar.gz` (sdist) - código fonte

## fazer release

```bash
git tag v0.1.0
git push origin v0.1.0
```

o workflow roda automaticamente e anexa os arquivos na release

## instalar depois

```bash
# pelo wheel da release
pip install https://github.com/user/repo/releases/download/v0.1.0/lib-0.1.0-py3-none-any.whl

# ou direto do git (mais fácil)
pip install git+https://github.com/user/repo.git@v0.1.0
```

pra monorepo com subdir:
```bash
pip install git+https://github.com/user/repo.git@v0.1.0#subdirectory=packages/lib-name
```

## erros comuns

- esquecer de colocar `packages = ["src/minha_lib"]` no pyproject → build não acha o código
- nome do pacote com hífen mas import com underscore → sempre usar underscore
- versão da tag não bate com pyproject.toml → não é problema mas fica estranho
- build falha mas não vejo erro → adicionar `run: python -m build --verbose`

## por que não usar pypi público

pq isso aqui é experimental/interno, não precisa poluir o pypi
github releases funciona bem pra isso
