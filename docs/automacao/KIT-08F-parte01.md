# KIT-08F — parte01: abertura, inventário vivo e plano

Cartão t_ac0f78f7 (KIT-08F), run654, perfil default (único confirmado). Instância
implementadora NOVA: 654 != implementador original 643 != reviewer 648. Revisão
independente será pedida no MESMO cartão via kanban_request_review; KIT-12 t_0a434c97
e KIT-15 t_10584ca5 permanecem gated até aprovação técnica.

Data/hora local inicial: 2026-10-09 22:4x UTC-03 (offline, sem jogo/rede/build).

## 1. Inventário vivo (lido antes de qualquer edição)

- tools/automacao/kit08/visualizador.py SHA256
  3d6d2983a845d1423859ef75f7f8e658cde7c14c0d4fe3ee23194d08a9789701 — CONFERE com o
  baseline reprovado declarado no corpo do cartão (red).
- Suíte imutável do reviewer: scratch/kit/KIT-08R-run648/test_review_kit08.py
  sha256 597b5ab38129d059e00ea17b50ba7a3b07e76a5ad904960d4f23e5b5cf435c14;
  review_controls.py sha256 575f2c4cec59b46b1f540f5c4ae325c9967e34710fc5d818f97b268eacf901cd.
  COPIADOS byte a byte (não editados) para scratch/kit/KIT-08F-run654/.
- Sandbox da reviewer copiada para scratch/kit/KIT-08F-run654/sandbox (cópia byte a byte
  do escopo, incl. baseline visualizador.py 3d6d... e fixtures kit09) para permitir
  replay RED sem tocar na prova histórica.

## 2. Achados F1–F9 → o que o código reprovado faz (mapeado no fonte 3d6d...)

- F1 (paths): referencia_local_segura(:76-101) só olha a string CRUA: aceita `%2e%2e/...`,
  `img/%2e%2e%2f...`, `C%3a/...`, `safe.png?x=1#frag`. Decodificada, a referência sai do
  confinamento. → rejeitar `%`, `?`, `#` e manter recusas já provadas (hardening lexical;
  efeito browser segue INDETERMINADO, não alegar exfiltração).
- F2 (aprovação): renderizar(:446-453) injeta stale/motivos num dict vazio → truthy →
  VIGENTE sem aprovação; aprovacao_stale ignora mod/origem/completude. → ausência/incompleto/
  sintético/identidade divergente NUNCA é aprovação; verdadeiro positivo mantém vigência.
- F3 (comparação): usa veredito sem o rótulo fixture do doc; dict por id esconde duplicatas;
  regressão pelo estado cru (perda de prova não regride); caso removido/zero casos = OK.
- F4 (compatibilidade): `contextos_compativeis` só compara quando AMBAS as pontas têm valor
  e ignora `mod`. → simetria do declarado (um lado só = recusa), mínimo obrigatório, mod igual;
  fonte/dll próprias da candidata NÃO impedem comparação.
- F5 (veredito/identidade): bool('false') vira True; evidencia=[] passa; fonte_sha/sessão do
  critério contradizendo o contexto vivo não invalida; rotulo_fixture em identidade ignorado.
- F6 (CLI): --identidade é mesclada em main(:526-532) DEPOIS de montar_doc/avaliar.
- F7 (exit): main(:550-561) ignora o resultado da comparação (exit0 com comparação recusada).
- F8 (campos/imagem): sessão string descartada (:371 antes de testar isinstance(str) em :372);
  imagem relativa não resolve/embute ao gravar HTML em outra pasta (CLI exit0).
- F9 (infra): `_ler` dos opcionais fora do try (:526-536) → traceback/exit1 em vez de exit2.

## 3. Invariantes que NÃO podem quebrar

- Suíte autor tools/automacao/kit08/teste_visualizador_kit08.py: Ran21 OK.
- contra_prova_kit08.py: 8/8 VERDE — âncoras de mutação exigem count==1 no fonte:
  `    return html.escape(str(texto), quote=True)`,
  `script-src 'none'; base-uri 'none'; form-action 'none'`,
  `    if not isinstance(ref, str):`,
  `    return (not motivos), motivos`, `    return bool(motivos), motivos`,
  `    if estado == OK and provou and proc == "runtime":`,
  `        return "NAO_EXERCITADO" if fixture else "PASSOU"`,
  `    if estado == REPROVADO:\n        return "FALHOU"`,
  `PENDENTE (nao concedido por esta ferramenta).`,
  `    doc["resumo"] = kit09.resumir(criterios, ident)`,
  `AQUI = os.path.dirname(os.path.abspath(__file__))`.
- review_controls (10 mutações) usa os MESMOS âncoras (menos D7) + `    return (not motivos), motivos`
  usado em 2 mutações → precisa continuar aparecendo exatamente 1x.

## 4. Plano de correção (ordem)

1. referencia_local_segura: rejeitar `%`,`?`,`#` (com motivos; nunca ecoar o valor).
2. veredito_tecnico: prova_runtime is True; evidência não vazia; consistência
   fonte/dll/config/sessão do critério contra o contexto do doc; manter as âncoras.
3. origem_sintetica: incluir identidade aninhada.
4. aprovação: estado ausente/inválida/stale/vigente; nunca VIGENTE por ausência; mod+hashes.
5. comparar: fixture nos dois lados, duplicatas/ausências/zero casos, regressão por veredito,
   simetria+mod no contexto.
6. renderizar: sessão string preservada; imagem resolvida/embutida data: com confinamento e
   lacuna explícita.
7. main: ler TODOS os inputs dentro do try (exit2 controlado), mesclar --identidade ANTES de
   montar_doc; exit agregando comparação.

## 5. Provas planejadas

- RED: suíte imutável contra o baseline 3d6d... (sandbox) → esperado 34=24FAIL/10OK, exit1.
- VERDE: suíte imutável com REVIEW_MODULE no fonte corrigido → 34 OK, exit0.
- Positivo: suíte autor (21) e contra-prova (8/8) no fonte corrigido.
- Cada correção mostrada reprovando ANTES (RED) e passando depois.
