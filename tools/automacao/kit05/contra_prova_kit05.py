#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contra_prova_kit05.py - KIT-05F: contra-prova DURAVEL do pipeline passivo.

Por que este arquivo existe (achados F7 e F9 do parecer KIT-05R)
----------------------------------------------------------------
* F7 - o runner do KIT-05 dependia de `git rev-parse` e de uma contra-prova
  descartavel em `scratch/`. Aqui a contra-prova e PARTE DURAVEL da ferramenta
  (`tools/automacao/kit05/`), resolve a raiz pelo PROPRIO LAYOUT (sem `.git`,
  sem ascender ao repo do dono) e roda offline (sem Hermes/IA/credenciais).
* F9 - a contra-prova antiga aceitava "exit != 0 + nome do teste presente no
  output verbose", o que da VERDE quando o alvo PASSA e outro teste falha.
  Aqui o discriminador exige:
    - exit 1 (do unittest com falha),
    - `FAIL:` do ALVO declarado e o conjunto EXATO de testes que falharam,
    - presenca de `AssertionError`,
    - AUSENCIA de `ERROR:`, de skip e de execucao vazia/estourada por timeout.
  E ha um controle adversarial explicito (`controle_falso_verde`): um defeito
  plantado que derruba OUTRO teste tem de ser RECUSADO pela contra-prova.

Uso:
    python tools/automacao/kit05/contra_prova_kit05.py
    python tools/automacao/kit05/contra_prova_kit05.py --individual
    PYTHON=/caminho/python python tools/automacao/kit05/contra_prova_kit05.py

Exit: 0 = verde (todas as iscas reprovaram como deviam e o controle falso-verde
foi recusado); 1 = vermelho (alguma regra nao e coberta / o oraculo foi
enganado); 2 = erro de infraestrutura (layout/fonte ausente).

Nunca escreve no modulo original: cada isca roda numa COPIA temporaria.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))                 # .../kit05
RAIZ = os.path.dirname(os.path.dirname(AQUI))                     # raiz do repo
REL_MODULO = os.path.join("tools", "automacao", "runtime", "observacao_passiva.py")
REL_TESTE = os.path.join("tools", "automacao", "kit05",
                         "teste_observacao_passiva.py")


def resolver_layout(inicio=AQUI):
    """F7: resolve a raiz pelo LAYOUT (nunca por `git rev-parse`)."""
    atual = os.path.abspath(inicio)
    for _ in range(8):
        modulo = os.path.join(atual, REL_MODULO)
        teste = os.path.join(atual, REL_TESTE)
        if os.path.isfile(modulo) and os.path.isfile(teste):
            return atual, modulo, teste
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    return None, None, None


RAIZ_RESOLVIDA, MODULO, TESTE = resolver_layout()

# --------------------------------------------------------------------------
# Mutacoes (defeitos plantados). Cada uma e uma lista de pares (velho, novo).
# --------------------------------------------------------------------------
MUTACOES = {
    "trava_modo_passivo": [
        ("if tipo in TIPOS_ATIVOS:", "if False:"),
    ],
    "dedup_por_mudanca": [
        ("if self._ultimo_estado.get(fonte) == assinatura:",
         "if False:"),
    ],
    "dedup_global_ignora_fonte": [
        ("fonte = janela if janela is not None else FONTE_GLOBAL",
         "fonte = FONTE_GLOBAL"),
    ],
    "dedup_ignora_janela_na_assinatura": [
        ("    return (tipo, janela, itens)", "    return (tipo, itens)"),
    ],
    "dedup_global_sem_janela": [
        ("fonte = janela if janela is not None else FONTE_GLOBAL",
         "fonte = FONTE_GLOBAL"),
        ("    return (tipo, janela, itens)", "    return (tipo, itens)"),
    ],
    "fila_limitada": [
        ("while len(self._eventos) > self.fila_max:", "while False:"),
    ],
    "teto_capturas": [
        ("if self._capturas_solicitadas >= self.teto_capturas:", "if False:"),
    ],
    "pausa_segura": [
        ('        if self._pausado:\n'
         '            self._degrada("pausado", tipo=tipo, detalhe="entrada '
         'descartada em pausa")\n'
         '            return None',
         '        if False:\n'
         '            self._degrada("pausado", tipo=tipo, detalhe="entrada '
         'descartada em pausa")\n'
         '            return None'),
    ],
    "pausa_invalida_pendencia": [
        ("invalidadas = list(self._pendentes.keys())\n            "
         "self._pendentes.clear()",
         "invalidadas = []\n            pass"),
    ],
    "pausa_nao_bloqueia_captura": [
        ("        if self._pausado:\n"
         "            self._capturas_recusadas += 1\n"
         '            self._degrada("pausado", tipo=evento.get("tipo"),',
         "        if False:\n"
         "            self._capturas_recusadas += 1\n"
         '            self._degrada("pausado", tipo=evento.get("tipo"),'),
    ],
    "sem_simultaneidade": [
        ('"lacunas_total": self._lacunas_total,\n'
         '            "simultaneidade_afirmada": False,',
         '"lacunas_total": self._lacunas_total,\n'
         '            "simultaneidade_afirmada": True,'),
    ],
    "timeout_clique_sem_janela": [
        ('if agora < pend["prazo_ms"]:', "if False:"),
    ],
    "janela_tardia_resolve": [
        ("        self._materializar_vencidos(agora)\n"
         "        self._resolve_janela(janela, agora)",
         "        self._resolve_janela(janela, agora)"),
        ('if agora <= pend["prazo_ms"]:', "if True:"),
    ],
    "pedido_marca_captura": [
        ('evento["quadro"]["solicitacao_id"] = captura_id',
         'evento["quadro"]["solicitacao_id"] = captura_id\n'
         '        evento["quadro"]["captura_apos_atualizacao_visual"] = True'),
    ],
    "confirmacao_sem_png": [
        ("        if not caminho or not os.path.isfile(caminho):",
         "        if False:"),
    ],
    "confirmacao_sem_quadro_posterior": [
        ("        if ind is None or int(ind) <= indice_evento:",
         "        if False:"),
    ],
    "limite_aux_degrada": [
        ("        while len(self._degradacoes) > self.limite_aux:",
         "        while False:"),
    ],
    "limite_aux_rejeitados": [
        ("        while len(self._rejeitados) > self.limite_aux:",
         "        while False:"),
    ],
    "limite_aux_pendentes": [
        ("        while len(self._pendentes) > self.limite_aux:",
         "        while False:"),
    ],
    # ---- mutacoes adicionais (descoberta por teste; --descobrir) ----
    "x_id_repetido": [
        ('            "id": uuid.uuid4().hex,\n'
         '            "sessao": self.id_sessao,\n'
         '            "tipo": tipo,',
         '            "id": "id-fixo",\n'
         '            "sessao": self.id_sessao,\n'
         '            "tipo": tipo,'),
    ],
    "x_clique_deduplicado": [
        ("if tipo != CLIQUE_RECEBIDO:", "if True:"),
    ],
    "x_tipos_observados_reduzidos": [
        ("TIPOS_OBSERVADOS = (CLIQUE_RECEBIDO, JANELA_ABERTA, JANELA_FECHADA, "
         "TOOLTIP)",
         "TIPOS_OBSERVADOS = (CLIQUE_RECEBIDO, JANELA_ABERTA, JANELA_FECHADA)"),
    ],
    "x_rejeita_desconhecido_rotulo": [
        ('self._rejeita(tipo, "tipo_desconhecido")',
         'self._rejeita(tipo, "motivo_errado")'),
    ],
    "x_dado_ativo_ignorado": [
        ("ativas = sorted(k for k in dados if k in CHAVES_ATIVAS)",
         "ativas = []"),
    ],
    "x_retencao_idade_ignorada": [
        ("        if self.retencao_ms > 0:", "        if False:"),
    ],
    "x_retencao_tamanho_ignorada": [
        ("        if len(self._eventos) > self.retencao_max:\n"
         "            for sai in self._eventos[:-self.retencao_max]:",
         "        if False:\n"
         "            for sai in self._eventos[:-self.retencao_max]:"),
    ],
    "x_janela_resolve_qualquer": [
        ('if pend["janela"] != janela:', "if False:"),
    ],
    "x_timeout_sem_motivo": [
        ('"motivo": "clique recebido sem janela dentro do timeout",',
         '"motivo": "",'),
    ],
    "x_dedup_ignora_tipo": [
        ("    return (tipo, janela, itens)", "    return (janela, itens)"),
    ],
    "x_dedup_sempre": [
        ("if self._ultimo_estado.get(fonte) == assinatura:", "if True:"),
    ],
    "x_confirmacao_nao_marca": [
        ('        evento["quadro"]["captura_apos_atualizacao_visual"] = True\n'
         '        evento["quadro"]["captura_id"] = captura_id',
         '        evento["quadro"]["captura_apos_atualizacao_visual"] = False\n'
         '        evento["quadro"]["captura_id"] = captura_id'),
    ],
    "x_pedido_quadro_anterior_aceito": [
        ("        if indice_quadro is not None and int(indice_quadro) < "
         "indice_evento:", "        if False:"),
    ],
    "x_captura_inexistente_rotulo": [
        ('self._degrada("captura_evento_inexistente", detalhe=str(evento_id))',
         'self._degrada("evento_fantasma", detalhe=str(evento_id))'),
    ],
    "replay_lista_paralela": [
        ('        obs.registrar(tipo, dados=ent.get("dados"),\n'
         '                      janela=ent.get("janela"), quadro=ent.get("quadro"))',
         '        _ev = obs.registrar(tipo, dados=ent.get("dados"),\n'
         '                            janela=ent.get("janela"), '
         'quadro=ent.get("quadro"))\n'
         '        if _ev:\n'
         '            obs._lista_paralela = getattr('
         'obs, "_lista_paralela", []) + [_ev]'),
        ("    eventos = obs.eventos()\n"
         "    falhas = [e for e in eventos if e.get(\"tipo\") == "
         "FALHA_CLIQUE_SEM_JANELA]\n"
         "    return obs, eventos, falhas",
         "    eventos = getattr(obs, \"_lista_paralela\", None) or obs.eventos()\n"
         "    falhas = [e for e in eventos if e.get(\"tipo\") == "
         "FALHA_CLIQUE_SEM_JANELA]\n"
         "    return obs, eventos, falhas"),
    ],
}

# Iscas por REGRA: (nome, mutacao, testes que DEVEM falhar, espera_aceitar)
ISCAS = (
    ("A_trava_modo_passivo", "trava_modo_passivo",
     ("test_rejeita_tipo_ativo",), True),
    ("B_dedup_por_mudanca", "dedup_por_mudanca",
     ("test_estado_repetido_nao_vira_evento",
      "test_intercalacao_constante_nao_gera_spam"), True),
    ("C_fila_limitada", "fila_limitada",
     ("test_fila_limitada_descarta_e_declara",), True),
    ("D_teto_capturas", "teto_capturas",
     ("test_teto_de_capturas",), True),
    ("E_pausa_segura", "pausa_segura",
     ("test_pausa_descarta_e_retoma",), True),
    ("F_sem_simultaneidade", "sem_simultaneidade",
     ("test_nenhum_evento_afirma_simultaneidade",), True),
    ("G_timeout_respeita_prazo", "timeout_clique_sem_janela",
     ("test_fronteira_exata_gera_uma_falha_e_nao_duplica",
      "test_janela_resolve_e_nao_gera_falha",
      "test_timeout_antes_do_prazo_nao_gera_falha"), True),
    ("H_pausa_invalida_pendencia", "pausa_invalida_pendencia",
     ("test_pausa_invalida_pendencia_nao_observada",), True),
    ("I_dedup_fonte_global", "dedup_global_ignora_fonte",
     ("test_intercalacao_constante_nao_gera_spam",), True),
    ("I2_dedup_global_sem_janela", "dedup_global_sem_janela",
     ("test_janelas_distintas_com_dados_iguais_coexistem",
      "test_intercalacao_constante_nao_gera_spam"), True),
    ("J_pedido_nao_e_captura", "pedido_marca_captura",
     ("test_confirmacao_exige_png_real",
      "test_confirmacao_exige_quadro_posterior",
      "test_confirmacao_exige_sessao_e_evento_coerentes",
      "test_pausa_bloqueia_pedido_e_confirmacao_de_captura",
      "test_pedido_nao_confirma_captura"), True),
    ("K_confirmacao_exige_png", "confirmacao_sem_png",
     ("test_confirmacao_exige_png_real",), True),
    ("L_confirmacao_exige_quadro", "confirmacao_sem_quadro_posterior",
     ("test_confirmacao_exige_quadro_posterior",), True),
    ("M_limite_degrada", "limite_aux_degrada",
     ("test_todo_estado_auxiliar_e_limitado_sob_milhares",
      "test_limite_aux_explicito_pode_ser_maior_finito"), True),
    ("N_limite_rejeitados", "limite_aux_rejeitados",
     ("test_todo_estado_auxiliar_e_limitado_sob_milhares",), True),
    ("O_limite_pendentes", "limite_aux_pendentes",
     ("test_todo_estado_auxiliar_e_limitado_sob_milhares",), True),
    ("P_janela_tardia", "janela_tardia_resolve",
     ("test_janela_tardia_nao_apaga_vencimento",), True),
    ("Q_pausa_bloqueia_captura", "pausa_nao_bloqueia_captura",
     ("test_pausa_bloqueia_pedido_e_confirmacao_de_captura",), True),
    ("R_replay_estado_retido", "replay_lista_paralela",
     ("test_replay_respeita_retencao_no_payload_final",
      "test_replay_nao_guarda_lista_paralela_de_falhas",
      "test_cli_rotula_fixture_offline_e_nao_promove_runtime"), True),
    # CONTROLE ADVERSARIAL (F9): o defeito plantado derruba OUTRO teste; o alvo
    # declarado (test_ids_unicos) continua PASSANDO. Um oraculo fraco (exit != 0
    # + nome presente no output verbose) daria VERDE aqui — o estrito tem de
    # RECUSAR.
    ("CONTROLE_falso_verde", "dedup_por_mudanca",
     ("test_ids_unicos",), False),
)

# Demonstracao POR TESTE (F9): cada teste da suite de contra-prova, rodando
# SOZINHO contra a mutacao declarada, tem de REPROVAR. Preenchido apos a
# descoberta empirica (--descobrir); nunca inventado.
TABELA_REPROVACAO = {
    'test_abrir_fechar_reabrir_sobrevive': 'x_dedup_ignora_tipo',
    'test_aceita_tipos_observados': 'x_dedup_ignora_tipo',
    'test_captura_evento_inexistente': 'x_captura_inexistente_rotulo',
    'test_cli_rotula_fixture_offline_e_nao_promove_runtime': 'replay_lista_paralela',
    'test_clique_nao_deduplica': 'x_clique_deduplicado',
    'test_confirmacao_com_png_e_quadro_posterior_confirma': 'x_confirmacao_nao_marca',
    'test_confirmacao_exige_png_real': 'confirmacao_sem_png',
    'test_confirmacao_exige_quadro_posterior': 'confirmacao_sem_quadro_posterior',
    'test_confirmacao_exige_sessao_e_evento_coerentes': 'pedido_marca_captura',
    'test_estado_repetido_nao_vira_evento': 'dedup_por_mudanca',
    'test_fila_limitada_descarta_e_declara': 'fila_limitada',
    'test_fronteira_exata_gera_uma_falha_e_nao_duplica': 'timeout_clique_sem_janela',
    'test_ids_unicos': 'x_id_repetido',
    'test_intercalacao_constante_nao_gera_spam': 'dedup_por_mudanca',
    'test_janela_de_outra_identidade_nao_resolve': 'x_janela_resolve_qualquer',
    'test_janela_resolve_e_nao_gera_falha': 'timeout_clique_sem_janela',
    'test_janela_tardia_nao_apaga_vencimento': 'janela_tardia_resolve',
    'test_janelas_distintas_com_dados_iguais_coexistem': 'dedup_global_sem_janela',
    'test_limite_aux_explicito_pode_ser_maior_finito': 'limite_aux_degrada',
    'test_mudanca_de_estado_vira_evento': 'x_dedup_sempre',
    'test_nenhum_evento_afirma_simultaneidade': 'sem_simultaneidade',
    'test_pausa_bloqueia_pedido_e_confirmacao_de_captura': 'pausa_nao_bloqueia_captura',
    'test_pausa_descarta_e_retoma': 'pausa_segura',
    'test_pausa_invalida_pendencia_nao_observada': 'pausa_invalida_pendencia',
    'test_pedido_com_quadro_anterior_e_recusado': 'x_pedido_quadro_anterior_aceito',
    'test_pedido_nao_confirma_captura': 'pedido_marca_captura',
    'test_rejeita_dado_ativo': 'x_dado_ativo_ignorado',
    'test_rejeita_tipo_ativo': 'trava_modo_passivo',
    'test_rejeita_tipo_desconhecido': 'x_rejeita_desconhecido_rotulo',
    'test_replay_nao_guarda_lista_paralela_de_falhas': 'replay_lista_paralela',
    'test_replay_respeita_retencao_no_payload_final': 'replay_lista_paralela',
    'test_retencao_por_idade': 'x_retencao_idade_ignorada',
    'test_retencao_por_tamanho': 'x_retencao_tamanho_ignorada',
    'test_teto_de_capturas': 'teto_capturas',
    'test_timeout_antes_do_prazo_nao_gera_falha': 'timeout_clique_sem_janela',
    'test_timeout_gera_falha_com_motivo': 'x_timeout_sem_motivo',
    'test_todo_estado_auxiliar_e_limitado_sob_milhares': 'limite_aux_degrada',
}

# Ordem de descoberta: mutacoes ESPECIFICAS primeiro, amplas por ultimo, para a
# atribuicao teste->mutacao ser a mais dirigida possivel (nao colateral).
ORDEM_DESCOBERTA = (
    "trava_modo_passivo", "x_rejeita_desconhecido_rotulo", "x_dado_ativo_ignorado",
    "dedup_por_mudanca", "x_dedup_ignora_tipo",
    "dedup_ignora_janela_na_assinatura", "dedup_global_ignora_fonte",
    "dedup_global_sem_janela",
    "fila_limitada", "x_retencao_idade_ignorada", "x_retencao_tamanho_ignorada",
    "limite_aux_degrada", "limite_aux_rejeitados",
    "limite_aux_pendentes", "x_id_repetido", "teto_capturas",
    "x_captura_inexistente_rotulo",
    "pausa_segura", "pausa_invalida_pendencia", "pausa_nao_bloqueia_captura",
    "timeout_clique_sem_janela", "x_janela_resolve_qualquer",
    "janela_tardia_resolve", "x_timeout_sem_motivo", "sem_simultaneidade",
    "confirmacao_sem_png", "confirmacao_sem_quadro_posterior",
    "x_confirmacao_nao_marca", "pedido_marca_captura",
    "x_pedido_quadro_anterior_aceito", "replay_lista_paralela",
    "x_tipos_observados_reduzidos",
    # Amplas por ultimo: quebram qualquer teste que precise de um evento aceito.
    "x_clique_deduplicado", "x_dedup_sempre",
)


def _aplica_mutacao(fonte, nome_mutacao):
    for velho, novo in MUTACOES[nome_mutacao]:
        if velho not in fonte:
            return None
    for velho, novo in MUTACOES[nome_mutacao]:
        fonte = fonte.replace(velho, novo)
    return fonte


def rodar(entradas, teste_alvo=None, mutacao=None, timeout=120):
    """Roda a suite (ou so `teste_alvo`) numa copia com a mutacao aplicada.

    Devolve (exit_code, saida). exit_code None = timeout/erro de execucao.
    """
    tmp = tempfile.mkdtemp(prefix="kit05f-cp-")
    try:
        shutil.copy2(TESTE, os.path.join(tmp, os.path.basename(TESTE)))
        with open(MODULO, encoding="utf-8") as fh:
            fonte = fh.read()
        if mutacao is not None:
            fonte = _aplica_mutacao(fonte, mutacao)
            if fonte is None:
                return None, "TRECHO NAO ENCONTRADO na fonte (isca invalida)"
        with open(os.path.join(tmp, "observacao_passiva.py"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(fonte)
        cmd = [sys.executable, os.path.join(tmp, os.path.basename(TESTE))]
        if teste_alvo:
            cmd.append(teste_alvo)
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              universal_newlines=True, timeout=timeout)
        return proc.returncode, proc.stdout or ""
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT (>%ds)" % timeout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def avaliar(saida, rc, alvos_esperados):
    """Discriminador ESTRITO (F9). Devolve (aceito, motivo)."""
    if rc is None:
        return False, "execucao nao concluida (timeout/erro): %s" % saida[:60]
    if rc == 0:
        return False, "exit 0 (o defeito plantado NAO derrubou nada)"
    if rc != 1:
        return False, "exit=%s (exige exit 1 de falha de teste)" % rc
    if "ERROR:" in saida:
        return False, "colateral: ERROR no output (nao e FAIL do alvo)"
    if re.search(r"Ran 0 tests", saida) or "skipped" in saida:
        return False, "nenhum teste rodou / houve skip"
    achados = sorted(set(re.findall(r"^FAIL: (\S+)", saida, re.M)))
    if not achados:
        return False, "nenhuma linha FAIL no output"
    esperado = sorted(alvos_esperados)
    if achados != esperado:
        return False, "FAIL inesperado/ausente: %s (esperado %s)" % (achados, esperado)
    if "AssertionError" not in saida:
        return False, "FAIL sem AssertionError (nao e falha de assercao do alvo)"
    if ("FAILED (failures=%d" % len(esperado)) not in saida:
        return False, "contagem de falhas diverge do declarado"
    return True, "FAIL do alvo: %s" % ", ".join(achados)


def _falso_verde_antigo(saida, rc, alvo):
    """Oraculo FRACO do KIT-05 (F9): exit != 0 + nome presente no output."""
    return rc is not None and rc != 0 and alvo in saida


def modo_regras():
    print("=" * 78)
    print(" KIT-05F contra-prova (regras) — discriminador ESTRITO (F9)")
    print("=" * 78)
    ok = True
    for nome, mutacao, alvos, espera_aceitar in ISCAS:
        rc, saida = rodar(None, mutacao=mutacao)
        aceito, motivo = avaliar(saida, rc, alvos)
        if espera_aceitar:
            estado = "OK (%s)" % motivo if aceito else "FALHA DA ISCA (%s)" % motivo
            if not aceito:
                ok = False
        else:
            # Controle adversarial: o discriminador TEM de recusar.
            if aceito:
                estado = "FALHA DO ORACULO (aceitou defeito fora do alvo)"
                ok = False
            else:
                estado = "OK (recusado: %s)" % motivo
            antigo = _falso_verde_antigo(saida, rc, alvos[0])
            estado += " | oraculo antigo aceitaria=%s" % antigo
        print("[%-28s] %s" % (nome, estado))
    print("=" * 78)
    if ok:
        print(" VEREDITO REGRAS: VERDE (todas as iscas reprovaram; "
              "controle falso-verde recusado)")
    else:
        print(" VEREDITO REGRAS: VERMELHO")
    return 0 if ok else 1


def _testes_da_suite():
    _, saida = rodar(None, mutacao=None)
    return sorted(set(re.findall(r"^(?:test_\w+) \(([\w.]+)\)", saida, re.M)))


def modo_descobrir():
    """Auxiliar: para cada teste, acha a mutacao que o derruba (rodando so o alvo)."""
    _, saida = rodar(None, mutacao=None)
    ids = []
    for metodo, qualificado in re.findall(r"^(test_\w+) \(([\w.]+)\)", saida, re.M):
        partes = qualificado.split(".")
        if len(partes) >= 2:
            ids.append((metodo, "%s.%s" % (partes[-2], partes[-1])))
    ids = sorted(ids, key=lambda par: par[1])
    print("# testes: %d" % len(ids))
    for metodo, qualificado in ids:
        achou = None
        ordem = [n for n in ORDEM_DESCOBERTA if n in MUTACOES]
        ordem += [n for n in MUTACOES if n not in ordem]
        for mut in ordem:
            rc, out = rodar(None, teste_alvo=qualificado, mutacao=mut)
            aceito, _ = avaliar(out, rc, (metodo,))
            if aceito:
                achou = mut
                break
        print("    %r: %r," % (metodo, achou))
    return 0


def _ids_qualificados():
    """Mapa metodo -> 'Classe.metodo' (unittest so aceita nome qualificado)."""
    _, saida = rodar(None, mutacao=None)
    mapa = {}
    for metodo, qualificado in re.findall(r"(?m)^(test_\w+) \(([\w.]+)\)", saida):
        partes = qualificado.split(".")
        if len(partes) >= 2:
            mapa[metodo] = "%s.%s" % (partes[-2], partes[-1])
    return mapa


def modo_individual():
    print("=" * 78)
    print(" KIT-05F contra-prova (por teste) — cada teste rodando SOZINHO")
    print("=" * 78)
    if not TABELA_REPROVACAO:
        print("TABELA_REPROVACAO vazia — rode --descobrir e embuta o resultado.")
        return 2
    qualificados = _ids_qualificados()
    ok = True
    faltando = []
    for teste, mutacao in sorted(TABELA_REPROVACAO.items()):
        qualificado = qualificados.get(teste)
        if mutacao is None or qualificado is None:
            faltando.append(teste)
            print("[%-58s] SEM MUTACAO/ID DECLARADO" % teste)
            ok = False
            continue
        rc, saida = rodar(None, teste_alvo=qualificado, mutacao=mutacao)
        aceito, motivo = avaliar(saida, rc, (teste,))
        print("[%-58s] %s" % (teste, "OK" if aceito else "FALHA (%s)" % motivo))
        if not aceito:
            ok = False
    print("=" * 78)
    if faltando:
        print(" VEREDITO TESTES: INCOMPLETO (%d sem mutacao/id)" % len(faltando))
        return 1
    print(" VEREDITO TESTES: %s (%d teste(s) reprovando individualmente)"
          % ("VERDE" if ok else "VERMELHO", len(TABELA_REPROVACAO)))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-05F contra-prova duravel.")
    ap.add_argument("--individual", action="store_true",
                    help="demonstra cada teste da suite reprovando sozinho")
    ap.add_argument("--descobrir", action="store_true",
                    help="auxiliar: descobre qual mutacao derruba cada teste")
    args = ap.parse_args(argv)

    if MODULO is None or TESTE is None:
        print("ERRO: layout nao resolvido (esperado <raiz>/%s e %s)"
              % (REL_MODULO, REL_TESTE))
        return 2
    if args.descobrir:
        return modo_descobrir()
    if args.individual:
        return modo_individual()
    return modo_regras()


if __name__ == "__main__":
    sys.exit(main())
