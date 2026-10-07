# Sub-Tarefa 2 — Expansão de trilhas e adição de desafios Java

## Contexto
Tarefa de expansão do Geo-Explorer: substituir `data/trilhas.json` com ≥ 30 trilhas DIO e adicionar desafios de Java em `data/desafios.json`.

## O que foi feito

### data/trilhas.json
- Substituído completamente com **32 trilhas** (5 originais + 27 novas).
- Todos os campos originais das 5 trilhas mantidos intactos (retrocompatibilidade).
- Novos campos adicionados em todas as trilhas: `tecnologia`, `xp_total`, `badges`, `promocao`, `vitalicio`, `lives`.
- Trilhas de Java criadas com IDs exatos: `java_basico`, `java_intermediario`, `java_avancado`.
- Trilha `python` mantida com exatamente 5 módulos (exigência do teste `test_trilha_python_tem_5_modulos`).
- Cada módulo contém `ordem`, `titulo` e `topicos` (array com ≥ 3 itens).

### data/desafios.json
- Adicionados 3 desafios de Java ao array existente:
  - `tecnologia: "java"`, `nivel: "iniciante"` — "Calculadora de Média"
  - `tecnologia: "java"`, `nivel: "intermediario"` — "Sistema de Banco Simples com OOP"
  - `tecnologia: "java"`, `nivel: "avancado"` — "Implementar um Pool de Threads"

## Resultado dos testes
```
15 passed in 0.29s — tests/test_data_loader.py
```
Todos os 15 testes passaram sem falhas.
