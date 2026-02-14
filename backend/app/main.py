from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.settings import get_settings
from app.api.router import router
from app.services.exceptions import InvalidMonthFormatError

# Variáveis globais
settings = get_settings()
app = FastAPI()

@app.exception_handler(InvalidMonthFormatError)
async def invalid_month_format_handler(request: Request, exc: InvalidMonthFormatError):
    return JSONResponse(
            status_code=400,
            content={"detail": exc.detail}
        )

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)