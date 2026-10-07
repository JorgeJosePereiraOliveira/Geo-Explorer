"""Esqueleto do servidor HTTP do Geo-Explorer para acesso via HTTPS / API Key / SSO.

Este módulo NÃO está ativado por padrão. O transporte stdio em src/mcp/server.py
é o modo de operação atual.

Para habilitar o transporte HTTP:
    1. Instale as dependências opcionais:
           pip install "geo-explorer[http]"
    2. Gere um certificado TLS (auto-assinado para dev ou via Let's Encrypt para produção):
           openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    3. Configure as variáveis de ambiente (veja .env.example):
           GEO_API_KEY=seu-token-secreto
           GEO_HOST=0.0.0.0
           GEO_PORT=8443
           GEO_TLS_CERT=cert.pem
           GEO_TLS_KEY=key.pem
    4. Execute:
           python -m src.mcp.http_server

Roadmap de autenticação suportado:
    - API Key (implementado neste esqueleto — pronto para ativar)
    - OAuth2 / SSO via OIDC (stub documentado abaixo)
    - mTLS (mutual TLS) para ambientes corporativos

Uso como servidor MCP via HTTP (futuro):
    Registre no Bob com transport "http" apontando para https://<host>:<porta>/mcp.
"""
from __future__ import annotations

import os
import sys

# ── Verificação de dependências opcionais ─────────────────────────────────────
try:
    import fastapi  # noqa: F401
    import uvicorn  # noqa: F401
except ImportError:
    print(  # noqa: T201
        "[geo-explorer] FastAPI/Uvicorn não instalados.\n"
        "Execute: pip install 'geo-explorer[http]'",
        file=sys.stderr,
    )
    sys.exit(1)

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from src.mcp.server import (
    _buscar_desafio,
    _buscar_trilha,
    _gerar_codigo,
    _trilhas,
    _desafios,
)
from datetime import date

# ── Configuração via variáveis de ambiente ────────────────────────────────────
_API_KEY = os.environ.get("GEO_API_KEY", "")
_HOST = os.environ.get("GEO_HOST", "0.0.0.0")
_PORT = int(os.environ.get("GEO_PORT", "8443"))
_TLS_CERT = os.environ.get("GEO_TLS_CERT", "cert.pem")
_TLS_KEY = os.environ.get("GEO_TLS_KEY", "key.pem")

# ── Aplicação FastAPI ─────────────────────────────────────────────────────────
app = FastAPI(
    title="Geo-Explorer API",
    description="API HTTP do Geo-Explorer — trilhas, desafios e certificados DIO.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Redirecionar HTTP → HTTPS em produção (desabilite em desenvolvimento local)
# app.add_middleware(HTTPSRedirectMiddleware)

# ── Autenticação via API Key ──────────────────────────────────────────────────
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def _verificar_api_key(api_key: str | None = Security(_api_key_header)) -> str:
    """Valida a API Key enviada no header X-API-Key.

    Em desenvolvimento, se GEO_API_KEY não estiver configurado, todas as
    requisições são aceitas (modo inseguro — não use em produção).
    """
    if not _API_KEY:
        # Modo desenvolvimento: sem autenticação
        return "dev-mode"
    if api_key != _API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida ou ausente. Inclua 'X-API-Key: <token>' no header.",
        )
    return api_key


# ── STUB: Autenticação OAuth2 / SSO via OIDC ─────────────────────────────────
# Para habilitar SSO corporativo (ex: Azure AD, Okta, Google Workspace):
#
# 1. Instale: pip install python-jose[cryptography] httpx
#
# 2. Configure o OIDC provider:
#    OIDC_ISSUER=https://login.microsoftonline.com/<tenant>/v2.0
#    OIDC_CLIENT_ID=<client-id>
#    OIDC_CLIENT_SECRET=<client-secret>
#
# 3. Implemente a verificação do JWT:
#
#   from jose import jwt
#   import httpx
#
#   async def _verificar_token_oidc(token: str = Depends(oauth2_scheme)):
#       jwks_uri = f"{OIDC_ISSUER}/.well-known/openid-configuration"
#       # ... buscar public keys, validar JWT, verificar claims
#       return payload
#
# 4. Substitua `Depends(_verificar_api_key)` por `Depends(_verificar_token_oidc)`
#    nos endpoints abaixo.
#
# Referência: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

# ── Endpoints REST ────────────────────────────────────────────────────────────

@app.get("/health")
async def health() -> dict:
    """Health check — não requer autenticação."""
    return {"status": "ok", "service": "geo-explorer"}


@app.get("/trilhas", dependencies=[Depends(_verificar_api_key)])
async def listar_trilhas() -> list[dict]:
    """Lista todas as trilhas disponíveis."""
    return [
        {
            "id": t["id"],
            "nome": t["nome"],
            "nivel": t["nivel"],
            "carga_horaria": t["carga_horaria"],
            "xp_total": t.get("xp_total"),
            "badges": t.get("badges", []),
            "promocao": t.get("promocao"),
            "vitalicio": t.get("vitalicio"),
            "lives": t.get("lives"),
        }
        for t in _trilhas()
    ]


@app.get("/trilhas/{tecnologia}", dependencies=[Depends(_verificar_api_key)])
async def buscar_trilha(tecnologia: str) -> dict:
    """Retorna o plano de estudos de uma trilha pelo ID."""
    trilha = _buscar_trilha(tecnologia)
    if trilha is None:
        raise HTTPException(status_code=404, detail=f"Trilha '{tecnologia}' não encontrada.")
    return trilha


@app.get("/desafios/{tecnologia}/{nivel}", dependencies=[Depends(_verificar_api_key)])
async def buscar_desafio(tecnologia: str, nivel: str) -> dict:
    """Retorna um desafio de código para a tecnologia e nível informados."""
    desafio = _buscar_desafio(tecnologia, nivel)
    if desafio is None:
        raise HTTPException(
            status_code=404,
            detail=f"Desafio não encontrado para '{tecnologia}' — nível '{nivel}'.",
        )
    return desafio


@app.get("/certificados/{tecnologia}", dependencies=[Depends(_verificar_api_key)])
async def gerar_certificado(tecnologia: str, nome: str, data_conclusao: str | None = None) -> dict:
    """Gera um certificado fictício de conclusão.

    Query params:
        nome: Nome completo do estudante.
        data_conclusao: Data no formato YYYY-MM-DD (padrão: hoje).
    """
    trilha = _buscar_trilha(tecnologia)
    if trilha is None:
        raise HTTPException(status_code=404, detail=f"Trilha '{tecnologia}' não encontrada.")
    data_str = data_conclusao or date.today().isoformat()
    codigo = _gerar_codigo(nome, tecnologia, data_str)
    return {
        "nome": nome,
        "trilha_id": tecnologia,
        "trilha_nome": trilha["nome"],
        "nivel": trilha["nivel"],
        "carga_horaria": trilha["carga_horaria"],
        "xp_total": trilha.get("xp_total"),
        "data_conclusao": data_str,
        "codigo_verificacao": codigo,
    }


# ── Ponto de entrada ──────────────────────────────────────────────────────────

def main() -> None:
    """Inicia o servidor HTTP com TLS (uvicorn)."""
    import uvicorn

    ssl_kwargs: dict = {}
    if _TLS_CERT and _TLS_KEY:
        ssl_kwargs = {"ssl_certfile": _TLS_CERT, "ssl_keyfile": _TLS_KEY}

    uvicorn.run(
        "src.mcp.http_server:app",
        host=_HOST,
        port=_PORT,
        **ssl_kwargs,
    )


if __name__ == "__main__":
    main()
