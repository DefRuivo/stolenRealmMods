#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai fatos verificaveis dos 20 eventos Normal 21-40 (somente leitura)."""
import json, re, os

BASE = r"C:/dev/stolen-realm/docs/cobertura/EV-R1"
EV = json.load(open(os.path.join(BASE, 'eventos.json'), encoding='utf-8'))
CAT = json.load(open(os.path.join(BASE, 'catalogo-referencias.json'), encoding='utf-8'))
REG = {r['path_id']: r for r in CAT['registros']}
EVENTOS = EV['eventos']
NORMAL = [e for e in EVENTOS if e['categoria'] == 'Normal']
SLICE = NORMAL[20:40]
ENUMS = json.load(open(os.path.join(BASE, 'enums.json'), encoding='utf-8'))

TERRAIN = {int(k): v for k, v in ENUMS['TerrainType'].items()}
NODETYPE = {int(k): v for k, v in ENUMS['NodeType'].items()}
QUALITY = {int(k): v for k, v in ENUMS['ItemQuality'].items()}
RESULT = {int(k): v for k, v in ENUMS['EventResultType'].items()}

def st(pid):
    r = REG.get(pid)
    return (r['data'].get('m_Name') if r else None)

def refinfo(ref):
    if not ref:
        return None
    return {'chave': ref.get('chave'), 'nome': ref.get('nome'), 'tipo': ref.get('tipo')}

facts = {'range': [21, 40], 'events': []}
for i, e in enumerate(SLICE, start=21):
    co = e['condicoes']
    opcoes = []
    for o in e['opcoes']:
        acts = []
        for a in o['efeitos']:
            eff = []
            for x in a['efeitos']:
                vm = x['vida_mana']
                rc = x['recompensas']
                eff.append({
                    'hp_max_pct': vm['percentMaxHealth'], 'mp_max_pct': vm['percentMaxMana'],
                    'alvo_default': x['alvo']['tipo_default_serializado']['nome'],
                    'alvo_override': x['alvo']['tipo_override']['nome'] if x['alvo']['override'] else None,
                    'ouro_dar': rc['ouro']['dar'], 'ouro_razao': rc['ouro']['razao'],
                    'ouro_retirar': rc['ouro']['retirar'],
                    'xp_dar': rc['experiencia']['dar'], 'xp_razao': rc['experiencia']['razao'],
                    'itens_dar': rc['itens']['dar'],
                    'itens_pool': (rc['itens']['pool_tipo'] or {}).get('nome'),
                    'itens_qtd': rc['itens']['quantidade_configurada'],
                    'itens_tabelas': len(rc['itens']['tabelas']),
                    'itens_tipos': rc['itens']['restricoes']['possibleItemTypes'],
                    'itens_rar': rc['itens']['restricoes']['possibleRarities'],
                    'status': [{'chave': c.get('chave'), 'nome': c.get('nome')} for c in rc['status']['candidatos']],
                    'status_sortear': rc['status']['sortear'],
                    'skills': [s.get('nome') for s in rc['skills']],
                    'remocoes': [{'chave': r.get('chave'), 'nome': r.get('nome')} for r in x['remocoes_status']],
                })
            b = a['batalha']
            acts.append({
                'indice': a['indice'], 'resultado': (a['resultado'] or {}).get('nome'),
                'limite_rolagem': a['limite_rolagem'], 'texto': a['texto'],
                'efeitos': eff,
                'batalha_iniciar': b['iniciar'], 'batalha_ref': refinfo(b['referencia']),
                'evento_encadeado': refinfo(a.get('evento_encadeado')),
                'overrides': len(a.get('overrides') or []),
            })
        opcoes.append({
            'indice': o['indice'], 'titulo': o['titulo'], 'texto': o['texto'],
            'status_requeridos': o['condicoes']['status_requeridos'],
            'ocultar_sem_requisitos': o['condicoes']['ocultar_sem_requisitos'],
            'ocultar_se_status': o['condicoes']['ocultar_se_status'],
            'rolagem_bonus': [{'valor': b['valor'], 'nome': b['nome']} for b in o['rolagem']['bonus']],
            'rolagem_misteriosa': o['rolagem']['misteriosa'],
            'acoes': acts,
        })
    facts['events'].append({
        'ordinal': i, 'chave': e['chave'], 'id': e['id'], 'titulo': e['titulo'],
        'nome_asset': e['nome_asset'], 'categoria': e['categoria'],
        'raridade_valor': e['raridade']['valor'], 'raridade_nome': e['raridade']['nome'],
        'peso': e['peso'], 'pool': [p['nome'] for p in e['pool']],
        'disabled': co['disabled'], 'minLevel': co['minLevel'],
        'allowedNodeTypes': [NODETYPE.get(x, x) for x in co['allowedNodeTypes']],
        'allowedTerrainTypes': [TERRAIN.get(x, x) for x in co['allowedTerrainTypes']],
        'allowOnAllTerrainTypes': co['allowOnAllTerrainTypes'],
        'allowAtAllTimesOfDay': co['allowAtAllTimesOfDay'], 'allowedTimeOfDay': co['allowedTimeOfDay'],
        'allowAtAllLevels': co['allowAtAllLevels'], 'isLesserEvent': co['isLesserEvent'],
        'LeadsToFortune': co['LeadsToFortune'], 'KeepInDeckWhenUsed': co['KeepInDeckWhenUsed'],
        'requiredStatusesToSpawn': co['requiredStatusesToSpawn'],
        'terrainTypesAllowedAtAnyTime': [TERRAIN.get(x, x) for x in co['terrainTypesAllowedAtAnyTime']],
        'modos': [m['nome'] for m in e['modos']], 'historia': e['historia']['nome'],
        'full_release': e['full_release']['nome'],
        'texto': e['texto'], 'texto_len': len(e['texto']),
        'texto_resultados_possiveis': e['texto_resultados_possiveis'],
        'origem_path_id': e['origem']['path_id'], 'sha256': e['origem']['sha256_objeto'],
        'caminhos_resource': e['origem']['caminhos_resource'],
        'n_opcoes': len(e['opcoes']), 'n_acoes': sum(len(o['efeitos']) for o in e['opcoes']),
        'opcoes': opcoes,
        'nulls': sorted(e['ausencias'].keys()),
    })

# --- contagens / agregados verificaveis ---
agg = {}
agg['eventos'] = len(SLICE)
agg['chaves_unicas'] = len({e['chave'] for e in SLICE})
agg['ids_unicos'] = len({e['id'] for e in SLICE})
agg['opcoes_total'] = sum(len(e['opcoes']) for e in SLICE)
agg['acoes_total'] = sum(len(o['efeitos']) for e in SLICE for o in e['opcoes'])
agg['acoes_success'] = sum(1 for e in SLICE for o in e['opcoes'] for a in o['efeitos']
                           if (a['resultado'] or {}).get('nome') == 'Success')
agg['acoes_failure'] = sum(1 for e in SLICE for o in e['opcoes'] for a in o['efeitos']
                           if (a['resultado'] or {}).get('nome') == 'Failure')
agg['sem_narrativa'] = [i for i, e in enumerate(SLICE, 21) if len(e['texto']) <= 1]
agg['disabled'] = [i for i, e in enumerate(SLICE, 21) if e['condicoes']['disabled'] == 1]
agg['uma_opcao'] = [i for i, e in enumerate(SLICE, 21) if len(e['opcoes']) == 1]
agg['com_failure'] = [i for i, e in enumerate(SLICE, 21)
                      if any((a['resultado'] or {}).get('nome') == 'Failure' for o in e['opcoes'] for a in o['efeitos'])]
agg['com_rolagem'] = [i for i, e in enumerate(SLICE, 21) if any(o['rolagem']['bonus'] for o in e['opcoes'])]
agg['rolagem_sem_failure'] = [i for i, e in enumerate(SLICE, 21)
                              if any(o['rolagem']['bonus'] for o in e['opcoes'])
                              and not any((a['resultado'] or {}).get('nome') == 'Failure' for o in e['opcoes'] for a in o['efeitos'])]
agg['leads_to_fortune'] = [i for i, e in enumerate(SLICE, 21) if e['condicoes']['LeadsToFortune'] == 1]
agg['raridade'] = {}
for i, e in enumerate(SLICE, 21):
    agg['raridade'].setdefault(e['raridade']['nome'], []).append(i)
agg['peso'] = {}
for i, e in enumerate(SLICE, 21):
    agg['peso'].setdefault(e['peso'], []).append(i)
agg['nulls_total'] = sum(len(e['ausencias']) for e in SLICE)
agg['inicia_batalha'] = [i for i, e in enumerate(SLICE, 21)
                         if any(a['batalha']['iniciar'] for o in e['opcoes'] for a in o['efeitos'])]
agg['emite_status'] = [i for i, e in enumerate(SLICE, 21)
                       if any(x['recompensas']['status']['candidatos'] for o in e['opcoes'] for a in o['efeitos'] for x in a['efeitos'])]
agg['da_item'] = [i for i, e in enumerate(SLICE, 21)
                  if any(x['recompensas']['itens']['dar'] for o in e['opcoes'] for a in o['efeitos'] for x in a['efeitos'])]
agg['da_xp'] = [i for i, e in enumerate(SLICE, 21)
                if any(x['recompensas']['experiencia']['dar'] for o in e['opcoes'] for a in o['efeitos'] for x in a['efeitos'])]
agg['da_ouro'] = [i for i, e in enumerate(SLICE, 21)
                  if any(x['recompensas']['ouro']['dar'] for o in e['opcoes'] for a in o['efeitos'] for x in a['efeitos'])]
agg['acao_sem_texto'] = [i for i, e in enumerate(SLICE, 21)
                         if any(a['texto'] == '' for o in e['opcoes'] for a in o['efeitos'])]
agg['opcao_sem_texto'] = [i for i, e in enumerate(SLICE, 21)
                          if any(o['texto'] == '' for o in e['opcoes'])]
agg['com_status_requerido'] = [i for i, e in enumerate(SLICE, 21)
                               if any(o['condicoes']['status_requeridos'] for o in e['opcoes'])]
agg['batalha_sem_ref'] = [i for i, e in enumerate(SLICE, 21)
                          if any(a['batalha']['iniciar'] and not a['batalha']['referencia'].get('chave')
                                 for o in e['opcoes'] for a in o['efeitos'])]
agg['nulos_por_ordinal'] = {str(i): len(e['ausencias']) for i, e in enumerate(SLICE, 21)}
facts['agregados'] = agg

json.dump(facts, open('EV-R2-NORMAL-b02-parte02-fatos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(agg, ensure_ascii=False, indent=1))
