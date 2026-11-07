# PyLiteracy
---
## Treetool
A rule-based parser that turns Mandarin Chinese sentences into **X-bar–style syntax trees**
(CP → TP → ModP → … → NP), built on top of the [Articut](https://api.droidtown.co/) word
segmenter / POS tagger. It also models a couple of narrow-syntax operations
(EPP subject movement and verb raising) and prints trees as Unicode box-drawing art that
lines up correctly with CJK characters.

```
    VP[吃]
 ╭───┴────╮
他   ClsP[五碗]
      ╭──┴───╮
     ""   NP[飯]
           ╭─┴──╮
          ""   ""
```

> Status: work in progress / research prototype. See [Known issues](#known-issues--todo).

---

## How it works

1. **Tagging.** A sentence is sent to Articut, which returns a POS-tagged string such as
   `<ENTITY_pronoun>他</ENTITY_pronoun><MODAL>可以</MODAL><ACTION_verb>吃</ACTION_verb>…`
   (see `sample.json` for a full Articut `lv2` response).
2. **Head finding.** For each projection, a regex in `HeadPatterns` locates the head in the
   tagged string. `split_pos()` cuts the string into `(left, head, comp)`; the `comp` part is
   handed down to the next projection.
3. **Projection chain.** The parser walks down a fixed spine:

   ```
   CP → TP → ModP → AuxP → NegP → AspP → LightVP → VP | DegP | PP → ClsP → NP
                                                          └→ De_CompP (得-complements)
   ```

   | Projection | Head pattern matches (examples) |
   |---|---|
   | `CP` | sentence-final 了, `CLAUSE_particle` / `CLAUSE_YesNoQ` (嗎) |
   | `TP` | always a null head `∅` |
   | `ModP` | `MODAL` (可以), 可能, 要 + verb |
   | `AuxP` | `AUX` 就 / 卻 / 是, A-not-A questions |
   | `NegP` | `FUNC_negation` (不, 沒有) |
   | `AspP` | `ASPECT` 過 / 了 / 完 / 著, 在 / 已經 before a verb |
   | `LightVP` | `ACTION_lightVerb` (e.g. 被); otherwise `∅` |
   | `VP` / `DegP` / `PP` | verbs; degree heads 很 / 太 (adjectival predicates); 從 / 在 |
   | `ClsP` | `ENTITY_classifier` (五碗) |
   | `NP` | nouns, pronouns, locations; 的-relative clauses become `left` |
   | `De_CompP` | 得 |

   Adverbials (…地, time expressions) in the `left` position are split out by `split_left()`.
   An empty head `""` means "this projection is absent"; `∅` means "present but phonologically null".
4. **Tree building.** `parse_S()` returns either a dict of all projections or, with
   `genTree=True`, a single tree in which absent projections are pruned (`gen_realTree()`).
5. **Movement (optional).** `ex_EPP_movement()` raises the subject to `TP.left` and leaves
   `Subj_trace`s (or inserts *pro* when there is no overt subject). `ex_verb_raising()` raises
   the verb from `VP` head to `AspP` head, leaving a `V_trace`.

---

## Repository layout

| File | Purpose |
|---|---|
| `linguistic_parse.py` | **Current parser.** Head patterns, `parse_*` functions, `parse_S`, movement operations, and a set of built-in `test_sentences` (pre-tagged, so no API call is needed). |
| `type.py` | The `Tree` datatype and its subclasses (`VP`, `ClsP`, `NP`, …). Tracks `parent` links, strips POS tags for display, and offers two printers: `pstr()` / `pprint()` (indented `├──` style) and `treeart_str()` (box-drawing tree). Includes the example tree `ex1`. |
| `treeart.py` | Vendored copy of the [`treeart`](https://pypi.org/project/treeart/) package, patched with display-width helpers (`dwidth`, `dljust`, …) so full-width CJK characters align. |
| `main.py` | Scratch entry point; currently prints `type.ex1` with `treeart_str()`. Commented code shows how to call Articut and save a response. |
| `formalize_approach.py` | Earlier, self-contained version of the parser (its own `@dataclass Tree`, calls Articut directly, reads `./data/test_data.json`). Kept for reference. |
| `sample.json` | Example Articut `lv2` output for 「戴克斯的原始版本僅適用於找到兩個頂點之間的最短路徑」. |

---

## Requirements

- **Python 3.11+** (`type.py` uses `typing.assert_never`)
- [`ArticutAPI`](https://github.com/Droidtown/ArticutAPI)

```bash
pip install ArticutAPI
```

### Articut credentials

Live parsing needs a Droidtown account. The scripts expect one of:

- `account.info` (used by `formalize_approach.py`):
  ```json
  { "username": "you@example.com", "apikey": "YOUR_KEY" }
  ```
- `DROIDTOWN.json` (commented out in `main.py`):
  ```json
  { "username": "you@example.com", "key": "YOUR_KEY" }
  ```

Add both to `.gitignore` so keys are never committed.

---

## Usage

**Parse the built-in examples** (no API key needed — the inputs are already tagged):

```bash
python linguistic_parse.py
```

This parses 「他可以吃五碗飯」 and prints its full projection chain with `treeart_str()`.

**Print the example tree:**

```bash
python main.py
```

**From your own code:**

```python
from ArticutAPI import Articut
from linguistic_parse import parse_S, ex_EPP_movement, ex_verb_raising

articut = Articut(username, apikey)
tagged = articut.parse("他吃了五包他喜歡的零食", level="lv1")["result_pos"][0]

tree_dict = parse_S(tagged, genTree=False, showTree=True)   # dict of every projection
tree      = parse_S(tagged, genTree=True,  showTree=True)   # pruned single tree

ex_EPP_movement(tree_dict, genTree=True, showTree=True)
ex_verb_raising(tree_dict, genTree=True, showTree=True)
```

**Build and print a tree by hand:**

```python
from type import VP, ClsP, NP

t = VP(head="吃", left="他",
       comp=ClsP(head="五碗", left="",
                 comp=NP(head="飯", left="", comp="")))
print(t.treeart_str())   # box-drawing tree
t.pprint()               # indented ├── / └── tree
```

`Tree` accepts either `Tree(left, head, comp)` positionally (head-initial only) or keyword
arguments `Tree(left=…, head=…, comp=…, head_type=…)` — the two forms cannot be mixed.

### Example sentences covered

| Sentence | What it exercises |
|---|---|
| 我覺得說他可以被吃五碗他喜歡的飯 | every projection at once |
| 他可以吃五碗飯 | ModP, no C |
| 他吃五碗飯 | no modal |
| 她參加比賽 | no classifier |
| 他很高 | DegP (adjectival predicate) |
| 他跑得很快 | 得-complement |
| 他吃了他喜歡的零食 | relative clause |
| 他吃了五包他喜歡的零食 | relative clause + classifier |
| 他白飯 | ungrammatical (no predicate) |
| 樹上沒有葉子 | NegP |

---

## Known issues / TODO

- `parent` links are not always set correctly (TODO in `linguistic_parse.py`).
- In `parse_S`, every projection is chained into the next one's `comp`, so `De_CompP` ends up
  under `NP` and still holds raw tagged text, and absent projections show up as `[""]` nodes
  in `treeart_str()` output. `gen_realTree()` prunes these, but the two paths do not yet agree.
- Sentence-final 了 is placed in the CP head as a stop-gap; it belongs in a right-headed CP.
- 在…裡面 style prepositional phrases are not handled.
- Only head-initial structures are modelled (CP is treated as head-final via the C pattern).
- `main.py` does `import type`, which shadows Python's built-in `type()` in that file;
  renaming the module (e.g. `syntax_tree.py`) would avoid surprises.
- Planned: tree-printing variants sketched in the docstring of `type.py`
  (left/right layouts, labelled `head:` / `comp:` edges, drawn movement arrows).

---

## Credits

- POS tagging by [Articut](https://api.droidtown.co/) (Droidtown Linguistic Tech).
- Tree rendering adapted from [`treeart`](https://pypi.org/project/treeart/).
- Directory-tree printing algorithm in `type.py` adapted from
  [this Stack Overflow answer](https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python).
- AspP background reading: <https://www.persee.fr/doc/clao_0153-3320_1995_num_24_1_1466>
