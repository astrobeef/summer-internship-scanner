# Job Posts Structure
1. Found in `div class="section__content__results"` on EA
    - No jobs atm
2. Found in `div id="ibm-hits-wrapper""` on IBM. More specifically `div class="bx--card-group__cards__row bx--row--condensed"`
    - Found in `div class="bx--card-group__cards__col"` on IBM. Nested one level deeper is a link to the post structured like: `a id="search-result-e48f5dc559ff86fc59729663e89d0be15d72f348ea0a372115f01ffc261b8527-dp0"`. Further nested within the link (odd) is brief info about the job.
3. Found in `div class="space-y-3"` on Hitmarker.
    - Found in `div class="flex-auto min-w-0 p-4"` on Hitmarker. No obvious specific classes/ids
4. Found in `div class="JobsViewstyles__FilteredResults-sc-xcdagw-2 bsBnOO"` on Epic Games.
    - No jobs atm
5. Found in `div class="job-list__body ..."` on Riot Games
    - No jobs atm
6. Found in `div class="_search-jobs-block_imvtw_177 ..."` on Activision. Deeper element with `role=list` contains posts directly: `div class="phw-grid-1 phw-content-block phw-content-block-top-space phw-grid phw-grid-lg-1 _job-list_bqb3j_19 phw-mt-0"`
    - Found in `div class="phw-card-block ..." data-ph-at-id="jobs-list"`
7. Found in `ul class="au-target" data-ph-at-id="jobs-list"` on Abbott.
    - Found in `li class="jobs-list-item" data-ph-at-id="jobs-list-item"`
8. Found in `div class="job-listings"` on ZeniMax.
    - Found in `a class="job-link"` with nested brief information. The only nested info listed which might contain intern (though none do atm) would be `div class="job-title"`.
9. Found in `ul class="results-list front" data-testid="jobs-list-only_jobs-list"` on Sony (PlayStation).
    - Found in `li class="results-list__item" data-testid="jobs-list-only_jobs-list_item"`. Info nested within, including link to full job description.
10. Found in `div class="jobs-container"` on Insomniac Games.
    - Found in `a class="job-row regular"`. Brief info nested under link: position, employee type, department.
11. Found in `div class="ms-List-page"` on Microsoft.
    - Found in `div class="ms-List-cell" role="listitem" data-list-index="0" data-automationid="ListCell"`. Indexes are included for each.
12. Found in `ul class="jobs-module_root__gY8Hp"` on Amazon.
    - Found in `li`. Deeper div contains data: `div class="job-card-module_root__QYXVA"`
13. Found in `ul role="list"` on NVIDIA.
    - Found in `li class="css-1q2dra3"`. This happens in other post formats too, but information is deeply nested within empty divs. Posts seem to always include "intern" and time of internship. Ex. Fall 2025
14. Found in `ul role="list"` on Intel (same structure as NVIDIA since it's through Workday)
15. Found in `div class="job-results-container"` on AMD. Deeper container: `mat-accordion class="mat-accordion cards"`.
    - Found in `mat-expansion-panel class="search-result-item ,,,"`. Found deeper in `span class="mat-content ng-tns-c75-15"`
16. Found in `ul class="jobs-list__list"` on Honeywell.
    - Found in `li data-qa="searchResultItem"`. Link found deeper in `a class="job-list-item__link"`. Info found deeper (not nested in the link but sibling to it): `div class="job-list-item__content"`
17. Found in `section id="open-positions"` on Obsidian Games. Found deeper in `span class="job-filter-item job-open-positions"`.
    - No open atm. The span contains a message saying such, so the span may only exist because there are no results.
18. Not sure if Respawn Games displays internships on the given link. As of now, I cannot find any links to internship pages and this page itself seems out of date.