"""COR-AUT6 E1-E9: regressao permanente, bytes e CLI reais em sandbox.

Nenhum dado deste teste e coleta de jogo; ambiente_prova=teste_contrato impede
promocao. Os contraexemplos verificam o motivo, nao so RV-49/exit global.
"""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import cobertura as co
import observacoes_fixture as of
import prova
import suporte_testes as st


def casos(*ids):
    dados = json.loads(Path(co.CASOS_PADRAO).read_text(encoding='utf-8'))
    return {'casos': [c for c in dados['casos'] if c['id'] in ids]}


def avaliar_corpo(obs, ident):
    return co.avaliar(obs, ident, {'casos': [st.CASO_CORPO]})


def decisao():
    path = Path(co.REPO) / 'tools/automacao/ciclo/decisao.py'
    spec = importlib.util.spec_from_file_location('aut6_decisao', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Regressao(unittest.TestCase):
    def setUp(self):
        self.obs, self.ident = st.gravar([st.corpo()], self._testMethodName)

    def sem_prova(self, cs):
        self.assertTrue(cs)
        self.assertFalse(any(c['prova_runtime'] for c in cs))
        for c in cs:
            self.assertNotEqual(decisao().normalizar_criterio(c, self.ident, co.REPO)['classificacao'], 'OK_VINCULANTE')

    def test_E1_fixture_prioridade(self):
        for campo, valor in [('rotulo_fixture', True), ('evidencia_runtime', False)]:
            o = copy.deepcopy(self.obs)
            o[0][campo] = valor
            self.assertEqual(co._rotulo(o[0]), 'fixture')
            self.sem_prova(avaliar_corpo(o, self.ident))

    def test_E1_arquivo_alheio_e_pointer(self):
        unrelated = st.ROOT / 'baseline.json'
        unrelated.write_text('{"qualquer":"conteudo"}', encoding='utf-8')
        o = copy.deepcopy(self.obs)
        o[0]['evidencia'] = [str(unrelated)]
        cs = avaliar_corpo(o, self.ident)
        self.assertTrue(all(c['estado'] != 'OK' for c in cs))
        self.sem_prova(cs)
        o = copy.deepcopy(self.obs)
        o[0]['evidencia'][0]['ponteiro'] = '/observacoes/999'
        self.assertEqual(co._cadeia(o[0], st.cadeia_kw(self.ident))[0], 'NAO_EXERCITADO')

    def test_E1_valor_objeto_nao_vinculado(self):
        for key, valor in [('texto_renderizado', 'Shrine Effect Bonus Your active shrine auras: INVENTADO'),
                           ('objeto', 'Outro/Objeto'), ('personagem', 'Outro'), ('cenario', 'Outro')]:
            o = copy.deepcopy(self.obs[0])
            o[key] = valor
            estado, motivo = co._cadeia(o, st.cadeia_kw(self.ident))
            self.assertEqual(estado, 'INDETERMINADO', motivo)
            self.assertIn(key, motivo)

    def test_E1_bytes_adulterados(self):
        ref = self.obs[0]['evidencia'][0]
        path = Path(ref['caminho'])
        path.write_text(path.read_text(encoding='utf-8')+' ', encoding='utf-8')
        self.assertEqual(co._cadeia(self.obs[0], st.cadeia_kw(self.ident))[0], 'INDETERMINADO')
        self.sem_prova(avaliar_corpo(self.obs, self.ident))

    def test_E1_rotulo_teste_nao_removivel(self):
        self.obs[0].pop('ambiente_prova')
        self.assertEqual(co._cadeia(self.obs[0], st.cadeia_kw(self.ident))[0], 'INDETERMINADO')
        self.sem_prova(avaliar_corpo(self.obs, self.ident))

    def test_E2_completude_por_todo_criterio(self):
        cs = [{'id': str(i), 'estado': 'OK', 'prova_runtime': False} for i in range(20)]
        cs[-1]['prova_runtime'] = True
        self.assertEqual(co.exit_de(cs), 2)
        for c in cs:
            c['prova_runtime'] = True
        self.assertEqual(co.exit_de(cs), 0)  # teste do agregador, nao criterio/prova de produto
        self.assertEqual(co.exit_de([]), 2)

    def test_E3_sessao_velha(self):
        self.obs[0]['sessao'] = 'velha'
        estado, motivo = co._cadeia(self.obs[0], st.cadeia_kw(self.ident))
        self.assertEqual(estado, 'INDETERMINADO')
        self.assertIn('sessao', motivo)

    def test_E3_fonte_config_ausentes(self):
        for key in ('fonte_sha', 'dll_sha', 'config_sha'):
            o = copy.deepcopy(self.obs[0])
            o.pop(key)
            estado, motivo = co._cadeia(o, st.cadeia_kw(self.ident))
            self.assertEqual(estado, 'NAO_EXERCITADO')
            self.assertIn(key, motivo)

    def test_E3_alias_contraditorio(self):
        self.obs[0]['hash_fonte'] = 'f'*64
        self.assertEqual(co._cadeia(self.obs[0], st.cadeia_kw(self.ident))[0], 'INDETERMINADO')

    def test_E4_totais_impossiveis(self):
        obs = of.constroi()
        for o in obs:
            o['feed'] = o.get('feed', '').replace('total=+50% cru=+90%', 'total=+999% cru=+999%').replace('total=−75% cru=−100%', 'total=−999% cru=−999%')
        cs = co.avaliar(obs, None, casos('S-rv46-teto-damage-reduction', 'S-rv50-piso-mana-cost'))
        self.assertEqual([c['estado'] for c in cs], ['REPROVADO', 'REPROVADO'])
        self.assertTrue(all('clamp' in c['motivo'] for c in cs))

    def test_E4_contribuicao_ausente(self):
        obs = of.constroi()
        for o in obs:
            o['feed'] = '\n'.join(l for l in o.get('feed', '').splitlines() if 'RV-31 acumulado' not in l)
        cs = co.avaliar(obs, None, casos('S-rv46-teto-damage-reduction', 'S-rv50-piso-mana-cost'))
        self.assertTrue(all(c['estado'] == 'NAO_EXERCITADO' and 'contribuicao' in c['motivo'] for c in cs))

    def test_E4_cru_flag_e_total_item(self):
        for antigo, novo, motivo in [(' cru=+90%', '', 'medidos'), ('no-teto=sim', 'no-teto=nao', 'clamp'),
                                    ('Damage taken −40% (total −50%)', 'Damage taken −40% (total −49%)', 'contradiz')]:
            obs = of.constroi()
            for o in obs:
                o['feed'] = o.get('feed', '').replace(antigo, novo)
            cs = co.avaliar(obs, None, casos('S-rv46-teto-damage-reduction'))
            self.assertNotEqual(cs[0]['estado'], 'OK')
            self.assertIn(motivo, cs[0]['motivo'])

    def test_E5_inativo_erro(self):
        for key, value in [('ativo_na_hierarquia', False), ('visivel_na_tela', False), ('status', 'ERRO'), ('ok', False)]:
            raw = st.corpo()
            raw[key] = value
            obs, ident = st.gravar([raw], self._testMethodName+key)
            cs = avaliar_corpo(obs, ident)
            self.assertNotEqual(cs[0]['estado'], 'OK')
            self.sem_prova(cs)

    def test_E5_cor_posicao_e_ausencia(self):
        for key, value, pid in [('linha_azul_cor', '#FF0000', '/cor'), ('linha_azul_ultima', False, '/posicao'),
                                ('linha_azul_retangulo', {'x': 999, 'y': 0, 'largura': 5, 'altura': 5}, '/posicao')]:
            raw = st.corpo()
            raw[key] = value
            obs, ident = st.gravar([raw], self._testMethodName+key)
            cs = avaliar_corpo(obs, ident)
            self.assertEqual(next(c for c in cs if c['id'].endswith(pid))['estado'], 'REPROVADO')
        raw = st.corpo()
        for key in ('linha_azul_cor', 'linha_azul_retangulo'):
            raw.pop(key)
        obs, ident = st.gravar([raw], 'style-missing')
        self.assertTrue(all(c['estado'] == 'NAO_EXERCITADO' for c in avaliar_corpo(obs, ident)[1:]))

    def test_E6_feed_benigno_flutuante_vazado(self):
        obs = of.constroi()
        for o in obs:
            if o.get('superficie') == 'feed':
                o['feed'] = 'Increased Armor'
                o['texto_renderizado'] = 'Armor blocks damage: vazamento'
        cs = co.avaliar(obs, None, casos('S-bug34-armor-feed-e-corpo'))
        self.assertEqual(next(c for c in cs if c['id'].endswith('/feed'))['estado'], 'REPROVADO')
        self.assertEqual(next(c for c in cs if c['id'].endswith('/flutuante'))['estado'], 'REPROVADO')
        self.assertTrue(all(c['reabre_bug'] is False for c in cs))

    def test_E6_superficies_separadas_obrigatorias(self):
        cfg = casos('S-bug34-armor-feed-e-corpo')
        raw = st.corpo()
        raw.update(cenario=cfg['casos'][0]['id'], superficie='feed', feed='Increased Armor', texto_renderizado='Increased Armor')
        obs, ident = st.gravar([raw], 'armor-sem-flutuante')
        cs = co.avaliar(obs, ident, cfg)
        self.assertEqual(next(c for c in cs if c['id'].endswith('/flutuante'))['estado'], 'NAO_EXERCITADO')

    def test_E7_regressao_posterior(self):
        bom, ruim = st.corpo(), st.corpo()
        ruim['texto_renderizado'] = 'regression: missing line and note'
        obs, ident = st.gravar([bom, ruim], 'posterior')
        cs = avaliar_corpo(obs, ident)
        self.assertNotEqual(cs[0]['estado'], 'OK')
        self.assertEqual(len(cs[0]['medicoes']), 2)
        self.sem_prova(cs)

    def test_E7_alvo_cenario_diferente(self):
        raw = st.corpo()
        raw['cenario'] = 'outro-cenario'
        obs, ident = st.gravar([raw], 'alvo-errado')
        self.assertTrue(all(c['estado'] == 'NAO_EXERCITADO' for c in avaliar_corpo(obs, ident)))
        a, b = st.corpo(), st.corpo()
        b['personagem'] = 'TesteB'
        obs, ident = st.gravar([a, b], 'alvo-ambiguo')
        self.assertEqual(avaliar_corpo(obs, ident)[0]['estado'], 'INDETERMINADO')

    def test_E7_observacao_sem_cenario_ambigua(self):
        """A mesma medicao sem cenario declarado nao pode 'servir' para dois casos como OK."""
        raw = st.corpo()
        raw.pop('cenario')
        obs, ident = st.gravar([raw], 'sem-cenario')
        cfg = json.loads(Path(co.CASOS_PADRAO).read_text(encoding='utf-8'))
        dois = [c for c in cfg['casos'] if c['id'] == st.CASO_CORPO['id']]
        dois.append(next(c for c in cfg['casos'] if c['tipo'] == 'divergencia_rv49'))
        cs = co.avaliar(obs, ident, {'casos': dois})
        self.assertTrue(all(c['estado'] == 'INDETERMINADO' for c in cs if c['procedencia'] == 'runtime'
                            and c['id'] != 'S-aut6-completude-runtime'), cs)

    def test_E8_normalizador_real_adapter_CIC2(self):
        self.obs[0]['hash_fonte'] = self.obs[0]['dll_sha']
        # Hash alias e incorporado nos bytes ANTES de normalizar, nao emprestado da identidade.
        obs, ident = st.gravar(self.obs, 'costura-real')
        norm = co.normalizar_aut4(obs[0], alvos=['texto_renderizado', 'ativo_na_hierarquia', 'personagem'])
        self.assertEqual(norm['campos']['texto_renderizado']['valor'], obs[0]['texto_renderizado'])
        for key in ('superficie', 'cenario', 'personagem', 'sessao', 'fonte_sha', 'dll_sha', 'config_sha', 'origem'):
            self.assertEqual(norm[key], obs[0][key])
        cs = avaliar_corpo([norm], ident)
        self.assertTrue(all(c['estado'] == 'OK' for c in cs), cs)
        self.sem_prova(cs)  # shape completa de teste nunca aprovacao de runtime/produto
        # CLI real do produtor e do consumidor; sem reconstruir criterios para o CIC2.
        folder = st.ROOT / 'cli-costura'
        folder.mkdir(exist_ok=True)
        for name, data in [('obs', [norm]), ('ident', ident), ('casos', {'casos': [st.CASO_CORPO]})]:
            (folder/(name+'.json')).write_text(json.dumps(data), encoding='utf-8')
        cmd = [sys.executable, str(Path(co.AQUI)/'cobertura.py'), '--observacoes', str(folder/'obs.json'), '--identidade', json.dumps(ident), '--casos', str(folder/'casos.json'), '--json', str(folder/'criterios.json')]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 2, p.stdout+p.stderr)
        q = subprocess.run([sys.executable, str(Path(co.REPO)/'tools/automacao/ciclo/decisao.py'), '--criterios', str(folder/'criterios.json'), '--identidade', str(folder/'ident.json'), '--repo', co.REPO, '--out', str(folder/'decisao.json')], capture_output=True, text=True, timeout=60)
        self.assertEqual(q.returncode, 1, q.stdout+q.stderr)
        d = json.loads((folder/'decisao.json').read_text(encoding='utf-8'))
        self.assertEqual(d['resumo']['ok_vinculantes'], 0)

    def test_E8_campos_normalizados_ja_sem_superficie(self):
        path = Path(co.REPO)/'tools/automacao/runtime/coletor.py'
        spec = importlib.util.spec_from_file_location('aut4_direto', path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        raw = st.corpo()
        raw['hash_fonte'] = raw['dll_sha']
        norm = m.normalizar_observacao(raw, 'runtime', alvos=['texto_renderizado'])
        self.assertNotIn('superficie', norm)
        self.assertTrue(all(c['estado'] == 'NAO_EXERCITADO' for c in avaliar_corpo([norm], self.ident)))

    def test_E8_RV49_residual_sem_apagar_divergencia(self):
        cs = co.avaliar([], self.ident, casos('S-rv49-divergencia-perigo'))
        c = cs[0]
        self.assertEqual(c['estado'], 'INDETERMINADO')
        self.assertEqual(c['classe'], 'runtime')
        self.assertIn('fato_30_09', c['esperado'])
        self.assertIn('fato_03_10', c['esperado'])
        self.assertFalse(c['autorizacao_necessaria'])
        self.assertIn('RV-49', c['lacuna_probe'])
        d = decisao().consolidar(cs, self.ident)
        self.assertEqual([f['id'] for f in d['falhas_automaticas']],
                         ['S-rv49-divergencia-perigo', 'S-aut6-completude-runtime'],
                         'RV-49 tem de virar falha automatica (com o agregado acusando a lacuna)')
        self.assertEqual(d['resumo']['pendencias_humanas'], 0)
        self.assertEqual(d['resumo']['ok_vinculantes'], 0)
        self.assertFalse(d['pronto_para_decisao'])
        rv49 = next(f for f in d['falhas_automaticas'] if f['id'] == 'S-rv49-divergencia-perigo')
        self.assertIn('RV-49', rv49['lacuna_probe'])
        self.assertTrue(rv49['esperado']['fato_30_09'] and rv49['esperado']['fato_03_10'],
                        'a classificacao automatica nao pode apagar a divergencia')

    def test_E2_completude_no_consumidor(self):
        """Isolar criterios NAO aprova a rodada padrao: o agregado acusa a lacuna por criterio."""
        obs, ident = st.gravar([st.corpo()], 'completude')
        parcial = co.avaliar(obs, ident, {'casos': [st.CASO_CORPO]})
        self.assertNotIn('S-aut6-completude-runtime', [c['id'] for c in parcial])
        rodada = json.loads(Path(co.CASOS_PADRAO).read_text(encoding='utf-8'))
        do_corpo = [c for c in rodada['casos'] if c['id'] == st.CASO_CORPO['id']]
        do_corpo.append(next(c for c in rodada['casos'] if c['tipo'] == 'divergencia_rv49'))
        completa = co.avaliar(obs, ident, {'casos': do_corpo})
        agregado = next(c for c in completa if c['id'] == 'S-aut6-completude-runtime')
        self.assertEqual(agregado['estado'], 'NAO_EXERCITADO')
        self.assertIn('S-rv49-divergencia-perigo', agregado['observado']['lacunas'])
        self.assertEqual(co.exit_de(completa), 2)

    def test_E8_transicao_mesmo_personagem_sessao(self):
        cfg = casos('S-rv29-dentro-da-aura', 'S-rv29-fora-da-aura')
        a = st.corpo()
        a.update(cenario=[c['id'] for c in cfg['casos']], dentro_da_aura=True, sequencia=1,
                 feed='[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Warrior Aura] char=TesteA bonus=20 -> Damage +24% (total +54%)')
        b = copy.deepcopy(a)
        b.update(dentro_da_aura=False, sequencia=2, feed='hover concluido, sem aura')
        obs, ident = st.gravar([a, b], 'transicao-positiva')
        cs = co.avaliar(obs, ident, cfg)
        temporal = next(c for c in cs if c['id'] == 'S-rv29-transicao-mesmo-personagem')
        self.assertEqual(temporal['estado'], 'OK', temporal)
        self.assertFalse(temporal['prova_runtime'])
        for key, val in [('personagem', 'TesteB'), ('sessao', 'outra'), ('sequencia', 1)]:
            bad = copy.deepcopy(obs)
            bad[1][key] = val
            cs = co.avaliar(bad, ident, cfg)
            t = next(c for c in cs if c['id'] == 'S-rv29-transicao-mesmo-personagem')
            self.assertEqual(t['estado'], 'NAO_EXERCITADO')

    def test_E9_oraculo_ausente(self):
        original = co._fonte_buff
        def ausente(aura, atributo, bonus):
            return (None, None) if aura == 'Dwarven Aura' else original(aura, atributo, bonus)
        with patch.object(co, '_fonte_buff', ausente):
            cs = co.avaliar(of.constroi(), None, casos('S-rv28-dwarven-duas-pessoas'))
        self.assertEqual(len(cs), 3)
        self.assertTrue(all(c['estado'] == 'NAO_EXERCITADO' and c['esperado']['valor'] is None for c in cs))
        self.sem_prova(cs)

    def test_positivo_bytes_completos_nao_e_jogo(self):
        self.assertEqual(co._cadeia(self.obs[0], st.cadeia_kw(self.ident)), (None, None))
        cs = avaliar_corpo(self.obs, self.ident)
        self.assertTrue(all(c['estado'] == 'OK' for c in cs), cs)
        self.assertTrue(all('TESTE DE CONTRATO' in c['motivo'] for c in cs))
        self.sem_prova(cs)


if __name__ == '__main__':
    unittest.main(verbosity=2)
