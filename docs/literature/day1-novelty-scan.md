# Day 1 novelty scan: masked-paragraph context and verifier audit

**Study audited:** *Where Does Masked-Paragraph Reconstruction Signal Come From? A Context and Verifier Audit in Scientific Papers*
**Search date:** 2026-07-29
**Scope:** targeted adversarial scan, not a systematic review

## 1. Executive verdict

No checked paper performs essentially the complete proposed experiment. The nearest work divides into four already-developed lines:

1. open sentence or span infilling from surrounding text;
2. relevant/absent/irrelevant/noisy context perturbations in scientific QA;
3. atomic scientific claims linked to supporting evidence;
4. factuality evaluators tested with synthetic or deliberately modified errors.

The contribution is therefore an **integration**, not a new primitive. Its defensible distinction is narrower: open scientific paragraph reconstruction under source-controlled context, scored only on externally recoverable atomic claims, with task-specific error-detection calibration.

The current causal wording is wrong. The four arms do not *isolate* support-bearing evidence: true adjacent context also differs in discourse position, continuity, local style, lexical reuse, section structure, and potentially memorized paper identity. They estimate differences among context regimes. An evidence-ablated adjacent-context control is needed for a cleaner evidence-specific contrast.

The judge-validation component is also not novel in itself. Stenzl et al. directly tested a five-LLM panel on original and deliberately modified facts from clinical-oncology summaries, while FactCC established large-scale rule-based corruption with source and error spans. Moreover, ReFACT and long-document metric stress tests give direct reasons not to assume that controlled-corruption performance transfers to natural scientific errors.

**Decisive evidence:** Wyatt et al. is a direct reconstruction precedent; Wen et al. and SciCUEval are close context-control precedents; CLAIM-BENCH, Evidence Inference, SciFact, FActScore, and ResearchQA cover claim/evidence machinery; Stenzl et al. and FactCC cover planted-error validation. No checked source combines those elements in the proposed open-generation experiment.

## 2. Search scope and queries

### Process

- Ran the canonical Novelty Gauntlet in `C:\CS\sideProjects\portfolio`.
- Planned 61 OpenAlex/Crossref queries; 40 requests completed, yielding 76 candidate records.
- Manually checked 17 load-bearing primary papers or official records across ACL Anthology, PubMed/PMC, arXiv, PMLR/ICLR, Nature Scientific Data, and Google Research.
- Ran exact-phrase and conceptual follow-ups for masked paragraphs, scientific reconstruction, context provenance, claim-to-evidence linkage, synthetic corruptions, biomedical evidence inference, and reasoning-trace verification.
- Convened a blind Codex/Claude council. Both families completed initial memos and cross-examination; Claude completed the second revision. Codex’s final revision failed the council schema, so no blind-judge output was accepted. The chair therefore used only valid council material and independently rechecked the load-bearing sources.

### Representative queries

- `"masked sentence prediction" document context`
- `"masked paragraph" reconstruction language model scientific paper`
- `"masked paragraphs" scientific paper reconstruction`
- scientific text infilling whole sentence scientific abstracts
- scientific QA gold context absent random irrelevant noisy context
- semantically similar unrelated context injection scientific LLM
- same-document irrelevant context versus cross-document matched context
- scientific claim evidence spans full paper atomic claims
- biomedical evidence inference intervention comparator outcome evidence span
- LLM judge scientific summary planted factual errors
- synthetic corruption entity number unit negation comparator factual consistency
- scientific confabulation positional error annotations
- long-document factuality metric perturbation scientific
- scientific reasoning-chain evidence attribution logical correctness

### Coverage limitations

- This was not dual-screened or preregistered.
- English-language, indexed work was favored; theses, patents, non-English work, private evaluations, and obscure workshops remain possible gaps.
- Several closest records are 2025–2026 preprints or newly published papers.
- A failed search for duplication is not proof of novelty.
- Changing the corpus, subdomain, or Gemma model size is not counted as methodological novelty.

## 3. Closest precedents

**Legend:** AE = atomic claims plus external evidence spans; PE = LLM judge validated with planted errors.

| Precedent and class | Task/domain | Masked or generated unit; evidence supplied | Comparisons / evaluation | Relevant context separated from generic text? | AE / PE | Exact overlap | Exact remaining difference |
|---|---|---|---|---|---|---|---|
| [Wyatt, Joshi & Salim, 2025](https://aclanthology.org/2025.ijcnlp-short.24/) — **partial precedent; closest reconstruction study** | Zero-shot masked-sentence prediction in stories, recipes, and Wikipedia | One sentence, with multi-sentence masking analyses; full masked document provides preceding/following text | Mask position and density; BLEURT, SBERT, ROUGE, BLEU, and one-author blind cohesion preference | **No.** It varies position/density, not evidence provenance | No / No | Open reconstruction from surrounding document context | Not scientific; no prior-only/matched-cross-paper/nonadjacent-same-paper arms; no claim/evidence scoring or corruption-tested judge |
| [Donahue, Lee & Liang, 2020](https://aclanthology.org/2020.acl-main.225/) and [Huang et al., 2020](https://aclanthology.org/2020.acl-main.226/) — **adjacent methodological precedents** | Variable-length text/sentence infilling; ILM includes scientific abstracts, INSET uses long-form general text | Missing spans or intermediate sentences; surrounding text, sometimes keywords | Likelihood/generation metrics and human judgments; model/architecture comparisons | No | No / No | Establish that sentences and chunks can be generated from bilateral context | Training/generation papers, not factual context-source audits |
| [Wen, Howe & Wang, 2024](https://aclanthology.org/2024.findings-emnlp.197/) — **partial precedent; closest context-ablation study** | Context-dependent science QA and abstention across four datasets | Answer to a question; gold scientific context | Removes gold context, replaces it with irrelevant context, or adds extra context; accuracy and abstention | **Yes, broadly:** gold versus absent/irrelevant/additional | No / No | Directly asks whether scientific task behavior comes from correct rather than insufficient/incorrect context | QA/abstention, not open reconstruction; no crossed same-paper versus topic-matched cross-paper controls |
| [Yu et al., 2026 (SciCUEval)](https://www.nature.com/articles/s41597-026-06594-9) — **partial precedent** | Scientific-context understanding across text, tables, and knowledge graphs | QA, MCQ, T/F, and cloze/content-completion answers; relevant scientific entries plus distractors | Accuracy/rejection; direct versus context-assisted answering; 18 models | **Yes.** Injects embedding-selected, semantically similar but unrelated entries, with low lexical overlap | No / No; GPT-4o quality screen plus human experts is not planted-error validation | Scientific relevant-information identification, absence detection, noisy context, completion, and context-aware inference | Deterministic answer tasks, not free paragraph generation or reconstruction-specific claim/evidence auditing |
| [Javaji et al., 2025 (CLAIM-BENCH)](https://arxiv.org/abs/2506.08235) — **partial precedent** | Scientific claim-to-evidence extraction and validation in full AI/ML papers | Sentence/paragraph claims and one-to-many evidence spans from the paper | Single-pass, staged claim→evidence→conclusion, and claim-by-claim strategies; precision/recall and annotation agreement | No context-source ablation | **Yes / No** | Claim-level scientific evaluation with dispersed paper evidence | No masking or generation; no relevant-versus-generic context experiment |
| [Imran & Solanky, 2026 (ResearchQA)](https://arxiv.org/abs/2607.11074) — **partial precedent** | Citation-grounded single-paper scientific QA; 6,211 pairs from 494 OA papers | Answers plus supporting passages/citations | Lookup, comprehension, multi-hop, adversarial; deterministic citation matcher and LLM rubric | Adversarial questions and grounded refusal, but not the proposed four sources | Evidence passages, not predeclared atomic generated claims / No | Paper-grounded scientific evaluation with traceable citations and an LLM evaluator | QA rather than masked reconstruction; evaluator scores were compressed; no planted-error validation |
| [Lehman et al., 2019](https://aclanthology.org/N19-1371/) and [DeYoung et al., 2020](https://aclanthology.org/2020.bionlp-1.13/) — **adjacent methodological precedents** | Evidence Inference from full-text randomized-trial reports | Intervention–comparator–outcome prompt; increase/decrease/no-significant-difference label and supporting evidence | Classification and evidence identification; stronger models and annotation expansion in v2 | Not a generic-context ablation | **Structured claim/evidence / No** | Biomedical full-text direction-of-effect inference with explicit evidence | RCTs rather than observational epidemiology; structured classification, not paragraph reconstruction |
| [Wadden et al., 2020 (SciFact)](https://aclanthology.org/2020.emnlp-main.609/) and [Min et al., 2023 (FActScore)](https://aclanthology.org/2023.emnlp-main.741/) — **adjacent methodological precedents** | Scientific claim verification; atomic factual precision in long-form generation | Claims or decomposed atomic facts; retrieved abstract/knowledge evidence | Support/refute/insufficient evidence, rationale retrieval, or atomic precision | Evidence retrieval is central, but not a reconstruction context arm | **Yes / No** | Establishes atomic decomposition plus evidence-backed factual scoring | Different generation/task settings; no within-paper context-source manipulation |
| [Stenzl et al., 2026](https://pubmed.ncbi.nlm.nih.gov/42318048/) — **partial precedent; closest judge-validation study** | Faithfulness of scientific and plain-language clinical-oncology summaries | Facts extracted from summaries; source titles/abstracts | Five-LLM panel versus three humans; original and subtle, moderate, contradictory modifications; agreement and severity response | No context-source experiment | Facts, not the proposed external-span annotation / **Yes** | Direct biomedical validation of LLM factual judgment using deliberately modified facts | Summary verification, not reconstruction; severity bins rather than the frozen direction/numeric/unit/entity/comparator/exposure/condition taxonomy |
| [Kryscinski et al., 2020 (FactCC)](https://aclanthology.org/2020.emnlp-main.750/) and [Pagnoni et al., 2021 (FRANK)](https://aclanthology.org/2021.naacl-main.383/) — **adjacent methodological precedents** | Factual consistency of news summaries | Summary sentence, source support span, and inconsistent span | Over one million rule-transformed training examples in FactCC; human error taxonomy and metric benchmarking in FRANK | Source-document grounding, not context provenance | Error/support spans / Synthetic errors, but not validation of a general LLM judge | Entity, number, negation, predicate, circumstance, and related error taxonomies | Non-scientific summaries; FactCC trains a classifier; neither audits the proposed scientific judge in the reconstruction task |
| [Wang et al., 2026 (ReFACT)](https://aclanthology.org/2026.eacl-long.381/) and [Mujahid, Wright & Augenstein, 2026](https://aclanthology.org/2026.acl-long.1472/) — **adjacent negative evidence** | Scientific confabulation detection; long-document factuality-metric robustness | AskScience answer error spans; long summaries with truth-preserving perturbations | ReFACT: independent versus comparative detection, span F1, distractor failures. Stress test: six metrics, seven perturbations, three domains | Evaluates sensitivity to distractors, retrieval context, and claim density | Span annotations / No planted false-fact suite in these studies | Directly weakens assumptions about reliable automatic scientific error detection | Does not reconstruct masked prose; provides a warning and validation target, not duplication |
| [Xiao et al., 2026](https://arxiv.org/abs/2602.08237) and [Guo, Huang & Fang, 2026](https://arxiv.org/abs/2604.21277) — **superficially similar** | Long-context RLVR document reconstruction; multimodal masked-text reconstruction | Multiple paragraphs selected/ordered from shuffled originals; or visual sentence/paragraph recovery | Verifiable candidate ordering and downstream RL evaluation; level-aware multimodal reconstruction | No evidence-source audit | No / No | Paragraph masking and reconstruction terminology | First is discriminative ordering for RLVR, not open prose; second tests visual/layout grounding, not scientific evidence attribution |
| [Jacovi et al., 2024 (REVEAL)](https://aclanthology.org/2024.acl-long.254/) — **adjacent methodological precedent** | Verification of open-domain reasoning chains | Individual chain-of-thought steps and evidence passages | Step-level relevance, attribution, logical correctness; verifier contradiction tests | Evidence attribution is explicit | Step/evidence labels / No proposed planted-fact taxonomy | Shows how reasoning traces can be evaluated granularly | The proposed target is published prose reconstruction, not a reasoning trace; it should not be framed as recovery of author reasoning |

### Classification of the literature

- **Direct duplication:** none found.
- **Partial precedents:** Wyatt; Wen; SciCUEval; CLAIM-BENCH; ResearchQA; Stenzl.
- **Adjacent methodological precedents:** ILM/INSET; Evidence Inference; SciFact/FActScore; FactCC/FRANK; ReFACT; long-document factuality stress testing; REVEAL.
- **Superficially similar but materially different:** paragraph-order RLVR and multimodal masked-text reconstruction.

## 4. Synthesis and council answers

### 1. Has essentially this experiment already been performed?

**No, based on the checked record.** No source jointly uses:

- free-form masked scientific paragraph reconstruction;
- prior-only, adjacent, topic-matched cross-paper, and nonadjacent same-paper conditions;
- preannotated atomic claims recoverable from evidence outside the mask; and
- a judge calibrated on a typed suite of planted scientific errors.

This is a negative search result, not proof of firstness.

### 2. Which component is least novel?

**Masked reconstruction/infilling.** Whole-sentence and multi-sentence infilling is established, including scientific abstracts. Context perturbation and planted-error factuality evaluation are also established. The precise seven-type corruption list is a domain adaptation of existing corruption taxonomies, not a new evaluation principle.

### 3. Which component is most defensibly distinct?

**The source-crossed context comparison inside open scientific reconstruction, with scoring restricted to externally recoverable atomic claims.** The distinction is the experimental conjunction of:

- open generation rather than QA/selection;
- same-paper and cross-paper negative controls;
- claim-specific answerability defined before generation.

That is protocol-level distinctiveness, not a new task family.

### 4. Does the combination form a meaningful contribution?

**Conditionally.** It can be a meaningful pilot if it measures evidence-attributable claim recovery rather than aggregate similarity and if judge performance is reported by error type. As frozen, however, the four arms do not identify a clean causal effect of evidence relevance. Without a stronger control, the study is a well-instrumented comparison of context regimes.

### 5. Best framing

1. **Primary:** document-grounding / evidence-grounded factual reconstruction.
2. **Secondary:** evaluator validation for scientific claims.
3. **Avoid as primary framing:** scientific reasoning.

“Scientific reasoning” is too broad: success can arise from copying, discourse completion, domain priors, or memorization. “Factual reconstruction” is accurate but underspecifies the central provenance question.

### 6. Defensible novelty claims

- No prior study identified in this targeted scan combines open scientific paragraph reconstruction with the specified source-crossed context controls, externally linked recoverable claims, and corruption-tested factual judging.
- The study adapts established infilling, context-perturbation, claim/evidence, and evaluator-stress-testing methods into one document-grounding audit for small models.
- The study can estimate how claim recovery changes across relevant, topically matched, same-document irrelevant, and no-document-evidence regimes.
- The fixed epidemiology claim taxonomy and per-corruption judge report can provide a domain-specific diagnostic resource.

### 7. Claims to avoid

- “First masked-paragraph,” “first scientific infilling,” or “first scientific-context ablation” study.
- “First use of atomic claims,” “first scientific evidence spans,” or “first planted-error LLM-judge validation.”
- “The four arms isolate the causal contribution of relevant evidence.”
- “Prior-only equals generic domain knowledge.” It may include memorized paper text or secondary descriptions.
- “True adjacent performance demonstrates reasoning.” It may reflect copying or discourse prediction.
- “A validated judge is reliable on natural errors.” Controlled-error sensitivity does not establish transfer to omissions, interacting errors, hedging failures, or misplaced error spans.
- “The model reconstructs the author’s reasoning” or “the original paragraph is the uniquely correct answer.”
- Any RLVR claim.
- Generalization beyond the selected models, corpus, and claim distribution.
- “No prior work exists.” Use “none was identified in this targeted search.”

### 8. One small design change

Add a **fifth, evidence-ablated adjacent-context condition** for a preregistered subset.

Start from the true adjacent context and remove or neutralize only the annotated support-bearing spans, preserving document identity, adjacency, section, length, style, and as much lexical context as possible. Compare true adjacent versus evidence-ablated adjacent on externally recoverable claim accuracy.

This is stronger than adding another random-text control because it intervenes on the proposed mechanism while holding the main nuisance variables fixed. Report manipulation checks: retained token count, section, entity overlap, lexical similarity, and whether blinded annotators agree that the ablated text no longer supports the target claims.

## 5. Defensible novelty statement

> We evaluate evidence-grounded factual reconstruction in observational epidemiology by asking small instruction-tuned language models to regenerate masked paragraphs under four controlled context-provenance conditions. Unlike prior sentence-infilling, scientific QA context-perturbation, claim-verification, and factuality-evaluator studies considered separately, the pilot scores preannotated claims that are recoverable from evidence outside the mask and calibrates its automated judge against typed scientific corruptions. We found no prior study in the searched literature that combines these elements. The experiment estimates differences among context regimes; an evidence-ablated adjacent control is required for a stronger claim that the difference is specifically caused by support-bearing evidence.

## 6. Prohibited or unsupported novelty claims

Do not use:

- “We introduce scientific paragraph reconstruction.”
- “We are the first to distinguish relevant from irrelevant scientific context.”
- “We introduce atomic scientific claim evaluation.”
- “We introduce planted-error validation of LLM judges.”
- “Our controls isolate document evidence from model knowledge.”
- “Reconstruction measures general scientific reasoning.”
- “This reveals private author reasoning.”
- “This is RLVR.”
- “The judge reliably detects scientific hallucinations” without per-type sensitivity, specificity, calibration, and natural-error validation.

## 7. Design recommendation

Implement the evidence-ablated adjacent condition on a small stage-gate sample before scaling:

- six paragraphs;
- five conditions, one frozen decode, Gemma 3 4B;
- blinded manual scoring of every atomic claim;
- separate lexical-copy score;
- at least four clean and four corrupted claims per error type for preliminary judge sensitivity/specificity;
- stop or reframe if true adjacent does not beat evidence-ablated adjacent, if gains are confined to copied claims, or if consequential numeric/direction/comparator/condition errors are not detected reliably.

Also treat publication-date and prior-only phrase overlap as contamination diagnostics, not proof that training examples were or were not present.

## 8. Full references

1. Wyatt, C., Joshi, A., & Salim, F. D. (2025). [What am I missing here?: Evaluating Large Language Models for Masked Sentence Prediction](https://aclanthology.org/2025.ijcnlp-short.24/). *IJCNLP-AACL 2025*, 273–283. https://doi.org/10.18653/v1/2025.ijcnlp-short.24
2. Donahue, C., Lee, M., & Liang, P. (2020). [Enabling Language Models to Fill in the Blanks](https://aclanthology.org/2020.acl-main.225/). *ACL 2020*, 2492–2501. https://doi.org/10.18653/v1/2020.acl-main.225
3. Huang, Y., Zhang, Y., Elachqar, O., & Cheng, Y. (2020). [INSET: Sentence Infilling with INter-SEntential Transformer](https://aclanthology.org/2020.acl-main.226/). *ACL 2020*, 2502–2515. https://doi.org/10.18653/v1/2020.acl-main.226
4. Zhang, J., Zhao, Y., Saleh, M., & Liu, P. J. (2020). [PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization](https://proceedings.mlr.press/v119/zhang20ae.html). *ICML 2020*, 11328–11339.
5. Lewis, M., Liu, Y., Goyal, N., et al. (2020). [BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://aclanthology.org/2020.acl-main.703/). *ACL 2020*, 7871–7880. https://doi.org/10.18653/v1/2020.acl-main.703
6. Beltagy, I., Lo, K., & Cohan, A. (2019). [SciBERT: A Pretrained Language Model for Scientific Text](https://aclanthology.org/D19-1371/). *EMNLP-IJCNLP 2019*, 3615–3620. https://doi.org/10.18653/v1/D19-1371
7. Wen, B., Howe, B., & Wang, L. L. (2024). [Characterizing LLM Abstention Behavior in Science QA with Context Perturbations](https://aclanthology.org/2024.findings-emnlp.197/). *Findings of EMNLP 2024*, 3437–3450. https://doi.org/10.18653/v1/2024.findings-emnlp.197
8. Yu, J., Tang, Y., Feng, K., et al. (2026). [SciCUEval: A Comprehensive Dataset for Evaluating Scientific Context Understanding in Large Language Models](https://www.nature.com/articles/s41597-026-06594-9). *Scientific Data, 13*, 530. https://doi.org/10.1038/s41597-026-06594-9
9. Javaji, S. R., Cao, Y., Li, H., Yu, Y., Muralidhar, N., & Zhu, Z. (2025). [Can AI Validate Science? Benchmarking LLMs for Accurate Scientific Claim → Evidence Reasoning](https://arxiv.org/abs/2506.08235). arXiv:2506.08235.
10. Imran, S., & Solanky, D. S. (2026). [ResearchQA: Benchmarking Citation-Grounded Question-Answering on Scientific Papers](https://arxiv.org/abs/2607.11074). arXiv:2607.11074.
11. Wadden, D., Lin, S., Lo, K., Wang, L. L., van Zuylen, M., Cohan, A., & Hajishirzi, H. (2020). [Fact or Fiction: Verifying Scientific Claims](https://aclanthology.org/2020.emnlp-main.609/). *EMNLP 2020*, 7534–7550. https://doi.org/10.18653/v1/2020.emnlp-main.609
12. Lehman, E., DeYoung, J., Barzilay, R., & Wallace, B. C. (2019). [Inferring Which Medical Treatments Work from Reports of Clinical Trials](https://aclanthology.org/N19-1371/). *NAACL-HLT 2019*, 3705–3717. https://doi.org/10.18653/v1/N19-1371
13. DeYoung, J., Lehman, E., Nye, B., Marshall, I., & Wallace, B. C. (2020). [Evidence Inference 2.0: More Data, Better Models](https://aclanthology.org/2020.bionlp-1.13/). *BioNLP 2020*, 123–132. https://doi.org/10.18653/v1/2020.bionlp-1.13
14. Min, S., Krishna, K., Lyu, X., et al. (2023). [FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation](https://aclanthology.org/2023.emnlp-main.741/). *EMNLP 2023*, 12076–12100. https://doi.org/10.18653/v1/2023.emnlp-main.741
15. Song, Y., Kim, Y., & Iyyer, M. (2024). [VeriScore: Evaluating the Factuality of Verifiable Claims in Long-Form Text Generation](https://aclanthology.org/2024.findings-emnlp.552/). *Findings of EMNLP 2024*. https://doi.org/10.18653/v1/2024.findings-emnlp.552
16. Stenzl, A., Rogers, E., Ananiadou, S., et al. (2026). [Enhancing the Quality and Trustworthiness of Large Language Model-Generated Summaries of Clinical Oncology Literature](https://pubmed.ncbi.nlm.nih.gov/42318048/). *JAMIA Open, 9*(3), ooag078. https://doi.org/10.1093/jamiaopen/ooag078
17. Kryscinski, W., McCann, B., Xiong, C., & Socher, R. (2020). [Evaluating the Factual Consistency of Abstractive Text Summarization](https://aclanthology.org/2020.emnlp-main.750/). *EMNLP 2020*, 9332–9346. https://doi.org/10.18653/v1/2020.emnlp-main.750
18. Pagnoni, A., Balachandran, V., & Tsvetkov, Y. (2021). [Understanding Factuality in Abstractive Summarization with FRANK](https://aclanthology.org/2021.naacl-main.383/). *NAACL-HLT 2021*. https://doi.org/10.18653/v1/2021.naacl-main.383
19. Wang, Y., Preiß, M., Bugueño, M., Hoffbauer, J. V., Ghajar, A., Buz, T., & de Melo, G. (2026). [ReFACT: A Benchmark for Scientific Confabulation Detection with Positional Error Annotations](https://aclanthology.org/2026.eacl-long.381/). *EACL 2026*, 8174–8187. https://doi.org/10.18653/v1/2026.eacl-long.381
20. Mujahid, Z. M., Wright, D., & Augenstein, I. (2026). [Stress Testing Factual Consistency Metrics for Long-Document Summarization](https://aclanthology.org/2026.acl-long.1472/). *ACL 2026*, 31914–31933. https://doi.org/10.18653/v1/2026.acl-long.1472
21. Jacovi, A., Bitton, Y., Bohnet, B., et al. (2024). [A Chain-of-Thought Is as Strong as Its Weakest Link: A Benchmark for Verifiers of Reasoning Chains](https://aclanthology.org/2024.acl-long.254/). *ACL 2024*, 4615–4634. https://doi.org/10.18653/v1/2024.acl-long.254
22. Xiao, Y., et al. (2026). [Document Reconstruction Unlocks Scalable Long-Context RLVR](https://arxiv.org/abs/2602.08237). arXiv:2602.08237.
23. Guo, J., Huang, C., & Fang, X. (2026). [Can MLLMs “Read” What Is Missing?](https://arxiv.org/abs/2604.21277). arXiv:2604.21277.

## Final verdict

**Confidence: 86/100.** Confidence is high that the complete experiment was not duplicated in the checked literature and that its appropriate framing is document grounding. It is lower than certainty because novelty is an absence claim, several closest papers are recent, and unindexed work may exist. The decisive result is the absence of the full combination despite direct precedents for every component—and the fact that the proposed four arms remain causally confounded without evidence ablation.

**Incremental but defensible**
