---
description: Gera um certificado fictício de conclusão de trilha do Geo-Explorer
argument-hint: "<nome completo>" <tecnologia>
---
Use a ferramenta MCP `certificado` do servidor `geo-explorer` com os parâmetros:
- nome: "$1"
- tecnologia: "$2"

Formate a resposta como um certificado oficial em Markdown:

---

# 🎓 CERTIFICADO DE CONCLUSÃO

**GEO-EXPLORER** — Plataforma de Trilhas de Aprendizagem DIO

---

> Certificamos que

## $1

> concluiu com êxito a trilha

## <trilha_nome>

| Campo | Valor |
|---|---|
| **Nível** | <nivel> |
| **Carga Horária** | <carga_horaria>h |
| **XP Conquistado** | <xp_total> |
| **Data de Conclusão** | <data_conclusao> |
| **Código de Verificação** | `<codigo_verificacao>` |

---

*Este é um certificado fictício gerado pelo Geo-Explorer. O código de verificação é único e determinístico.*

---

Se a trilha não for encontrada, informe e liste as trilhas disponíveis.
