# Reference verification record

Every bibliography entry was checked automatically against an independent source on 2026-11-22 (by the thesis build tools). Requests contained only bibliographic titles and DOIs.

## Method

1. **Title search in OpenAlex.** The best match must have a title similarity of at least 0.90, contain the first author's surname, and have the expected year (preprint and proceedings may differ by one year). (DBLP, the first choice, answers automated clients with a browser challenge.)
2. **Citation data from doi.org.** Where the match has a publisher DOI, the bibliographic fields are taken from the DOI's CSL-JSON record (Crossref or DataCite), which has properly split author names.
3. **Published versions.** OpenAlex merges a preprint with its proceedings version. For proceedings without DOIs (PMLR, NeurIPS, ICLR, USENIX, MLSys) the published version is cited and verified on the official page: the page must load and contain the title; PMLR pages must also show the cited pages and year. Two venues were verified through the venue note of the arXiv record (ICLR 2018, ICML 2012) because OpenReview and the ICML 2012 site do not serve automated clients.
4. **Standards and legislation** (GDPR, FIPS 180-4) were checked by resolving their official URL or DOI.

## Result

93 references: 62 VERIFIED (OpenAlex, doi.org), 2 VERIFIED (arXiv venue note), 5 VERIFIED (doi.org), 22 VERIFIED (official page), 2 VERIFIED (resolved).

No reference was found to be fabricated or unresolvable.

### Corrections to the draft thesis's reference list

* `li2022secure` (draft [58]): the draft cites arXiv:2205.06117 (2022); the peer-reviewed workshop version (DistributedML@CoNEXT 2021, DOI 10.1145/3488659.3493776) is cited.
* `zhou2021augmented` (draft [76]): the draft's DOI 10.1109/GLOCOM.2021.9685154 does not resolve (HTTP 404); the correct DOI is 10.1109/GLOBECOM46510.2021.9685154.
* `feng2023voyager` (draft [78]): the draft cites arXiv:2310.08739 (2023); the peer-reviewed version (IEEE/IFIP NOMS 2024, DOI 10.1109/NOMS59830.2024.10575335) is cited.

### Verification notes (no change to the draft's citation)

* `bagdasaryan2020backdoor` (draft [1]): the title search matched the arXiv preprint (2018); the published version (Proc. Int. Conf. Artificial Intelligence and Statistics (AISTATS), PMLR, 2020) was verified separately and is cited.
* `fang2020local` (draft [2]): the title search matched the arXiv preprint (2019); the published version (Proc. 29th USENIX Security Symp., 2020) was verified separately and is cited.
* `zhu2019deep` (draft [3]): the title search matched a later book-chapter version (LNCS 12500, 2020); the NeurIPS 2019 paper cited in the draft was verified on the official proceedings page and is cited.
* `yin2018byzantine` (draft [7]): the title search matched the arXiv preprint (2018); the published version (Proc. Int. Conf. Machine Learning (ICML), PMLR, 2018) was verified separately and is cited.
* `baruch2019little` (draft [9]): the title search matched the arXiv preprint (2019); the published version (Advances in Neural Information Processing Systems, 2019) was verified separately and is cited.
* `mcmahan2017communication` (draft [10]): the title search matched the arXiv preprint (2016); the published version (Proc. Int. Conf. Artificial Intelligence and Statistics (AISTATS), PMLR, 2017) was verified separately and is cited.
* `li2020federated` (draft [18]): the title search matched the arXiv preprint (2018); the published version (Proc. Machine Learning and Systems (MLSys), 2020) was verified separately and is cited.
* `biggio2012poisoning` (draft [26]): the title search matched the arXiv preprint (2012); the published version (Proc. 29th Int. Conf. Machine Learning (ICML), 2012) was verified separately and is cited.
* `xie2020fall` (draft [28]): the title search matched the arXiv preprint (2019); the published version (Proc. Conf. Uncertainty in Artificial Intelligence (UAI), PMLR, 2020) was verified separately and is cited.
* `wang2020attack` (draft [32]): the title search matched the arXiv preprint (2020); the published version (Advances in Neural Information Processing Systems, 2020) was verified separately and is cited.
* `geiping2020inverting` (draft [39]): the title search matched the arXiv preprint (2020); the published version (Advances in Neural Information Processing Systems, 2020) was verified separately and is cited.
* `huang2021evaluating` (draft [40]): the title search matched the arXiv preprint (2021); the published version (Advances in Neural Information Processing Systems, 2021) was verified separately and is cited.
* `fowl2022robbing` (draft [41]): the title search matched the arXiv preprint (2021); the published version (Proc. Int. Conf. Learning Representations (ICLR), 2022) was verified separately and is cited.
* `elmhamdi2018hidden` (draft [43]): the title search matched the arXiv preprint (2018); the published version (Proc. Int. Conf. Machine Learning (ICML), PMLR, 2018) was verified separately and is cited.
* `mcmahan2018learning` (draft [49]): the title search matched the arXiv preprint (2017); the published version (Proc. Int. Conf. Learning Representations (ICLR), 2018) was verified separately and is cited.
* `bagdasaryan2019differential` (draft [51]): the title search matched the arXiv preprint (2019); the published version (Advances in Neural Information Processing Systems, 2019) was verified separately and is cited.
* `goldreich1987play` (draft [53]): the title search matched a 2019 reprint (ACM Books); the STOC 1987 original cited in the draft was verified through its DOI 10.1145/28395.28420 and is cited.
* `damgard2016confidential` (added): Financial Cryptography 2016, proceedings published 2017 (LNCS 9603); the publication year is cited.
* `paszke2019pytorch` (added): the title search matched the arXiv preprint (2019); the published version (Advances in Neural Information Processing Systems, 2019) was verified separately and is cited.
* `moritz2018ray` (added): the title search matched the arXiv preprint (2017); the published version (Proc. 13th USENIX Symp. Operating Systems Design and Implementation (OSDI), 2018) was verified separately and is cited.
* `bernstein2019signsgd` (added): the title search matched the arXiv preprint (2018); the published version (Proc. Int. Conf. Learning Representations (ICLR), 2019) was verified separately and is cited.

## Entries

| Key | Draft no. | Status | Year | DOI / URL | Evidence |
|---|---|---|---|---|---|
| `bagdasaryan2020backdoor` | 1 | VERIFIED (official page) | 2020 | https://proceedings.mlr.press/v108/bagdasaryan20a.html | page https://proceedings.mlr.press/v108/bagdasaryan20a.html: title found, pages and year found |
| `fang2020local` | 2 | VERIFIED (official page) | 2020 | https://www.usenix.org/conference/usenixsecurity20/presentation/fang | page https://www.usenix.org/conference/usenixsecurity20/presentation/fang: title found |
| `zhu2019deep` | 3 | VERIFIED (official page) | 2019 | https://proceedings.neurips.cc/paper_files/paper/2019/hash/60a6c4002cc7b29142def8871531281a-Abstract.html | page https://proceedings.neurips.cc/paper_files/paper/2019/hash/60a6c4002cc7b29142def8871531281a-Abstract.html: title found |
| `nasr2019comprehensive` | 4 | VERIFIED (OpenAlex, doi.org) | 2019 | 10.1109/sp.2019.00065 | OpenAlex https://openalex.org/W2930926105 (conference) |
| `shokri2017membership` | 5 | VERIFIED (OpenAlex, doi.org) | 2017 | 10.1109/sp.2017.41 | OpenAlex https://openalex.org/W2535690855 (conference) |
| `blanchard2017machine` | 6 | VERIFIED (official page) | 2017 | https://proceedings.neurips.cc/paper_files/paper/2017/hash/f4b9ec30ad9f68f89b29639786cb62ef-Abstract.html | page https://proceedings.neurips.cc/paper_files/paper/2017/hash/f4b9ec30ad9f68f89b29639786cb62ef-Abstract.html: title found |
| `yin2018byzantine` | 7 | VERIFIED (official page) | 2018 | https://proceedings.mlr.press/v80/yin18a.html | page https://proceedings.mlr.press/v80/yin18a.html: title found, pages and year found |
| `bonawitz2017practical` | 8 | VERIFIED (OpenAlex, doi.org) | 2017 | 10.1145/3133956.3133982 | OpenAlex https://openalex.org/W2767079719 (conference) |
| `baruch2019little` | 9 | VERIFIED (official page) | 2019 | https://proceedings.neurips.cc/paper_files/paper/2019/hash/ec1c59141046cd1866bbbcdfb6ae31d4-Abstract.html | page https://proceedings.neurips.cc/paper_files/paper/2019/hash/ec1c59141046cd1866bbbcdfb6ae31d4-Abstract.html: title found |
| `mcmahan2017communication` | 10 | VERIFIED (official page) | 2017 | https://proceedings.mlr.press/v54/mcmahan17a.html | page https://proceedings.mlr.press/v54/mcmahan17a.html: title found, pages and year found |
| `beutel2020flower` | 11 | VERIFIED (OpenAlex, doi.org) | 2020 | 10.48550/arxiv.2007.14390 | OpenAlex https://openalex.org/W3046183292 (repository) |
| `konecny2016federated` | 12 | VERIFIED (OpenAlex, doi.org) | 2016 | 10.48550/arxiv.1610.05492 | OpenAlex https://openalex.org/W2535838896 (repository) |
| `kairouz2021advances` | 13 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.1561/9781680837896 | OpenAlex https://openalex.org/W2995022099 (journal) |
| `hard2018federated` | 14 | VERIFIED (OpenAlex, doi.org) | 2018 | 10.48550/arxiv.1811.03604 | OpenAlex https://openalex.org/W2900120080 (repository) |
| `rieke2020future` | 15 | VERIFIED (doi.org) | 2020 | 10.1038/s41746-020-00323-1 | doi.org CSL-JSON for 10.1038/s41746-020-00323-1; published version cited |
| `yang2019federated` | 16 | VERIFIED (OpenAlex, doi.org) | 2019 | 10.1145/3298981 | OpenAlex https://openalex.org/W2912213068 (journal) |
| `zhao2018federated` | 17 | VERIFIED (OpenAlex, doi.org) | 2018 | 10.48550/arxiv.1806.00582 | OpenAlex https://openalex.org/W2807006176 (repository) |
| `li2020federated` | 18 | VERIFIED (official page) | 2020 | https://proceedings.mlsys.org/paper_files/paper/2020/hash/1f5fe83998a09396ebe6477d9475ba0c-Abstract.html | page https://proceedings.mlsys.org/paper_files/paper/2020/hash/1f5fe83998a09396ebe6477d9475ba0c-Abstract.html: title found |
| `li2020challenges` | 19 | VERIFIED (OpenAlex, doi.org) | 2020 | 10.1109/msp.2020.2975749 | OpenAlex https://openalex.org/W3021654819 (journal) |
| `feng2024leveraging` | 20 | VERIFIED (OpenAlex, doi.org) | 2024 | 10.1109/bigdata62323.2024.10825953 | OpenAlex https://openalex.org/W4406458813 (conference) |
| `gdpr2016` | 21 | VERIFIED (resolved) | 2016 | https://eur-lex.europa.eu/eli/reg/2016/679/oj | HTTP GET https://eur-lex.europa.eu/eli/reg/2016/679/oj: ok |
| `martinezbeltran2023decentralized` | 22 | VERIFIED (OpenAlex, doi.org) | 2023 | 10.1109/comst.2023.3315746 | OpenAlex https://openalex.org/W4386766438 (journal) |
| `lyu2020threats` | 23 | VERIFIED (OpenAlex, doi.org) | 2020 | 10.48550/arxiv.2003.02133 | OpenAlex https://openalex.org/W3010262580 (repository) |
| `mothukuri2021survey` | 24 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.1016/j.future.2020.10.007 | OpenAlex https://openalex.org/W3091870957 (journal) |
| `rodriguezbarroso2023survey` | 25 | VERIFIED (OpenAlex, doi.org) | 2023 | 10.1016/j.inffus.2022.09.011 | OpenAlex https://openalex.org/W4295806247 (journal) |
| `biggio2012poisoning` | 26 | VERIFIED (arXiv venue note) | 2012 |  | page https://arxiv.org/abs/1206.6389: title found, 'ICML 2012' found |
| `tolpegin2020data` | 27 | VERIFIED (OpenAlex, doi.org) | 2020 | 10.1007/978-3-030-58951-6_24 | OpenAlex https://openalex.org/W3087391814 (book series) |
| `xie2020fall` | 28 | VERIFIED (official page) | 2020 | https://proceedings.mlr.press/v115/xie20a.html | page https://proceedings.mlr.press/v115/xie20a.html: title found, pages and year found |
| `shejwalkar2021manipulating` | 29 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.14722/ndss.2021.24498 | OpenAlex https://openalex.org/W3138153888 (conference) |
| `gu2017badnets` | 30 | VERIFIED (OpenAlex, doi.org) | 2017 | 10.48550/arxiv.1708.06733 | OpenAlex https://openalex.org/W2748789698 (repository) |
| `bhagoji2019analyzing` | 31 | VERIFIED (official page) | 2019 | https://proceedings.mlr.press/v97/bhagoji19a.html | page https://proceedings.mlr.press/v97/bhagoji19a.html: title found, pages and year found |
| `wang2020attack` | 32 | VERIFIED (official page) | 2020 | https://proceedings.neurips.cc/paper_files/paper/2020/hash/b8ffa41d4e492f0fad2f13e29e1762eb-Abstract.html | page https://proceedings.neurips.cc/paper_files/paper/2020/hash/b8ffa41d4e492f0fad2f13e29e1762eb-Abstract.html: title found |
| `sun2019can` | 33 | VERIFIED (OpenAlex, doi.org) | 2019 | 10.48550/arxiv.1911.07963 | OpenAlex https://openalex.org/W2990595670 (repository) |
| `shejwalkar2022back` | 34 | VERIFIED (OpenAlex, doi.org) | 2022 | 10.1109/sp46214.2022.9833647 | OpenAlex https://openalex.org/W4288057793 (conference) |
| `carlini2022membership` | 35 | VERIFIED (OpenAlex, doi.org) | 2022 | 10.1109/sp46214.2022.9833649 | OpenAlex https://openalex.org/W4288057780 (conference) |
| `melis2019exploiting` | 36 | VERIFIED (OpenAlex, doi.org) | 2019 | 10.1109/sp.2019.00029 | OpenAlex https://openalex.org/W2898291644 (conference) |
| `hitaj2017deep` | 37 | VERIFIED (OpenAlex, doi.org) | 2017 | 10.1145/3133956.3134012 | OpenAlex https://openalex.org/W2591882872 (conference) |
| `zhao2020idlg` | 38 | VERIFIED (OpenAlex, doi.org) | 2020 | 10.48550/arxiv.2001.02610 | OpenAlex https://openalex.org/W3000479830 (repository) |
| `geiping2020inverting` | 39 | VERIFIED (official page) | 2020 | https://proceedings.neurips.cc/paper_files/paper/2020/hash/c4ede56bbd98819ae6112b20ac6bf145-Abstract.html | page https://proceedings.neurips.cc/paper_files/paper/2020/hash/c4ede56bbd98819ae6112b20ac6bf145-Abstract.html: title found |
| `huang2021evaluating` | 40 | VERIFIED (official page) | 2021 | https://proceedings.neurips.cc/paper_files/paper/2021/hash/3b3fff6463464959dcd1b68d0320f781-Abstract.html | page https://proceedings.neurips.cc/paper_files/paper/2021/hash/3b3fff6463464959dcd1b68d0320f781-Abstract.html: title found |
| `fowl2022robbing` | 41 | VERIFIED (official page) | 2022 |  | page https://iclr.cc/virtual/2022/papers.html: title found |
| `pasquini2022eluding` | 42 | VERIFIED (OpenAlex, doi.org) | 2022 | 10.1145/3548606.3560557 | OpenAlex https://openalex.org/W3212079419 (conference) |
| `elmhamdi2018hidden` | 43 | VERIFIED (official page) | 2018 | https://proceedings.mlr.press/v80/mhamdi18a.html | page https://proceedings.mlr.press/v80/mhamdi18a.html: title found, pages and year found |
| `pillutla2022robust` | 44 | VERIFIED (OpenAlex, doi.org) | 2022 | 10.1109/tsp.2022.3153135 | OpenAlex https://openalex.org/W2996769125 (journal) |
| `fung2020limitations` | 45 | VERIFIED (official page) | 2020 | https://www.usenix.org/conference/raid2020/presentation/fung | page https://www.usenix.org/conference/raid2020/presentation/fung: title found |
| `cao2021fltrust` | 46 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.14722/ndss.2021.24434 | OpenAlex https://openalex.org/W3138597937 (conference) |
| `nguyen2022flame` | 47 | VERIFIED (official page) | 2022 | https://www.usenix.org/conference/usenixsecurity22/presentation/nguyen | page https://www.usenix.org/conference/usenixsecurity22/presentation/nguyen: title found |
| `dwork2014algorithmic` | 48 | VERIFIED (OpenAlex, doi.org) | 2014 | 10.1561/0400000042 | OpenAlex https://openalex.org/W4205228770 (journal) |
| `mcmahan2018learning` | 49 | VERIFIED (arXiv venue note) | 2018 |  | page https://arxiv.org/abs/1710.06963: title found, 'ICLR 2018' found |
| `geyer2017differentially` | 50 | VERIFIED (OpenAlex, doi.org) | 2017 | 10.48550/arxiv.1712.07557 | OpenAlex https://openalex.org/W2777914285 (repository) |
| `bagdasaryan2019differential` | 51 | VERIFIED (official page) | 2019 | https://proceedings.neurips.cc/paper_files/paper/2019/hash/fc0de4e0396fff257ea362983c2dda5a-Abstract.html | page https://proceedings.neurips.cc/paper_files/paper/2019/hash/fc0de4e0396fff257ea362983c2dda5a-Abstract.html: title found |
| `yao1982protocols` | 52 | VERIFIED (doi.org) | 1982 | 10.1109/SFCS.1982.38 | doi.org CSL-JSON for 10.1109/SFCS.1982.38; published version cited |
| `goldreich1987play` | 53 | VERIFIED (doi.org) | 1987 | 10.1145/28395.28420 | doi.org CSL-JSON for 10.1145/28395.28420; published version cited |
| `shamir1979share` | 54 | VERIFIED (OpenAlex, doi.org) | 1979 | 10.1145/359168.359176 | OpenAlex https://openalex.org/W2141420453 (journal) |
| `damgard2012multiparty` | 55 | VERIFIED (OpenAlex, doi.org) | 2012 | 10.1007/978-3-642-32009-5_38 | OpenAlex https://openalex.org/W2402235285 (book series) |
| `mohassel2017secureml` | 56 | VERIFIED (OpenAlex, doi.org) | 2017 | 10.1109/sp.2017.12 | OpenAlex https://openalex.org/W2701059868 (conference) |
| `bell2020secure` | 57 | VERIFIED (OpenAlex, doi.org) | 2020 | 10.1145/3372297.3417885 | OpenAlex https://openalex.org/W3037821247 (conference) |
| `li2022secure` | 58 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.1145/3488659.3493776 | OpenAlex https://openalex.org/W3216699651 (conference-paper) |
| `truex2019hybrid` | 59 | VERIFIED (OpenAlex, doi.org) | 2019 | 10.1145/3338501.3357370 | OpenAlex https://openalex.org/W2970606380 (conference) |
| `so2021byzantine` | 60 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.1109/jsac.2020.3041404 | OpenAlex https://openalex.org/W3107632872 (journal) |
| `roychowdhury2022eiffel` | 61 | VERIFIED (OpenAlex, doi.org) | 2022 | 10.1145/3548606.3560611 | OpenAlex https://openalex.org/W4308632285 (conference) |
| `lycklama2023rofl` | 62 | VERIFIED (OpenAlex, doi.org) | 2023 | 10.1109/sp46215.2023.10179400 | OpenAlex https://openalex.org/W4384948726 (conference) |
| `rathee2023elsa` | 63 | VERIFIED (OpenAlex, doi.org) | 2023 | 10.1109/sp46215.2023.10179468 | OpenAlex https://openalex.org/W4385299238 (conference) |
| `ma2022shieldfl` | 64 | VERIFIED (OpenAlex, doi.org) | 2022 | 10.1109/tifs.2022.3169918 | OpenAlex https://openalex.org/W4226047321 (journal) |
| `jajodia2011moving` | 65 | VERIFIED (OpenAlex, doi.org) | 2011 | 10.1007/978-1-4614-0977-9 | OpenAlex https://openalex.org/W2494110282 (book series) |
| `cai2016moving` | 66 | VERIFIED (OpenAlex, doi.org) | 2016 | 10.1631/fitee.1601321 | OpenAlex https://openalex.org/W2553733554 (journal) |
| `zheng2019survey` | 67 | VERIFIED (OpenAlex, doi.org) | 2019 | 10.1007/s11390-019-1906-z | OpenAlex https://openalex.org/W2914370086 (journal) |
| `sengupta2020survey` | 68 | VERIFIED (OpenAlex, doi.org) | 2020 | 10.1109/comst.2020.2982955 | OpenAlex https://openalex.org/W2942521954 (journal) |
| `zhuang2014towards` | 69 | VERIFIED (OpenAlex, doi.org) | 2014 | 10.1145/2663474.2663479 | OpenAlex https://openalex.org/W1999588868 (conference) |
| `shacham2004effectiveness` | 70 | VERIFIED (OpenAlex, doi.org) | 2004 | 10.1145/1030083.1030124 | OpenAlex https://openalex.org/W2098010707 (conference) |
| `roy2019moving` | 71 | VERIFIED (OpenAlex, doi.org) | 2019 | 10.1145/3318216.3363338 | OpenAlex https://openalex.org/W2988796733 (conference) |
| `amich2021morphence` | 72 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.1145/3485832.3485899 | OpenAlex https://openalex.org/W3198840923 (conference) |
| `sengupta2019mtdeep` | 73 | VERIFIED (OpenAlex, doi.org) | 2019 | 10.1007/978-3-030-32430-8_28 | OpenAlex https://openalex.org/W2768209273 (book series) |
| `qian2022eimtd` | 74 | VERIFIED (OpenAlex, doi.org) | 2022 | 10.1145/3517806 | OpenAlex https://openalex.org/W3087792431 (journal) |
| `qiu2021mtmtd` | 75 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.1109/icc42927.2021.9500545 | OpenAlex https://openalex.org/W3190255965 (conference) |
| `zhou2021augmented` | 76 | VERIFIED (OpenAlex, doi.org) | 2021 | 10.1109/globecom46510.2021.9685154 | OpenAlex https://openalex.org/W4226042189 (conference) |
| `martinezbeltran2024mitigating` | 77 | VERIFIED (OpenAlex, doi.org) | 2024 | 10.1007/s11276-024-03667-8 | OpenAlex https://openalex.org/W4391290232 (journal) |
| `feng2023voyager` | 78 | VERIFIED (OpenAlex, doi.org) | 2024 | 10.1109/noms59830.2024.10575335 | OpenAlex https://openalex.org/W4400234085 (conference) |
| `kianpisheh2025deep` | 79 | VERIFIED (OpenAlex, doi.org) | 2025 | 10.1109/globecom59602.2025.11432263 | OpenAlex https://openalex.org/W7138863920 (conference) |
| `cramer2018spdz2k` |  | VERIFIED (doi.org) | 2018 | 10.1007/978-3-319-96881-0_26 | doi.org CSL-JSON for 10.1007/978-3-319-96881-0_26; published version cited |
| `keller2020mpspdz` |  | VERIFIED (OpenAlex, doi.org) | 2020 | 10.1145/3372297.3417872 | OpenAlex https://openalex.org/W3030820238 (conference) |
| `damgard2016confidential` |  | VERIFIED (OpenAlex, doi.org) | 2017 | 10.1007/978-3-662-54970-4_10 | OpenAlex https://openalex.org/W2262308442 (book series) |
| `xiao2017fashion` |  | VERIFIED (OpenAlex, doi.org) | 2017 | 10.48550/arxiv.1708.07747 | OpenAlex https://openalex.org/W2750384547 (repository) |
| `paszke2019pytorch` |  | VERIFIED (official page) | 2019 | https://proceedings.neurips.cc/paper_files/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html | page https://proceedings.neurips.cc/paper_files/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html: title found |
| `moritz2018ray` |  | VERIFIED (official page) | 2018 | https://www.usenix.org/conference/osdi18/presentation/moritz | page https://www.usenix.org/conference/osdi18/presentation/moritz: title found |
| `bernstein2019signsgd` |  | VERIFIED (official page) | 2019 |  | page https://iclr.cc/Conferences/2019/Schedule?type=Poster: title found |
| `xu2022signguard` |  | VERIFIED (OpenAlex, doi.org) | 2022 | 10.1109/icdcs54860.2022.00120 | OpenAlex https://openalex.org/W4313042326 (conference) |
| `phong2018privacy` |  | VERIFIED (OpenAlex, doi.org) | 2018 | 10.1109/tifs.2017.2787987 | OpenAlex https://openalex.org/W2781091734 (journal) |
| `wang2004ssim` |  | VERIFIED (OpenAlex, doi.org) | 2004 | 10.1109/tip.2003.819861 | OpenAlex https://openalex.org/W2133665775 (journal) |
| `ryffel2018generic` |  | VERIFIED (OpenAlex, doi.org) | 2018 | 10.48550/arxiv.1811.04017 | OpenAlex https://openalex.org/W2900319533 (repository) |
| `bell2023acorn` |  | VERIFIED (official page) | 2023 | https://www.usenix.org/conference/usenixsecurity23/presentation/bell | page https://www.usenix.org/conference/usenixsecurity23/presentation/bell: title found |
| `krawczyk1997hmac` |  | VERIFIED (doi.org) | 1997 | 10.17487/rfc2104 | doi.org CSL-JSON |
| `nist2015sha` |  | VERIFIED (resolved) | 2015 | https://doi.org/10.6028/NIST.FIPS.180-4 | HTTP GET https://doi.org/10.6028/NIST.FIPS.180-4: ok |

## Formatting corrections after verification

Applied to the verified entries. No entry was added or removed, no DOI, URL or year changed, and every entry still identifies the same verified publication.

| Key | Field | Before | After | Source |
|---|---|---|---|---|
| `mcmahan2017communication` | author (given / family) | Blaise Agüera y / Arcas | Blaise / Agüera y Arcas | PMLR v54 author list |
| `beutel2020flower` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `konecny2016federated` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `kairouz2021advances` | author (given / family) | Arjun / Nitin Bhagoji | Arjun Nitin / Bhagoji | Crossref name split |
| `hard2018federated` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `yang2019federated` | title | "Federated Machine Learning" | "Federated Machine Learning: Concept and Applications" | Crossref subtitle |
| `zhao2018federated` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `feng2024leveraging` | author (given / family) | Jan von / der Assen | Jan / von der Assen | Crossref name split |
| `gdpr2016` | type | "legislation" | "article-journal" | published in the Official Journal; renders as a periodical |
| `gdpr2016` | title | "Regulation (EU) 2016/679 (General Data Protection Regulation)" | "Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural pe… | official title of the act (EUR-Lex) |
| `gdpr2016` | issued | {"date-parts": [[2016]]} | {"date-parts": [[2016, 5, 4]]} | OJ L 119 of 4 May 2016 |
| `lyu2020threats` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `tolpegin2020data` | container-title | "Lecture Notes in Computer Science" | "Computer Security – ESORICS 2020" | Crossref container-title is [Lecture Notes in Computer Science, book title]; the book title is the proceedings |
| `gu2017badnets` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `sun2019can` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `hitaj2017deep` | title | "Deep Models Under the GAN" | "Deep Models Under the GAN: Information Leakage from Collaborative Deep Learning" | Crossref subtitle |
| `zhao2020idlg` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `elmhamdi2018hidden` | author (given / family) | El Mahdi El / Mhamdi | El Mahdi / El Mhamdi | PMLR v80 author list |
| `geyer2017differentially` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `damgard2012multiparty` | container-title | "Lecture Notes in Computer Science" | "Advances in Cryptology – CRYPTO 2012" | Crossref container-title is [Lecture Notes in Computer Science, book title]; the book title is the proceedings |
| `roychowdhury2022eiffel` | title | "EIFFeL" | "EIFFeL: Ensuring Integrity for Federated Learning" | Crossref subtitle |
| `jajodia2011moving` | title | "Moving Target Defense" | "Moving Target Defense: Creating Asymmetric Uncertainty for Cyber Threats" | Crossref subtitle |
| `sengupta2019mtdeep` | container-title | "Lecture Notes in Computer Science" | "Decision and Game Theory for Security" | Crossref container-title is [Lecture Notes in Computer Science, book title]; the book title is the proceedings |
| `zhou2021augmented` | page | "01-06" | "1-6" | zero-padded page range in the Crossref record |
| `cramer2018spdz2k` | title | "SPD$$\\mathbb {Z}_{2^k}$$: Efficient MPC mod $$2^k$$ for Dishonest Majority" | "SPDℤ<sub>2<sup>k</sup></sub>: Efficient MPC mod 2<sup>k</sup> for Dishonest Majority" | TeX markup in the Crossref title replaced by the typeset title |
| `cramer2018spdz2k` | container-title | "Lecture Notes in Computer Science" | "Advances in Cryptology – CRYPTO 2018" | Crossref container-title is [Lecture Notes in Computer Science, book title]; the book title is the proceedings |
| `damgard2016confidential` | container-title | "Lecture Notes in Computer Science" | "Financial Cryptography and Data Security" | Crossref container-title is [Lecture Notes in Computer Science, book title]; the book title is the proceedings |
| `xiao2017fashion` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `wang2004ssim` | author (given / family) | None / Zhou Wang | Zhou / Wang | Crossref stores the full name as family name |
| `ryffel2018generic` | publisher | "arXiv" | (removed) | avoids 'arXiv: arXiv:' in the IEEE style |
| `krawczyk1997hmac` | genre | null | "RFC" | RFC series |
| `krawczyk1997hmac` | number | null | "2104" | RFC number (DOI 10.17487/rfc2104) |
| `krawczyk1997hmac` | container-title | "" | (removed) | empty field |
