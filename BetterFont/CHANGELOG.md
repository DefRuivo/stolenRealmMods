# Changelog — BetterFont

## 1.0.0

Primeira versão publicada.

- **Troca a fonte renderizada do jogo por uma serifada** — Times New Roman, com fallback para Georgia / Liberation Serif — aplicada a **todos os textos TMP**, inclusive telas que abrem depois (level up, tooltips, menus).
- A **fonte original do jogo entra como fallback** do asset serifado, então ícones e símbolos que a Times não tem continuam renderizando (sem quadradinhos).
- A aplicação é **preguiçosa e com throttle**: o updater é criado na primeira UI viva (gatilho em `OptionsManager.Localize`), porque um GameObject criado no `Awake` do plugin é destruído pelo jogo na primeira carga de cena. A varredura roda com tempo real, então funciona mesmo com `timeScale = 0` (menus).
- **Sem qualquer alteração de gameplay.**
