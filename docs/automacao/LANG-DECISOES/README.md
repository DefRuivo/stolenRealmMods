# Decisões LANG — o que o dono precisa decidir

Cinco gates editoriais da localização pt-BR. Cada documento traz **só o que muda** (as propostas
literais, ID por ID) e separa o que é `MANTER` por padrão. Fonte: cartões `LANG-GATES-DECIDE`
(t_c8af73dc) e `LANG-C4-DECIDE` (t_ea33958b), derivados do pacote `LANG-R1-entrega-final.zip`.

## Quadro geral

| gate | o que é | universo | MUDAM | MANTER | documento |
| --- | --- | --- | --- | --- | --- |
| C1 | traduções ausentes | 1293 IDs | 1242 propostas (1233 centrais + 7 com defeito de concordância + 2 ManualLocalization) | 47 | `LANG-C1-DECISAO.md` |
| C2 | textos pt-BR iguais ao inglês | 268 | 29 | 239 | `LANG-C2-DECISAO.md` |
| C3 | templates e variáveis | 1013 | 37 (33 reordenam habilidade/nível, 2 concordância, 1 sentido, 1 rótulo) | 976 | `LANG-C3-DECISAO.md` |
| C4 | tags e formatação | 83 alertas | 16 | 67 | `LANG-C4-DECISAO.md` |
| C5 | concisão/layout | 376 (lotes A/B2/B3 = 259) | 31 (10 funcionais + 21 narrativos) | 228 | `LANG-C5-DECISAO.md` |

`MANTER` NÃO exige leitura nem aprovação individual — a regra do dono os considera aprovados.
Silêncio = manter.

## Colisões entre gates (precisam de UMA escolha, não duas)

- **LANG-00053** aparece no C3 (concordância "uma torrente") e no C5 (concisão narrativa).
  Aprovado nos dois, o texto fica indefinido: escolher a versão C3 OU a C5.
- **LANG-01184** aparece no C2 (traduzir "Appearance:") e no C3 (tradução de rótulo Appearance).
  Mesma proposta, dois gates: aprovar em um só basta.

## O que NÃO está decidido aqui

- **LANG-C5-B1**: 117 casos do lote B1 continuam **não concluídos** (cartão `LANG-C5-B1`, ainda na fila).
  Eles NÃO estão cobertos por nenhuma aprovação deste recorte.
- Os 7 rascunhos com defeito de concordância documentado (`[his]`) do C1 **não estão prontos para
  aplicação** mesmo se o wording for aceito.
- Nada aqui foi aplicado, instalado, empacotado ou publicado: são propostas.

## O que uma aprovação destrava

`BP-APL-1` (aplicar as correções aprovadas e reconstruir o pacote) exige **ao menos uma** mudança de
texto aprovada. Aprovada qualquer fatia, o `Corrigido` do BetterPortuguese deixa de ser igual ao
`Original` — e aí passa a haver o que avaliar em jogo.

`BP-6` (empacotar para publicação) exige os **cinco** gates resolvidos.
