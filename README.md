# RandomLab

Aplicación web para generar números pseudoaleatorios y verificar una muestra mediante pruebas de Póker y Corridas Arriba/Abajo.

## Estructura

- `backend/app/generators/multiplicative.py`: generador congruencial multiplicativo.
- `backend/app/generators/middle_product.py`: generador de productos medios.
- `backend/app/tests/poker.py`: prueba de Póker (chi-cuadrado).
- `backend/app/tests/runs.py`: prueba de corridas arriba y abajo.
- `frontend/`: interfaz en Next.js + Tailwind.

## Ejecutar

En una terminal:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

Abre `http://localhost:3000`. La documentación interactiva de la API queda disponible en `http://localhost:8000/docs`.

## Despliegue en Vercel

El archivo `vercel.json` compila el frontend y expone el backend FastAPI como función serverless bajo `/api`. En producción no es necesario configurar `NEXT_PUBLIC_API_URL`: la interfaz se conecta a esa ruta automáticamente.
