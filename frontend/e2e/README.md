# Testes ponta a ponta

Testes no navegador real (Playwright), contra o Django e o Next.js a correr. Usam os dados do `semear_demo` e criam
os seus próprios dados de teste (e-mails `*.test`).

```bash
# 1. Backend com os e-mails do allauth em ficheiros (para o teste da recuperação de palavra-passe)
cd backend
EMAIL_FICHEIROS=/tmp/rasto-emails .venv/bin/python manage.py runserver 8000

# 2. Frontend
cd frontend && npm run build && npm run start

# 3. Testes (noutra consola)
cd frontend
npx playwright install chromium                 # uma vez
EMAIL_FICHEIROS=/tmp/rasto-emails npm run e2e
```

- `sprint1.spec.ts`: fluxo completo da aceleradora, incluindo a activação da 2FA e a entrada com código.
- `conta.spec.ts`: equipa da entidade e recuperação da palavra-passe.
- `acessibilidade.spec.ts`: axe (WCAG 2.2 AA) sem violações graves nos ecrãs do Sprint 1, a 390 e 1280 px.
- Todos falham se a consola mostrar erros, incluindo violações da CSP.
