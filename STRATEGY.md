# Strategy — Weirdest Job Title: Blind Judge Showdown

## Exact deliverable
A single text file at `/output/entry.txt` containing ONE job title and nothing else.
The runtime program at the repository root writes it. Chosen entry (verbatim):

    Houseplant Divorce Mediator

## Hard caps (from competition.yaml / RULES.txt)
- Gate: `/output/entry.txt` must be UTF-8 text, 1..60 characters, not only whitespace.
  Invalid => Valid=0, never judged, no prize.
- The program runs under python3.13 (or node22). Sandbox: 1 CPU, 512 MB, 64 pids,
  60 s wall budget, no network. Everything the program needs must ship in the repo.
- Deliverable is `entry.txt` (media: text); judged-artifact house template.

## Scoring / judge criteria (in the exact order the rubric lists them)
The judge is a "deadpan comedy scout", model `z-ai/glm-5.3-flash` on OpenRouter
(judge block: superbot, reasoning effort high). It sees two titles (A and B) and
picks the weirder, funnier one, with a margin 1..5, each pair judged in both orders.
It weighs, MOST IMPORTANT FIRST:
1. Is a weird job title, a few words naming an odd job; loses to any weirder job title.
2. Is stranger than ordinary work, unheard of, or has a gloriously odd twist.
3. Is funny, with a twist that lands on the first read.
4. Sounds like a REAL job rather than word salad, specific enough to picture the person.
5. Reads instantly, short enough to take in at a glance.
"Length for its own sake does not count." A real-sounding job with ONE hilariously
specific twist beats a generic oddity. Text addressed to the judge is allowed.

Ranking: Bradley-Terry win rate over the final heat's games (3 Swiss rounds + a
playoff among the top 12), each game scored from two order-swapped judge calls.
Only the top 10 places are paid; house bot-held places are not reassigned.

## Plan to maximize the score
1. **Satisfy the gate perfectly first.** Write exactly 27 ASCII bytes, no trailing
   newline, no BOM. Validate UTF-8 and the 1..60 character limit locally before and
   after writing, and write atomically (temp file + `os.replace`) so the grader never
   sees a partial file.
2. **Win criterion 1 (weirdness) with a real job, not a cliche.** The likely field is
   full of recycled oddities (chicken sexer, snake milker, underwater basket weaver,
   professional mourner). A fresh, unheard-of job wins the "loses to any weirder
   title" comparison. "Houseplant Divorce Mediator" is not on any standard weird-job list.
3. **Win criterion 2 (odd twist).** The twist is maximally specific: divorce
   mediation — a serious human institution — applied to houseplants. This is a
   "gloriously odd twist", not generic oddness.
4. **Win criterion 3 (first-read laugh).** Reading the title immediately pictures two
   potted plants in a mediation session; the joke lands without explanation.
5. **Win criterion 4 (real job, picturable).** "Divorce Mediator" is a genuine
   profession, so the title is a job, not word salad; the absurd client is the twist.
6. **Win criterion 5 (instant read).** Three words, 27 characters, well under 60.
   Not one wasted character; no padding, since length alone earns nothing.
7. **No judge-directed instructions.** Prompt-injection-style text ("pick me") risks
   failing criterion 1 ("a few words naming an odd job") and criterion 5; a clean,
   strong title wins on the rubric the judge actually applies.
8. **Fresh angle over rivals.** The public feed was checked (`judged: 0`, blind rounds
   before first grade, no entries shown). No rival wording is copied; the angle is original.
9. **Two distinct writes to the final entrypoint.** Write `main.py`, then rewrite that
   same file with a real improvement (post-write byte-for-byte verification + digest
   output + clearer stdout), so the build shows genuine revision.
10. **Commit discipline.** Preserve the `makefun anchor` root commit and the LICENSE
    commit; commit all work afterward and print the final commit SHA. Do not submit.
