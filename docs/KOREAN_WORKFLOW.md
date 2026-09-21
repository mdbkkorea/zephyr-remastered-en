# Korean-first local workflow

Read AGENTS.md, STATUS.md, and TEST_LOG.md first.

Install UnityPy 1.25.3 into a project virtual environment for extraction. The full upstream requirements include Windows build dependencies and are unnecessary for this read-only step.

```sh
.venv/bin/python scripts/korean_catalog.py --game '/path/to/original/game'
.venv/bin/python scripts/check_korean_batch.py localization/en-US/korean-batch-001.jsonl
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

Extraction refuses existing output files. Use `--output private/new-catalog.jsonl` only when intentionally extracting another version. It checks file/object hashes before aligning original values with simple string edits. Structural operations are counted separately, not silently interpreted. The extractor never installs a patch.

Each draft contains the original string, Chinese reference, exact Unity resource identity and field path, original patch JSON path, English target, status, and review notes. IDs identify occurrences rather than Chinese text, so similar or identical Chinese translations cannot collapse different Korean source meanings.

Keep extracted full originals in ignored private/. Author subsequent translation batches from verified Korean rows, preserving the source fields. Validate each batch. Names in batch 001 are provisional, including Clausewitz, Bors, Lowen, Tur, Dakama and Antaria; consistency and canon review are still required. Family relationships in alternate lines are intentionally distinct where the Korean differs.

The fourteen particle-bearing system drafts omit Korean grammar markers but remain blocked on renderer verification. The validator reports these as warnings and refuses to mark them reviewed. A future build gate must resolve them before installation.

Do not use the legacy Chinese-deduplicated catalog as the authoritative translation model. Preserve it for comparison and reuse only after reviewing the corresponding Korean occurrences.

Apply the user-approved terms in [GLOSSARY.md](GLOSSARY.md). Check Korean and Chinese together to distinguish deity 주신 from verbal 주신; Korean remains authoritative.

For supporting English character/city/region names, consult relevant Korean Namu Wiki articles when accessible and record the exact source. Follow the approved glossary even when an external reference differs; flag discrepancies.

## Experimental resource rebuild

The `.venv` currently uses UnityPy 1.25.3 and spooky 2.0.0. Audit without writing game resources:

```sh
.venv/bin/python scripts/build_english_stage.py --report private/english-build-audit.json
.venv/bin/python scripts/render_korean_review.py
```

For a deliberately incomplete private serialization test, use `--experimental-incomplete-stage --game '/path/to/original/game' --output private/unique-stage-directory`. Output must not already exist or overlap the source. The tool verifies original hashes and writes only English draft strings, excluding unresolved particle rows. It checks readback and updates catalog CRC/size/cache hashes. It does not copy a full game, install, or launch. A successful stage is not runtime approval. Metadata literal drafts are not yet integrated. Never use the upstream Chinese installer for this English stage.
