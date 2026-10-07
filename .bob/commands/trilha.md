---
description: Exibe o plano de estudos completo de uma trilha do Geo-Explorer
argument-hint: <tecnologia>
---
Use a ferramenta MCP `trilha` do servidor `geo-explorer` para buscar o plano de estudos da tecnologia "$1".

Formate a resposta em Markdown com a seguinte estrutura:

# 📚 Trilha: <nome da trilha>

**Tecnologia:** <tecnologia> | **Nível:** <nivel> | **Carga horária:** <carga_horaria>h | **XP Total:** <xp_total>
**Badges disponíveis:** <badges separadas por vírgula>
**Promoção ativa:** Sim/Não | **Acesso vitalício:** Sim/Não | **Lives ao vivo:** <lives>

---

## Módulos

Para cada módulo, exiba:

### Módulo <ordem>: <titulo>
- <topico 1>
- <topico 2>
- <topico 3>

---

Se a tecnologia não for encontrada, liste as disponíveis e sugira alternativas próximas.
