## Plan: Ampliar Testes do FastAPI

A suíte já está separada do código em `tests/` na raiz e cobre os fluxos de API existentes. Manter essa organização e acrescentar um módulo pequeno para verificar o contrato OpenAPI e a integração de arquivos estáticos, evitando repetir os testes de inscrição/cancelamento já presentes.

**Steps**
1. Adicionar `tests/test_api_contract.py` com teste do documento `/openapi.json`, verificando as rotas e métodos esperados (`/activities`, inscrição e cancelamento).
2. No mesmo módulo, verificar que `GET /static/index.html` entrega o arquivo montado com sucesso e que um caminho estático inexistente retorna 404.
3. Reutilizar o fixture `client` de `tests/conftest.py`; não alterar a aplicação nem duplicar a cobertura existente em `tests/test_app.py`.

**Relevant files**
- `/workspaces/skills-getting-started-with-github-copilot-rafael-pialarissi-0411/tests/test_api_contract.py` — novo módulo de contrato FastAPI e montagem de estáticos.
- `/workspaces/skills-getting-started-with-github-copilot-rafael-pialarissi-0411/tests/conftest.py` — reutilizar o `TestClient` existente.
- `/workspaces/skills-getting-started-with-github-copilot-rafael-pialarissi-0411/pytest.ini` — já aponta para `tests/`; nenhuma alteração esperada.
- `/workspaces/skills-getting-started-with-github-copilot-rafael-pialarissi-0411/tests/test_app.py` — cobertura de comportamento existente a preservar, sem duplicação.

**Verification**
1. Executar `python -m pytest tests/test_api_contract.py` para validar o novo módulo.
2. Executar `python -m pytest` para verificar a suíte completa.

**Decisions**
- Usar o diretório `tests/` da raiz, conforme alinhado; não criar `src/tests/` nem reorganizar o backend.
- Presumir que a expansão desejada é cobertura estrutural do FastAPI (schema OpenAPI e montagem de estáticos), já que os casos funcionais de API existentes estão cobertos.
- Não adicionar testes de novos comportamentos de negócio sem indicação de quais regras devem ser garantidas.
