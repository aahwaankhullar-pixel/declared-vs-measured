# Declared vs. Measured: India's "Open Defecation Free" Status and What the National Health Survey Found

**Aahwaan Khullar** · Shiv Nadar School, Faridabad, India · October 2026

A short data note and fully reproducible analysis. It is a companion to my paper [*A Computational Text Analysis of Stakeholder Framing in the Swachh Bharat Mission*](https://github.com/aahwaankhullar-pixel/sbm-analysis), which found that the way the mission is *described* depends on who is writing. This note asks a related question about the numbers: does what gets *measured* depend on who is measuring?

## Question

By 2 October 2019, every Indian state had declared its rural areas open defecation free (ODF) under the Swachh Bharat Mission (SBM), and rural India as a whole was declared ODF. These declarations come from the same administrative system that was responsible for building the toilets. The National Family Health Survey (NFHS), run independently by the International Institute for Population Sciences, measured sanitation in every district at almost the same time.

1. How close is measured sanitation to what the declaration implies?
2. How much did districts actually change during SBM's first phase?
3. Did districts that gained more sanitation also see larger improvements in child health?

## Data

- **Source:** the official NFHS-5 (2019–21) district fact sheets published by IIPS for the Ministry of Health and Family Welfare. Each sheet also reports the NFHS-4 (2015–16) value for the same district where one exists.
- **Coverage:** 704 districts in 34 states and union territories. 572 districts have both rounds; most of the rest were created after 2015–16.
- **Extraction:** values were read directly from the published PDFs with `code/extract_pdfs.py`. The PDFs come from the [SaiSiddhardhaKalla/NFHS](https://github.com/SaiSiddhardhaKalla/NFHS) archive. Cross-checked against two community CSV conversions ([pratapvardhan/NFHS-5](https://github.com/pratapvardhan/NFHS-5) and SaiSiddhardhaKalla/NFHS), the values agree for 98.8% of districts. The disagreements came from errors in the CSVs (for example, Delhi's districts shifted by one row), so the official PDFs are used throughout.
- **Main measure:** "Population living in households that use an improved sanitation facility (%)". NFHS defines this as a flush or pour-flush toilet, ventilated or slab pit latrine, or twin-pit/composting toilet **that is not shared with another household**.
- **Timing:** fieldwork in 13 states began in January 2020, entirely after the ODF declaration (dates as printed in each fact sheet). The other states were surveyed between June 2019 and February 2020.

## Findings

### 1. Measured sanitation is far from what "open defecation free" implies

![District distribution](figures/fig1_district_distribution.png)

- In the **median district, 74%** of people used an improved sanitation facility. That is well short of the near-universal use the ODF declaration implies.
- **42% of districts were below 70%**, 57 districts (8%) were below 50%, and only 6% reached 90%.
- The lowest was Puruliya, West Bengal, at 29%, followed by Bijapur (Chhattisgarh) and Araria (Bihar).
- **The result does not depend on survey timing.** In the 363 districts surveyed entirely after the declaration, the median was 73% and 44% were below 70%.

![States](figures/fig3_states.png)

The gap is uneven:
- The median district is 99% in Kerala but 49% in Bihar, where 20 of 38 districts were below 50%.
- Uttar Pradesh, Bihar, Madhya Pradesh, Odisha and Jharkhand together hold most of the districts below 70%.

### 2. The progress was still real, and largest where it was most needed

![Before and after](figures/fig2_before_after.png)

- Between 2015–16 and 2019–21, the **median district gained 23 percentage points**, and the median coverage rose from 46% to 72%.
- 59% of districts gained 20 points or more, and only 3.5% declined.
- Districts that started lowest gained most: each point lower at baseline meant about 0.45 points more gain.

So the official claim overstates the result, but the independent data show a large, broad improvement. That matches the mixed picture in the research literature.

### 3. Sanitation gains and child health: an association that does not survive controls

![Health changes](figures/fig4_health_changes.png)

| Change in outcome (percentage points) per +10 pp gain in sanitation | No controls | With controls and state fixed effects |
|---|---|---|
| Child diarrhoea (last 2 weeks) | −0.69 [−1.66, 0.28] | +0.16 [−0.57, 0.89] |
| Child stunting | **−1.26 [−2.01, −0.52]** | −0.24 [−1.04, 0.55] |
| Child underweight | **−1.45 [−2.42, −0.49]** | −0.23 [−1.09, 0.64] |

Notes on the table:
- These are first-difference regressions across 572 districts; 95% confidence intervals, clustered by state, are in brackets.
- The controls are changes in electricity, improved drinking water, clean cooking fuel, and women with 10 or more years of schooling.

What the table shows:
- On their own, districts with larger sanitation gains also saw larger falls in stunting and underweight.
- But those districts were also gaining electricity, clean fuel and schooling. Once those changes and state-level differences are accounted for, the sanitation association shrinks to roughly zero.

**This does not show that sanitation has no health effect.** It shows that district-level survey averages cannot separate sanitation from the broader development happening alongside it. Answering that needs household-level data or a stronger design, such as the randomised trials in this literature, which have often found small or no effects of household sanitation on child growth (Humphrey et al., 2019; Luby et al., 2018; Null et al., 2018).

## Limitations

- **The measure understates toilet access.** It excludes toilets shared between households, and the fact sheets themselves note that "this indicator does not denote access to toilet facility completely." Part of the gap with the ODF declaration is about definitions, not open defecation, so these numbers should not be read as open-defecation rates. Mohanan (2022) discusses how NFHS and the government's own rural sanitation survey differ.
- **District totals include urban areas,** while the ODF declaration was for rural areas. Urban coverage is usually higher, so this makes the measured gap *smaller* than the rural gap.
- **District estimates are survey estimates** with sampling error, and 132 districts lack an NFHS-4 value. All district averages are unweighted.
- **The regressions are associations at the district level,** not causal effects.

## Reproduce it

- **Google Colab:** open `declared_vs_measured.ipynb` and choose *Runtime → Run all*. The data file is fetched from this repository.
- **Locally:** run `python code/analysis.py data/nfhs_district_fact_sheets.csv .`. It needs pandas, numpy and matplotlib; the regression and clustered standard errors are written out in plain NumPy so the method is visible.
- **Re-extract from the PDFs:** run `python code/extract_pdfs.py <folder of fact-sheet PDFs> data/nfhs_district_fact_sheets.csv`.

```
data/nfhs_district_fact_sheets.csv   district values read from the official fact sheets
code/extract_pdfs.py                 PDF → CSV extraction
code/analysis.py                     full analysis (also run inside the notebook)
declared_vs_measured.ipynb           notebook with outputs
results/                             summary numbers, state table, regressions, district panel
figures/                             the four charts above
```

## References

- Humphrey, J. H., et al. (2019). Independent and combined effects of improved water, sanitation, and hygiene, and improved complementary feeding, on child stunting and anaemia in rural Zimbabwe: A cluster-randomised trial. *The Lancet Global Health, 7*(1), e132–e147.
- International Institute for Population Sciences (IIPS) & Ministry of Health and Family Welfare. (2021). *National Family Health Survey (NFHS-5), 2019–21: District fact sheets.*
- Luby, S. P., et al. (2018). Effects of water quality, sanitation, handwashing, and nutritional interventions on diarrhoea and child growth in rural Bangladesh: A cluster randomised controlled trial. *The Lancet Global Health, 6*(3), e302–e315.
- Mohanan, P. C. (2022, March 7). *Rural sanitation: NFHS vs other surveys.* Centre for Economic Data and Analysis, Ashoka University.
- Null, C., et al. (2018). Effects of water quality, sanitation, handwashing, and nutritional interventions on diarrhoea and child growth in rural Kenya: A cluster-randomised controlled trial. *The Lancet Global Health, 6*(3), e316–e329.
- The Wire. (2019, October 2). *Modi declares rural India open defecation free, questions remain.*

## License and citation

Code is released under the MIT License. The data are derived from publicly released NFHS fact sheets.

Khullar, A. (2026). *Declared vs. measured: India's "open defecation free" status and what the national health survey found* [Data note and code]. https://github.com/aahwaankhullar-pixel/declared-vs-measured
