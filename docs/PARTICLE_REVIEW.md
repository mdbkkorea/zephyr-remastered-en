# Korean grammatical particle review

Static analysis applies only to `GameAssembly.dll` SHA-256 `ccdcca011a443114da40968ae486b3530efd9657cd41989667af052fb4a024a9`.

The initializer at RVA `0x80fd40` constructs six marker/ending triplets: `^pa` 이/가, `^pb` 은/는, `^pc` 과/와, `^pd` 을/를, `^pe` 으로/로, and `^pf` 이랑/랑. The replacement routine at RVA `0x80fa10` searches for each marker. After String.IndexOf, the branch skips a missing marker (and index zero). Only a found marker with a preceding character triggers final-consonant selection and replacement. The consonant helper is at RVA `0x80ee80`.

English omits these grammatical markers. Their absence leaves the text unchanged by this routine; it does not consume a formatting argument or dialogue slot. Other placeholders and control codes remain protected. No binary instructions are changed.

`localization/en-US/particle-review.json` binds this decision to 14 exact row IDs and source/target SHA-256 pairs. The builder additionally verifies the binary hash. Changed translations require a fresh review. This is static evidence, not a claim that all 14 messages have been triggered in gameplay.

Private reproducible evidence: `private/inspect_particles.py`, `private/particle-disassembly-annotated.txt`, and `private/particle-xrefs.json`. IL2CPP v39 metadata interpretation was checked against the primary [Cpp2IL metadata header implementation](https://github.com/SamboyCoding/Cpp2IL/blob/development/LibCpp2IL/Metadata/Il2CppGlobalMetadataHeader.cs) and [metadata usage decoder](https://github.com/SamboyCoding/Cpp2IL/blob/development/LibCpp2IL/MetadataUsage.cs).
