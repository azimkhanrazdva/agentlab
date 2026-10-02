# Development

Run backend checks:

```bash
pytest
ruff check .
mypy apps packages
```

Run frontend checks:

```bash
cd apps/web
npm install
npm run build
```

