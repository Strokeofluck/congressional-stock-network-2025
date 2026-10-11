# Specific textbook readings beside their actual application.
v1_course_link <- function(label, page) tags$a(label,
 href=paste0('https://courseweb.site/dsa495-2026/',page),
 target='_blank',rel='noopener noreferrer')
v1_class_readings <- list(
 c('Reproducibility','01','Module 1 · Reproducible workflows','August 17, 2026',
   'Run render.R and verify_v1.py; retain the frozen input and source commits. This adapts the course’s reproducible-workflow principle. The renderer uses R Markdown, not a Colab notebook.'),
 c('Validation and error review','05','Module 5 · Evaluation and errors','September 21, 2026',
   'Inspect duplicate rows, ticker aliases, roster boundaries and committee-date mismatches against source evidence. This adapts error review to data and network checks; classifier accuracy, precision and recall are not calculated here.'),
 c('Claims linked to evidence','07','Module 7 · Source grounding','October 5, 2026',
   'Use original filing links, the Block ticker announcement and exact textbook sections to check each claim. This applies a grounding principle; the project does not implement retrieval-augmented generation (RAG).'),
 c('Compare changes consistently','08','Module 8 · Evaluation and improvement','October 12, 2026 · planned as of October 11',
   'Use the same frozen extract when comparing versions. Independent checks separate numerical corrections from display changes. This is a connection to planned evaluation material, not a completed RAG evaluation.'),
 c('Explain findings and limits','12','Module 12 · Project presentations','November 30, 2026 · planned as of October 11',
   'Present the question, data, workflow, validation, findings and limitations. See the review path below. Treat annual shared purchases as descriptive overlap, with no claim of coordinated trading.')
)
v1_class_connections <- tags$section(id='classConnections',
 tags$h2('Class connections: DSA 495 · Fall 2026'),
 tags$p('DSA 495 teaches text analysis. These connections use its published workflow, evaluation and presentation principles; the network formulas remain tied to the SNA textbook. ',
   v1_course_link('Class materials','materials.html#12'), ' and ',
   v1_course_link('class schedule','schedule.html'),
   ' were checked October 11, 2026. Dates are scheduled sessions, not confirmation that a lecture occurred. These links identify modules, not unverified slide numbers or recording timestamps.'),
 tags$div(class='method-table-wrap',tags$table(class='method-table',
   tags$thead(tags$tr(tags$th('Project method'),tags$th('Class material and scheduled date'),tags$th('Connection and scope'))),
   tags$tbody(lapply(v1_class_readings,function(x)tags$tr(
     tags$td(x[1]),tags$td(v1_course_link(x[3],paste0('materials.html#',x[2])),tags$br(),x[4]),tags$td(x[5])))))),
 tags$h3('Review path for Module 12'),
 tags$ol(
   tags$li('Question and data — Open About. Explain that the extract covers accepted 2025 House stock purchases, not complete trading or current holdings.'),
   tags$li('Workflow — Use the textbook table below to explain binary member–stock affiliations, the two-member display rule and the member projection.'),
   tags$li('Evidence — Open Compare members. Show raw shared-stock counts beside Jaccard, include isolates and explain descriptive party mixing. Use validation/ and original filings to review the calculations and unresolved records.'),
   tags$li('Limitations — Explain missing ownership and amendment identifiers, uncertain duplicates, snapshot timing and unverified filing coverage. Graph proximity and overlap do not establish influence or misconduct.')
 ),
 tags$p(v1_course_link('Module 12 presentation guidance','materials.html#12'), ' · ',
   v1_course_link('Course project guidance','project.html'),
   '. The course project asks for a Python text-analysis workflow from unstructured text. This repository currently analyzes a structured extract with R and independent Python checks; these references do not establish that course-project requirement.')
)
v1_readings <- list(
 c('Affiliation edges','Chapter 2 · §2.0.1 Networks as edgelists','networks.html#networks-as-edgelists','Distinct reporting member–stock pairs form undirected affiliations. Purchase/year/accepted-ticker filters are project decisions.'),
 c('Two-mode network','Chapter 13 · §13.1 Two Mode Networks from Edgelists','two_mode.html#two-mode-networks-from-edgelists','Stocks-only has members and stocks. Committee and subcommittee layers add other relationship types.'),
 c('Binary matrix','Chapter 13 · §13.2 Two Mode Networks from Adjacency Matrices','two_mode.html#two-mode-networks-from-adjacency-matrices','B[i,t] is 1 when a member reported at least one accepted purchase. Repeats do not increase this tie.'),
 c('Binary / valued ties','Chapter 2 · §2.1.2 Binary vs. Valued Matrices','networks.html#binary-vs.-valued-matrices','Explore uses equal-width affiliations. Compare weights pairs by distinct shared stocks. Raw frequencies and amounts retain unresolved repeated rows.'),
 c('Degree','Chapter 13 · §13.4 Degree Centrality in Two Mode Networks','two_mode.html#degree-centrality-in-two-mode-networks','Member degree counts stocks; stock degree counts reporting members. Explore uses displayed stocks; Compare uses full lists. Degree does not measure influence.'),
 c('Projection','Chapter 13 · §13.6 Projecting One Mode Networks','two_mode.html#projecting-one-mode-networks','B times its transpose counts shared stocks. Zero the diagonal and retain isolates. This matrix code is equivalent to the book’s projection approach.'),
 c('Party color','Chapter 3 · §3.5 Visualizaing Node Attributes','network_viz.html#visualizaing-node-attributes','Color displays party as a categorical attribute; it does not establish clustering. “Visualizaing” is the published title/anchor.'),
 c('Party mixing','Chapter 8 · §8.1 Estimating assortativity','assortitivity.html#estimating-assortativity','Nominal assortativity uses all connected member pairs. Weighted mixing is a project sensitivity calculation. Neither is a significance test; zero means the endpoint baseline.'),
 c('Layout','Chapter 4 · §4.1 Force Directed Layouts','graph_layouts.html#force-directed-layouts','ForceAtlas2 arranges the graph for exploration. Screen distance is not a similarity measure. Physics stops after stabilization.'),
 c('Interactivity','Appendix B · §B.3 Interactive Visualization with visNetwork','interact_vis.html#interactive-visualization-with-visnetwork','visNetwork supplies interactive networks. Search, inspectors, exports and deferred loading are project interface features.'),
 c('Dates: background only','Chapter 15 · Dynamic Networks','dynamic.html','Purchases are aggregated annually. Dated committee matching does not implement dynamic SNA. Communities, brokerage and time-window similarity remain future work.')
)
v1_methodology_guide <- tags$div(
 v1_class_connections,
 tags$h2('Reading guide: method → textbook → application'),
 tags$p('Start with Chapter 13: Two Mode Networks, then Chapter 8: Assortativity. Other readings are Chapter 2: What is a Network?, Chapter 3: Visualizing Networks, Chapter 4: Graph Layouts, and Appendix B: Interactive Network Visualization. Links open the exact section. The book explains methods; it does not certify the scraped input or completeness.'),
 tags$div(class='method-table-wrap', tags$table(class='method-table',
   tags$thead(tags$tr(tags$th('Method'),tags$th('Textbook reading'),tags$th('Applied here'))),
   tags$tbody(lapply(v1_readings,function(x)tags$tr(tags$td(x[1]),tags$td(v1_book(x[2],x[3])),tags$td(x[4])))))),
 tags$h2('Stock identity and the two-member rule'),
 tags$p(sprintf('The source retains %s ticker strings. A verified Block Class A alias SQ → XYZ leaves %s analysis symbols. Original symbols and PDF links remain visible. Other symbol histories and share classes still need upstream review.',n_distinct(purchases_2025_all$reported_ticker),n_distinct(purchases_2025_all$ticker))),
 tags$p(tags$a('Block’s announcement: ticker change effective January 21, 2025',href='https://investors.block.xyz/investor-news/news-details/2025/Block-Announces-Ticker-Symbol-Change-to-XYZ-To-Report-Fourth-Quarter-Results/default.aspx',target='_blank',rel='noopener noreferrer')),
 tags$p(sprintf('Explore keeps %s shared stocks and %s reporting members. All %s accepted purchasers remain in Compare members; %s have no shared stock. A single-member stock cannot create a projected pair tie. The stock cutoff and the pair-overlap threshold are different display rules.',length(keep_tickers),n_distinct(purchases_network$politician_clean),nrow(v1_members),v1_isolates)),
 tags$h2('Similarity, amounts and institutional timing'),
 tags$p('Raw overlap grows with broad purchasing lists and popular stocks. Jaccard divides shared stocks by the union of both full accepted lists. This added normalization adjusts for list size; it is not a significance test and does not control for stock popularity, ownership or purchase dates.'),
 tags$p(sprintf('%s excess identical rows remain unresolved because owner, amendment linkage and original row identity are absent. Equal-width Explore ties avoid encoding uncertain frequency as stronger evidence. Dollar summaries sum retained bounds and may contain repeats; they are not verified personal spending.',v1_duplicate_excess)),
 tags$p('Committee snapshots are proxies. Each inspector record shows snapshot age; January 3–20 uses January 21, a future approximation. Membership changes between snapshots can be missed. Annual overlap and committee association do not establish coordination, influence or misconduct.'),
 tags$h2('Population and reproducibility'),
 tags$p('55 is the accepted-extract population, not all House traders. Finding more purchasers requires reconciliation of original filings, amendments, rejected tickers, exclusions and parsing losses. No accepted purchase found does not mean no trading.'),
 tags$p('The steps below use shortened R excerpts. Complete executable code lives in the Rmd, v1-analysis.R and methodology-guide.R. verify_v1.py independently checks normalized identities, affiliations, all pairs, Jaccard, party mixing, roster boundaries and output content.')
)
v1_directory_rows <- lapply(seq_len(nrow(v1_members)), function(i) {
 x <- v1_members[i, ]
 tags$tr(class='v1-directory-row',
   tags$td(tags$button(type='button', class='nav-button v1-directory-member', `data-member`=x$id, x$id)),
   tags$td(x$party), tags$td(x$full_stock_degree), tags$td(x$shared_member_degree),
   tags$td(ifelse(x$shared_member_degree > 0, 'Included', 'Outside: no shared stock')))
})
v1_directory <- tags$div(tags$h2('All accepted reporting members'),
 tags$p('Find people outside the opening graph here. Counts use full accepted stock lists and the complete annual projection.'),
 tags$label('Filter directory ',tags$input(id='v1DirectoryFilter',type='search',placeholder='Member name')),
 tags$div(class='method-table-wrap',tags$table(class='method-table',
   tags$thead(tags$tr(tags$th('Member'),tags$th('Party'),tags$th('Distinct stocks'),tags$th('Connected members'),tags$th('Opening graph'))),
   tags$tbody(v1_directory_rows)))
)
