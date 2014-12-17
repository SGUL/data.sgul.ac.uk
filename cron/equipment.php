<?php

$csv = <<<CSV
Type,Name,Description,Contact Name,Contact Email,Secondary Contact Name,Secondary Contact Email,Site Location,Web Address
facility,Clinical Research Facility,"The St George’s Clinical Research Facility, run jointly with our partner St George’s Healthcare NHS Trust, is a custom-built centre that provides physical facilities and nursing and administrative support to facilitate high-quality research programmes and clinical trials. The facility is open for use by university and trust staff, as well as students and other organisations.",Giuseppe Sollazzo,gsollazz@sgul.ac.uk,Open Data Team,opendata@sgul.ac.uk,Tooting,www.sgul.ac.uk
facility,"Situated on site at St George’s, the Image Resource Facility (IRF) provides state-of-the-art advanced bio-imaging technology. The facility works with our researchers, St George’s NHS Healthcare Trust staff and other academic institution’s including UCL, King’s College London and Kingston University.",Image Resource Facility,Giuseppe Sollazzo,gsollazz@sgul.ac.uk,Open Data Team,opendata@sgul.ac.uk,Tooting,http://www.irf.sgul.ac.uk/
facility,"The Medical Biomics Centre at St George’s is the world's first purpose-built clinical and biomedical research facility to combine genomics, transcriptomics and proteomics on a clinical site. It provides the technology to carry out out integrated analysis of the molecular basis of complex disease processes. The state-of-the-art facilities allow researchers to assist in the development of novel diagnostics, in the identification of new therapeutic targets, and in increasing our understanding of the pathophysiology of disease.",Medical Biomics Centre,Giuseppe Sollazzo,gsollazz@sgul.ac.uk,Open Data Team,opendata@sgul.ac.uk,Tooting,http://www.biomics.org.uk/
CSV;

$csvfile = "./cron/output/equipment.csv";
$f_csv = fopen($csvfile, 'w') or die("can't open file");
fwrite($f_csv, $csv);
fclose($f_csv);
?>