# A-Maze-ing — Planning & suivi

Rendu : **2026-10-14** (déplacé, était le 2026-10-07) · Spec : `docs/superpowers/specs/2026-09-30-a-maze-ing-design.md`
Légende : `[ ]` à faire · `[~]` en cours · `[x]` fini (flake8 + mypy verts, testé)

Règle de fermeture (avant de cocher `[x]`) : sortie `make lint` collée,
cas limites testés, README mis à jour dans le même commit, choix de design
expliqué en une phrase.

## J1 — 2026-10-01 · Socle + config
- [x] Déplacer les anciens fichiers hors du repo (`config.py`, `maze(1).py`, `pattern.py`, `test_pattern.py`, `mazegen/maze.py`, `mazegen/pattern.py`)
- [x] `.gitignore` (dépend de : rien)
- [x] `Makefile` : install, run, debug, clean, lint, lint-strict, build
- [~] `pyproject.toml` (setuptools, package `mazegen`, version 1.0.0) — build vérifiable seulement au J2, quand `mazegen/` existe
- [x] `LICENSE.md` (MIT)
- [x] `config.txt` par défaut, commenté (WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT, SEED, SHOW_PATH)
- [x] `config_parser.py` : `MazeConfig` (dataclass), `ConfigError`, `REQUIRED_KEYS`, `OPTIONAL_KEYS`, `load_config()`, `parse_int`, `parse_bool`, `parse_coords`
- [x] README : squelette (1re ligne italique, Description, Instructions, Resources, format du config)
- Concepts : dataclass, exceptions perso, `with open()`, EAFP (`int()` dans un `try`)

## J2 — 2026-10-08 · Générateur parfait
- [x] `mazegen/generator.py` : constantes `DIRECTIONS`, `OPPOSITE`
- [x] `MazeGenerator.__init__` + `_reset_walls()` (dépend de : spec §6)
- [x] `_open_wall(x, y, direction)` : seul endroit qui modifie les murs
- [x] `_carve_dfs()` : DFS itératif, pile `list`, `random.Random(seed)`
- [x] `mazegen/__init__.py`
- Concepts : pile (DFS itératif), `random.Random` vs seed globale, `walls[y][x]`

## J3 — 2026-10-10 · 42 + solve + sortie
- [x] `PATTERN_42` + `_place_pattern()` (centre dans la colonne vide)
- [x] Validation entrée/sortie → `ValueError` (dépend de : `_place_pattern`). Tester ENTRY=-1,0 : en Python `walls[0][-1]` ne plante pas, il lit la dernière colonne
- [x] `solve(start, end)` : BFS avec `collections.deque`
- [x] `output_writer.py` : `to_hex_rows()`, `write_output()`
- [x] `a_maze_ing.py` : relie config → générateur → sortie, gestion d'erreurs
- [x] Vérif : `python3 maze_analyzer.py maze.txt` → `PERFECT maze`, cohérence OK
- Concepts : BFS / file, dict `parent`, format hexa sans bit à bit

## J4 — 2026-10-11 · Mode Pac-Man (PERFECT=False) — jour à risque
- [x] `_is_dead_end(x, y)`
- [x] `_creates_open_3x3(x, y)` + `_is_open_3x3`, `_close_wall`
- [x] `_remove_dead_ends()` (dépend de : `_open_wall`, `_creates_open_3x3`)
- [x] Vérif : analyzer → `Pac-Man-USABLE`, idéalement 0 cul-de-sac réel
- Concepts : boucles (graphe non-arbre), fenêtre glissante 3x3

## J5 — 2026-10-12 · Affichage
- [x] `display.py` : `build_char_grid()`, `render()`, couleurs ANSI
- [x] `run_menu()` : régénérer, chemin on/off, couleur murs, couleur 42, quitter
- [x] `EOFError` / `KeyboardInterrupt` → sortie propre
- Concepts : codes ANSI, grille (2h+1)x(2w+1)

## J6 — 2026-10-13 · Package + doc
- [x] `make build` → `mazegen-1.0.0-py3-none-any.whl` à la racine
- [x] Test : venv neuf, `pip install` du .whl, import OK
- [x] README complet (algo, pourquoi, réutilisation, gestion de projet, usage de l'IA)
- [x] `make lint-strict`

## J7 — 2026-10-14 · Rendu + soutenance (plus de jour de marge)
- [ ] Répétition : expliquer chaque fichier à voix haute
- [ ] Modifs type review : ajouter une clé config, changer une couleur

## Journal
| Date | Fait | Écart vs plan |
|---|---|---|
| 2026-09-30 | Cadrage, choix, spec (`7140004`) | — |
| 2026-09-30 | J1 commencé en avance : anciens fichiers sortis (`af00580`), `.gitignore` + `LICENSE.md` (`c72cd1f`), `Makefile` + `.flake8` + `pyproject.toml` (`9e85205`, `make lint` OK), `config.txt` écrit | +1 jour d'avance. Ajout imprévu : `.flake8` (flake8 analysait `.venv/`). À surveiller : commits pas lancés après `git add` (3 fois) |
| 2026-10-07 | `config_parser.py` fini : `make lint` vert, `tests/check_config.py` 25 cas OK (ajout `MAX_SIZE`, `check_inside`, tests `OUTPUT_FILE`) | Deadline déplacée au 2026-10-14, J2–J7 recalés du 08 au 13. README : squelette fait |
| 2026-10-10 | J2 : `mazegen/generator.py` + `__init__.py` (code donné par Claude à ma demande), `make lint` et `lint-strict` verts, `tests/check_generator.py` OK (cohérence, bordures, connexe, parfait, seed) sur 2x2, 20x15, 100x100, 2x100. `_carve_dfs` tracé à la main sur un 2x2 | Retard de 2 jours sur J2 : J3–J6 décalés d'un jour, le jour de marge est consommé. À surveiller : code reçu tout fait, à savoir défendre ligne par ligne. Fermé le jour même : 4 réponses de défense OK, `make lint` + `tests.check_generator` lancés par moi |
| 2026-10-10 | J3 : `PATTERN_42`, `_check_entry_exit`, `solve` (BFS), `output_writer.py`, `a_maze_ing.py` (code donné par Claude). Analyzer : `PERFECT maze`, cohérence OK, coins + centre OK. Erreurs testées : pas d'argument, fichier absent, maze < 9x7, entrée sur le 42, sortie non écrivable | J3 fait le jour prévu. `PERFECT=False` donne encore un maze parfait : c'est J4 |
| 2026-10-14 | J3 fermé (4 réponses OK, lint + tests verts). J4 : `_remove_dead_ends` + vérif 3x3 (code donné par Claude, sprint). Analyzer sur 240 mazes (8 tailles x 15 seeds x 2 modes) : toujours le bon verdict, 0 zone 3x3 ouverte, `config.txt` → Pac-Man-USABLE avec 0 cul-de-sac réel (bonus) | Jour du rendu : sprint J4–J6 en mode code direct |
| 2026-10-14 | J5 : `display.py` (grille, couleurs ANSI, menu 1–5, Ctrl-D/Ctrl-C), testé en envoyant des choix au menu. J6 : `.whl` construit, installé dans un venv neuf, import OK ; README complet (affichage, sortie, algo, réutilisation, gestion de projet, ressources, usage de l'IA) ; `make lint-strict` vert | Code donné par Claude (sprint). Reste J7 : répétition |
