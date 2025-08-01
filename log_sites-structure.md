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

# Clearer Structure Notes

## EA Games
- Container: `<div class="results results--listed ">`
- Post Structure (no internships atm, so using regular job post structure):
    ~~~html
<article class="article article--result article--non-toggle" id="article--1">
  <div class="article__header">
    <div class="article__header__text">
      <h3 class="article__header__text__title title title--04">
        <a class="link link_result" href="https://jobs.ea.com/en_US/careers/JobDetail/Development-Director-I/210016">
          Development Director Live Ops (Temporary)
        </a>
      </h3>
      <div class="article__header__text__subtitle">
        <span class="list-item-location">Vancouver, Canada</span>
        <span class="separator">&nbsp;•&nbsp;</span>
        <span class="list-item-jobPostingLocation">
          <span class="list-item-0">Edmonton, Canada</span>
        </span>
        <span class="separator">&nbsp;•&nbsp;</span>
        <span class="list-item-id">Role ID 210016</span>
        <span class="separator">&nbsp;•&nbsp;</span>
        <span class="list-item-workerType">Temporary Employee</span>
        <span class="separator">&nbsp;•&nbsp;</span>
        <span class="list-item-department">EA Studios - Full Circle</span>
      </div>
    </div>
  </div>
</article>
    ~~~

## IBM
- Container: `<div id="ibm-hits-wrapper" >`
- Post Structure:
    ~~~html
    <div id="ibm-hits-wrapper">
        <div class="bx--card-group__cards__row bx--row--condensed">
            <a id="search-result-e48f5dc559ff86fc59729663e89d0be15d72f348ea0a372115f01ffc261b8527-dp0" href="https://ibmglobal.avature.net/en_US/careers/JobDetail?jobId=48579&amp;source=WEB_Search_NA" tabindex="0" class="bx--card-group__card">
                <div class="bx--tile bx--card bx--card-link bx--card__CTA bx--card__CardCTA" data-autoid="dds--card">
                    <div class="bx--card__wrapper">
                        <div class="bx--card__content">
                            <div class="bx--card__eyebrow" style="height: 18px;">Cloud</div>
                            <div class="bx--card__heading" style="height: 96px;">2026 Returning Intern</div>
                            <div class="ibm--card__inner" style="height: 82px;"><div class="bx--card__copy"><div class="ibm--card__copy__inner">Internship<br>Multiple Cities</div>
                            </div>
                            </div>
                            <div class="bx--card__footer bx--card__footer__copy" style="height: 20px;">
                            <span class="bx--card__cta__copy"></span>
                            <span size="20">
      </span></div></div></div></div></a>
        </div>
    </div>
    ~~~

## Hitmarker
- Container: `<div class="space-y-3">`
- Structure:
    ~~~html
    <a href="https://hitmarker.net/jobs/ubisoft-us-communications-intern-1480874">
    <div>
        <div>
            <div>
                <div></div>
                <span class="font-bold">US
                    Communications Intern</span>
            </div>
            <div>
                <div>
                    <span class="truncate">Ubisoft</span>
                </div>
                <div>
                    <span></span>
                    <span class="truncate">San Francisco, CA,
                        USA</span>
                </div>
                <div>
                    <span class="truncate"><!---->Internship</span>
                </div>
                <div>
                    <span class="truncate">Entry (0–1
                        years)
                    </span>
                </div><!---->
                <div>
                    <span data-datetime="2025-07-30T10:54:21.000Z" data-hide-time="" class="truncate"
                        data-formatted="">14 hours ago</span>
                </div>
            </div>
        </div>
        <div>
        </div>
    </div>
</a>
    ~~~

## Epic Games
- Container: `div class="JobsViewstyles__FilteredResults-sc-xcdagw-2 bsBnOO"`
- Structure: No posts atm

## Riot Games
- Container: `div class="job-list__body ..."`
- Structure: No posts atm
    ~~~html
    <ul class="job-list__body list--unstyled">
        <p class="copy text-center job-list__notice">No jobs found for your current filters.
        </p>
    </ul>
    ~~~

## Abbott Health Care
- Container: `<ul data-ph-at-id="jobs-list" ph-role="data.bind:jobResults" data-ph-id="ph-default-1620733883672-ph-search-results-v20rewup-lKf84R" class="au-target" au-target-id="59" data-ph-at-widget-data-count="10" role="list">`
- Paging Notes:
    - Page 1: https://www.jobs.abbott/us/en/search-results?rk=l-early-careers&sortBy=Most%20relevant
    - Page 2: https://www.jobs.abbott/us/en/search-results?from=10&s=1&rk=l-early-careers
- Structure:
    ~~~html
    <li class="jobs-list-item" data-ph-at-id="jobs-list-item">
    <div class="information">
        <a data-ph-at-id="job-link"
        href="https://www.jobs.abbott/us/en/job/31094633/2025-Spring-Engineering-Co-op">
        <div class="job-title">
            <span>2025 Spring Engineering Co-op</span>
        </div>
        </a>
        <span class="job-location">
        Available in 3 locations
        </span>
        <span class="job-category">
        Business Support
        </span>
        <p class="job-description" data-ph-at-id="jobdescription-text">
        Electrical Engineering. Computer Science and Engineering...
        </p>
    </div>
    </li>
    ~~~

## Zenimax Games
- Container: `<div class="job-listings">`
- Structure:
    ~~~html
        <a href="/requisitions/view/3288" aria-label="World Designer - Design - Arkane Studios - France " class="job-link">
        <div class="job-row">
            <div tabindex="0" class="job-title">World Designer</div>
            <div tabindex="0" class="job-department pl-md-3">Design</div>
            <div tabindex="0" class="job-department pl-md-3">
                <div>Lyon, FR</div>
            </div>
            <div tabindex="0" class="job-location pl-md-3">Arkane Studios - France </div>
        </div>
    </a>
    ~~~

## Sony
- Container: `<ul class="results-list front" data-testid="jobs-list-only_jobs-list">`
- Paging info:
    - Page 1: https://careers.playstation.com/early-careers?filter%5Bcountry%5D%5B0%5D=United%20States&filter%5Bcountry%5D%5B1%5D=United%20States%20of%20America&filter%5Bcountry%5D%5B2%5D=Canada
    - Page 2: https://careers.playstation.com/early-careers?filter%5Bcountry%5D%5B0%5D=United%20States&filter%5Bcountry%5D%5B1%5D=United%20States%20of%20America&filter%5Bcountry%5D%5B2%5D=Canada&page_number=2
- Structure:
    ~~~html
    <li class="results-list__item" data-testid="jobs-list-only_jobs-list_item">
    <a class="results-list__item-title--link"
        href="/ai-systems-engineer/job/5592075004">
        AI Systems Engineer
    </a>

    <span class="results-list__item-street--label">
        Aliso Viejo, California
    </span>

    <a class="results-list__item-apply"
        href="/ai-systems-engineer/job/5592075004">
        Apply Now
    </a>
    </li>
    ~~~

## Insomniac Games
- Container: `<div class="jobs-container">`
- Structure:
    ~~~html
    <a class="job-row regular" href="https://job-boards.greenhouse.io/insomniac/jobs/5584365004" target="_blank" aria-label="Job Link">
    <div data-aos="fade-up" class="job-cell position aos-init aos-animate">Character Artist
    </div>
    <div data-aos="fade-up" class="job-cell location aos-init aos-animate">Contract
    </div>
    <div data-aos="fade-up" class="job-cell department aos-init aos-animate">Art
    </div>
    <div data-aos="fade-up" class="job-cell mobile-department-location aos-init aos-animate">Contract&nbsp;&nbsp;|&nbsp;&nbsp;Art
    </div>
    </a>
    ~~~

## Microsoft
- Container: `div class="ms-List-page"`
- Structure:
    ~~~html
    <div class="ms-List-cell" role="listitem">
  <!-- Job title (link usually present on parent or “See details” anchor) -->
    <h2 class="MZGzlrn8gfgSs8TZHhv2">
        Software Engineer II – AI Platform Development (Azure PostgreSQL)
    </h2>
    <span class="posted-date">1 day ago</span>
    <span class="job-location">
        Redmond, Washington, United States
    </span>
    <span class="work-flexibility">
        Up to 50% work from home
    </span>
    <a class="seeDetailsLink-547" href="{JOB_DETAILS_URL}">
        See details
    </a>
    </div>
    ~~~

## Amazon
- Container: `ul class="jobs-module_root__gY8Hp"`
- Pagining info: Paging does not seemingly have an impact on the URL
- Structure:
    ~~~html
    <li>
    <a class="header-module_title__9-W3R"
        href="/jobs/3048521" target="_blank">
        2026 Applied Science Internship – Gen AI &amp; Large Language Models
    </a>
    <span class="metadatum-module_text__ncKFr">
        Seattle, WA, USA
    </span>
    <span class="metadatum-module_text__ncKFr">
        Updated: 7/30/2025
    </span>
    <div class="job-card-module_content__8sS0J">
        Revolutionize the Future of AI at the Frontier of Applied Science…
    </div>
    <button class="footer-module_expando__1hi-H">
        Read more
    </button>
    </li>
    ~~~

## NVIDIA & Intel & Activision
- Container: `<ul aria-label="Page 1 of 1" role="list">`
    - NOTE: There are multiple `ul role="list"` on the page
- Paging Info: Unknown (only one page)
- Structure:
    ~~~html
    <li class="css-1q2dra3">
    <a class="css-19uc56f"
        href="/en-US/NVIDIAExternalCareerSite/job/Canada-Toronto/Software-Engineering-Intern--Robotics-Perception-Research---Fall-2025_JR1997029">
        Software Engineering Intern, Robotics Perception Research – Fall 2025
    </a>

    <span class="job-location">Canada, Toronto</span>
    <span class="posted-date">Posted 5 Days Ago</span>
    <span class="job-id">JR1997029</span>
    </li>
    ~~~

## AMD
- Container: `<mat-accordion _ngcontent-ndu-c163="" class="mat-accordion cards">`
- Paging info: Included in base URL already
- Structure:
    ~~~html
    <mat-expansion-panel class="search-result-item">
    <a class="job-title-link" href="/careers-home/jobs/66134?lang=en-us">
        IT Intern
    </a>
    <span class="req-id">Req ID: 66134</span>
    <span class="location label-value">
        Penang, MY – GBS by the Sea
    </span>
    <span class="categories label-value">
        Student / Intern / Temp
    </span>
    <a class="apply-button"
        href="https://globalcampus-amd.icims.com/jobs/66134/login">
        Apply Now
    </a>
    </mat-expansion-panel>
    ~~~

## Honeywell
- Container: `ul class="jobs-list__list"`
- Structure:
    ~~~html
    <li data-qa="searchResultItem">
    <a class="job-list-item__link"
        href="https://careers.honeywell.com/en/sites/Honeywell/job/109207/">
        Sr Software Engineer – Cloud Solutions
    </a>
    <span class="location">
        Pittsford, NY, United States (Hybrid)
    </span>
    <span class="posted-date">07/28/2025</span>
    <span class="req-id">109207</span>
    <span class="job-tag">Trending</span>
    </li>
    ~~~

## Obsidian Games
- Container: `<div class="job-filter">`
- Structure:
    ~~~html
    <div class="job-filter">
        <span class="job-filter-item job-open-positions">
        Unfortunately, there are no open summer internship positions. Check back soon!
    </span>
        </div>
    ~~~