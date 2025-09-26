# On on page entry, check for login popup modal

~~~HTML
<button class="sign-in-modal__outlet-btn cursor-pointer btn-md btn-primary btn-secondary" data-tracking-client-ingraph="" data-tracking-control-name="public_jobs_contextual-sign-in-modal_sign-in-modal_outlet-button" data-modal="base-sign-in-modal">
<!---->              Sign in
          </button>
~~~

# On login page, fill form

~~~HTML

<form data-id="sign-in-form" action="https://www.linkedin.com/uas/login-submit" method="post" novalidate="" class="mt-1.5 mb-2">
      <input name="loginCsrfParam" value="9d1ca7b1-11f8-41f7-8fd7-38054628bea9" type="hidden">

      <div class="flex flex-col">
        
    <div class="mt-1.5" data-js-module-id="guest-input">
      <div class="flex flex-col">
        <label class="input-label mb-1" for="base-sign-in-modal_session_key">
          Email or phone
        </label>
        <div class="text-input flex">
          <input class="text-color-text font-sans text-md outline-0 bg-color-transparent w-full" autocomplete="username" id="base-sign-in-modal_session_key" name="session_key" required="" data-tracking-control-name="public_jobs_contextual-sign-in-modal_sign-in-modal_sign-in-session-key" data-tracking-client-ingraph="" type="text">
          
        </div>
      </div>

      <p class="input-helper mt-1.5" for="base-sign-in-modal_session_key" role="alert" data-js-module-id="guest-input__message"></p>
    </div>
  

        
    <div class="mt-1.5" data-js-module-id="guest-input">
      <div class="flex flex-col">
        <label class="input-label mb-1" for="base-sign-in-modal_session_password">
          Password
        </label>
        <div class="text-input flex">
          <input class="text-color-text font-sans text-md outline-0 bg-color-transparent w-full" autocomplete="current-password" id="base-sign-in-modal_session_password" name="session_password" required="" data-tracking-control-name="public_jobs_contextual-sign-in-modal_sign-in-modal_sign-in-password" data-tracking-client-ingraph="" type="password">
          
            <button aria-live="assertive" aria-relevant="text" data-id="sign-in-form__password-visibility-toggle" class="font-sans text-md font-bold text-color-action z-10 ml-[12px] hover:cursor-pointer" aria-label="Show your LinkedIn password" data-tracking-control-name="public_jobs_contextual-sign-in-modal_sign-in-modal_sign-in-password-visibility-toggle-btn" type="button">Show</button>
          
        </div>
      </div>

      <p class="input-helper mt-1.5" for="base-sign-in-modal_session_password" role="alert" data-js-module-id="guest-input__message"></p>
    </div>
  

        <input name="session_redirect" value="https://www.linkedin.com/jobs/search/?currentJobId=4295730239&amp;distance=25&amp;f_E=1&amp;f_I=109%2C4&amp;f_WT=1%2C3&amp;geoId=103644278&amp;keywords=programmer" type="hidden">

<!---->      </div>

      <div data-id="sign-in-form__footer" class="flex justify-between
          sign-in-form__footer--full-width">
        <a data-id="sign-in-form__forgot-password" class="font-sans text-md font-bold link leading-regular
            sign-in-form__forgot-password--full-width" href="https://www.linkedin.com/uas/request-password-reset?trk=public_jobs_contextual-sign-in-modal_sign-in-modal_forgot_password" data-tracking-control-name="public_jobs_contextual-sign-in-modal_sign-in-modal_forgot_password" data-tracking-will-navigate="">Forgot password?</a>

<!---->
        <input name="trk" value="public_jobs_contextual-sign-in-modal_sign-in-modal_sign-in-submit" type="hidden">
        <button class="btn-md btn-primary flex-shrink-0 cursor-pointer
            sign-in-form__submit-btn--full-width" data-id="sign-in-form__submit-btn" data-tracking-control-name="public_jobs_contextual-sign-in-modal_sign-in-modal_sign-in-submit-btn" data-tracking-client-ingraph="" data-tracking-litms="" type="submit">
          Sign in
        </button>
      </div>
          <div class="sign-in-form__divider left-right-divider pt-2 pb-3">
            <p class="sign-in-form__divider-text font-sans text-sm text-color-text px-2">
              or
            </p>
          </div>
    <input type="hidden" name="controlId" value="d_jobs_guest_search-public_jobs_contextual-sign-in-modal_sign-in-modal_sign-in-submit-btn"><input type="hidden" name="pageInstance" value="urn:li:page:d_jobs_guest_search_jsbeacon;GPrUaXa7SweNpKNoC3jEtw=="></form>

~~~

# On login page, submit

~~~HTML
<button class="btn-md btn-primary flex-shrink-0 cursor-pointer
            sign-in-form__submit-btn--full-width" data-id="sign-in-form__submit-btn" data-tracking-control-name="public_jobs_contextual-sign-in-modal_sign-in-modal_sign-in-submit-btn" data-tracking-client-ingraph="" data-tracking-litms="" type="submit">
          Sign in
        </button>
~~~

# On jobs page

Clickable div within right sidebar (some unnecessary details removed):
~~~HTML
<li id="ember208" class="ember-view   YuEraHenaoPPgKVBvBLVPgbiHiPUGZEoNDM occludable-update p0 relative scaffold-layout__list-item" data-occludable-job-id="4296168115">
            
                  
    <div>
      
    <div data-job-id="4296168115" class="display-flex job-card-container relative job-card-list
        job-card-container--clickable
        
        job-card-list--underline-title-on-hover jobs-search-results-list__list-item--active jobs-search-two-pane__job-card-container--viewport-tracking-1" aria-current="page">

      <div>
        <div id="ember209" class="job-card-list__entity-lockup  artdeco-entity-lockup artdeco-entity-lockup--size-4 ember-view">
            

          

        
</div>

            
          
    
  
      
            
          
      </div>
      
    </div>
  
    </div>
  
                              
        </li>
~~~

Scrollable job listings:
~~~HTML
<div class="TqHDUxArccTqdKuLKLEVvZooySmcJTQuUE">
        <div id="jobs-search-results-footer">

    <div class="jobs-search-pagination jobs-search-results-list__pagination p4">
      <p class="jobs-search-pagination__page-state">
        Page 1 of 25
      </p>
        <button aria-label="View next page" id="ember291" class="artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view jobs-search-pagination__button jobs-search-pagination__button--next" type="button"> 
<span class="artdeco-button__text">
    Next
</span></button>
    </div>
        </div>
      </div>
~~~

Job Details:
~~~HTML
<div class="jobs-search__job-details--wrapper">        
      <div aria-label="Software Engineer - Internship - Up to $18,000 p/m + Benefits - Quant Fund " class="jobs-search__job-details--container
          " data-job-details-events-trigger="">
        
      <div class="jobs-semantic-search-job-details-wrapper" tabindex="0">        
    <div class="job-view-layout jobs-details">
      <div>
        <div class="jobs-details__main-content jobs-details__main-content--single-pane full-width
            ">
          <div>
    <div class="t-14" tabindex="-1">
<!---->      <div class="relative
          job-details-jobs-unified-top-card__container--two-pane">
        <div>
          <div class="display-flex align-items-center">
            <div class="display-flex align-items-center flex-1">
                <div class="job-details-jobs-unified-top-card__company-name" dir="ltr">
                  <a class="hVejVlSQqoNbByOzBeuSnvvNKvctCBcqBJZew " target="_self" tabindex="0" href="https://www.linkedin.com/company/hunter-bond/life" data-test-app-aware-link=""><!---->Hunter Bond<!----></a>
                </div>
            </div>
          </div>
  
            </div>
          </div>

          <div class="display-flex justify-space-between flex-wrap mt2">
            <div class="t-24 job-details-jobs-unified-top-card__job-title">
              <h1 class="t-24 t-bold inline">
                <a href="/jobs/view/4302668926/?alternateChannel=search&amp;eBP=CwEAAAGZgzBskGuku5NFiqIu_b6EW1lCW91OAjLseHPJd7yHovaLB9kXXTQv5592gmwzLZNWiqYAEesSBdl7xp7T0_edqvC3suV160tQSVxtRjE4_aFATZN8bZDZu4e90Zl2G74qd_GErOF9C23ecAmRwESqvKZXoV7l78F1XdnbVGh2yFSyNVBRjTmM2EGbLT8b-iQr5gAEW4gx5dCYZtSJnQbQZP5XvVUNfM0Bj4UR1NbWqpQLxx2K75X9nYN_--HkBYw2r0ei6ZFt36B5ESC8bzDxO0PBCUFrRTCXDQ5GYn0naLdetzARXySdTPYLnm4BB4XBbzkeo4xrPhsF5QAre8Yp7ciuKfLqhB21CXlqLRBk-7n4mYsZOGtY0zggtHUWwstPjIQPAIN29FzRviaVcyKjvV5C8o-ar3kSSSaOWmXt9siCcutCOxc573ZZcdLRI5K7MexaWhVO42TDfuPFDseGM4_1QfxOydla&amp;refId=tJ6Q6bOTwbj8ZGX8CMx5aQ%3D%3D&amp;trackingId=%2BE%2F%2BwRAajw%2FNRh13iqcp4A%3D%3D&amp;trk=d_flagship3_search_srp_jobs" id="ember56" class="ember-view">Software Engineer - Internship - Up to $18,000 p/m + Benefits - Quant Fund</a>
              </h1>
              <span class="white-space-nowrap">&nbsp;

              </div>

<!---->
          <div class="job-details-jobs-unified-top-card__primary-description-container">
              <div class="t-black--light mt2 job-details-jobs-unified-top-card__tertiary-description-container">
                <span dir="ltr"><span class="tvm__text tvm__text--low-emphasis"><!---->New York, United States<!----></span><span class="tvm__text tvm__text--low-emphasis"><span class="white-space-pre"> </span>·<span class="white-space-pre"> </span></span><span class="tvm__text tvm__text--low-emphasis"><span><!---->2 days ago<!----></span></span><span class="tvm__text tvm__text--low-emphasis"><span class="white-space-pre"> </span>·<span class="white-space-pre"> </span></span><span class="tvm__text tvm__text--low-emphasis"><!---->Over 100 applicants<!----></span><p><span class="tvm__text tvm__text--low-emphasis"><!---->Promoted by hirer<!----></span><span class="tvm__text tvm__text--low-emphasis"><span class="white-space-pre"> </span>·<span class="white-space-pre"> </span></span><span class="tvm__text tvm__text--positive"><strong><!---->Actively reviewing applicants<!----></strong></span></p></span>
              </div>
          </div>

<!---->

<!---JOB PREFERENCES SUCH AS INTERNSHIP--->
      <div class="job-details-fit-level-preferences">
            <button tabindex="0" class="artdeco-button artdeco-button--secondary artdeco-button--muted" type="button">
              <span class="tvm__text tvm__text--low-emphasis"><strong><!---->$18K/yr<!----></strong></span>
            </button>
            <button tabindex="0" class="artdeco-button artdeco-button--secondary artdeco-button--muted" type="button">
              <span aria-hidden="true"><span class="tvm__text tvm__text--low-emphasis"><strong><li-icon aria-hidden="true" type="check" class="v-align-bottom" size="small"></li-icon><span class="white-space-pre"> </span>On-site<!----></strong></span></span><span class="visually-hidden"><!---->Matches your job preferences, workplace type is On-site.<!----></span>
            </button>
            <button tabindex="0" class="artdeco-button artdeco-button--secondary artdeco-button--muted" type="button">
              <span aria-hidden="true"><span class="tvm__text tvm__text--low-emphasis"><strong><li-icon aria-hidden="true" type="check" class="v-align-bottom" size="small"></li-icon><span class="white-space-pre"> </span>Internship<!----></strong></span></span><span class="visually-hidden"><!---->Matches your job preferences, job type is Internship.<!----></span>
            </button>
      </div>
<!---END OF JOB PREFERENCES SUCH AS INTERNSHIP--->
          <div class="mt4">
              <div class="display-flex">
                  
    <div class="jobs-s-apply jobs-s-apply--fadein inline-flex mr2">
        
    <div class="jobs-apply-button--top-card">
      <button aria-label="Easy Apply to Software Engineer - Internship - Up to $18,000 p/m + Benefits - Quant Fund  at Hunter Bond" id="jobs-apply-button-id" class="jobs-apply-button
         artdeco-button artdeco-button--3 artdeco-button--primary ember-view" data-job-id="4302668926" data-live-test-job-apply-button="">        


<span class="artdeco-button__text">
    Easy Apply
</span></button>
    </div>
          </div>
                  <span class="visibility-hidden"></span>

                    
    <button class="jobs-save-button
         artdeco-button artdeco-button--secondary artdeco-button--3" type="button">
        <span aria-hidden="true" class="jobs-save-button__text">
          Save
        </span>
        <span class="a11y-text">
          Save Software Engineer - Internship - Up to $18,000 p/m + Benefits - Quant Fund&nbsp;  at Hunter Bond
        </span>
    </button>
              </div>
              </div>
              </div>
              </div>
        <div class="job-details-jobs-unified-top-card__sticky-header
            job-details-jobs-unified-top-card__sticky-header--disabled">
          <div class="job-details-jobs-unified-top-card__title-container">
              <a data-control-id="+E/+wRAajw/NRh13iqcp4A==" href="/jobs/view/4302668926/?alternateChannel=search&amp;refId=tJ6Q6bOTwbj8ZGX8CMx5aQ%3D%3D&amp;trackingId=%2BE%2F%2BwRAajw%2FNRh13iqcp4A%3D%3D&amp;trk=d_flagship3_search_srp_jobs" id="ember59" class="ember-view">
                <h2 class="t-16 t-black t-bold truncate">
                  Software Engineer - Internship - Up to $18,000 p/m + Benefits - Quant Fund
                </h2>
              </a>
            <div class="t-14 truncate">
              Hunter Bond · New York, United States (On-site)
            </div>
          </div>
          <div class="job-details-jobs-unified-top-card__sticky-buttons-container">
              
    <div class="jobs-s-apply jobs-s-apply--fadein inline-flex mr2">
        
    <div class="jobs-apply-button--top-card">
      <button aria-label="Easy Apply to Software Engineer - Internship - Up to $18,000 p/m + Benefits - Quant Fund  at Hunter Bond" id="jobs-apply-button-id" class="jobs-apply-button
         artdeco-button artdeco-button--2 artdeco-button--primary ember-view" data-job-id="4302668926" data-live-test-job-apply-button="">


<span class="artdeco-button__text">
    Easy Apply
</span></button>
    </div>
  
          </div>
  

                
    <button class="jobs-save-button
         mr2 artdeco-button artdeco-button--2 artdeco-button--secondary" aria-expanded="false" type="button">
        <span aria-hidden="true" class="jobs-save-button__text">
          Save
        </span>
        <span class="a11y-text">
          Save Software Engineer - Internship - Up to $18,000 p/m + Benefits - Quant Fund&nbsp;  at Hunter Bond
        </span>
    </button>
        </div>
    </div>
  </div>  


<!--MEET THE HIRING TEAM-->
    <div class="job-details-module">
<!---->            
    <div class="job-details-people-who-can-help__section--two-pane artdeco-card ph5 pv4">
<!---->      <h2 class="text-heading-medium
          mb2">
        Meet the hiring team
      </h2>
      <div>
        

    <div class="display-flex align-items-center mt4">
      <a class="hVejVlSQqoNbByOzBeuSnvvNKvctCBcqBJZew " aria-label="View Harry Rubin’s verified profile graphic" href="https://www.linkedin.com/in/harry-rubin0" data-test-app-aware-link="">  
      </a>
      <div class="hirer-card__hirer-information">
        <a class="hVejVlSQqoNbByOzBeuSnvvNKvctCBcqBJZew " aria-label="View Harry Rubin’s verified profile" href="https://www.linkedin.com/in/harry-rubin0" data-test-app-aware-link="">
          <span class="t-black jobs-poster__name text-body-medium-bold" dir="ltr">
            <strong><!---->Harry Rubin<!----></strong><span class="white-space-pre"> </span><!----><!----><span class="tvm__text tvm__text--low-emphasis">
</span>
          </span>
        </a>
          <div class="hirer-card__connection-degree-container t-14 t-normal t-black--light">
            <div class="display-flex flex-row-reverse align-items-baseline">
              <span class="hirer-card__connection-degree" dir="ltr">
                <!---->3rd<!---->
              </span>
            </div>
          </div>

        <div class="linked-area flex-1">
          <div class="text-body-small t-black" dir="ltr">
            <!---->Quantitative Technology Headhunter @ Hunter Bond | London | New York | Montreal | Singapore |<!---->
          </div>
            <div class="t-12 hirer-card__job-poster" dir="ltr">
              <!---->Job poster<!---->
            </div>
<!---->        </div>
      </div>

      

    <div class="entry-point">          
        <button id="ember2533" class="artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view">
          <span class="artdeco-button__text">
              Message
          </span>
        </button>
    </div>
    </div>
    </div>
    </div>
    </div>
            
    <div class="jobs-box--fadein jobs-box--full-width jobs-box--with-cta-large jobs-description
        
        
        
         jobs-description--reformatted
        
         job-details-module">

<!---->
      <article class="jobs-description__container
          ">
        <div class="jobs-description__content jobs-description-content
            ">
          <div class="jobs-box__html-content
              ArJggGbBmTOCdXaQrLCdNEuKOlNyEGzBFlKSs
              t-14 t-normal
              jobs-description-content__text--stretch" id="job-details" tabindex="-1">
            <h2 class="text-heading-large">
              About the job
            </h2>

<!---->            <div class="mt4">
                <p dir="ltr">
                  <span><p><span><strong><!---->🎓Role:<!----></strong></span><span class="white-space-pre"> </span>Software Engineer<span class="white-space-pre"> </span><span><em><!---->Intern<!----></em></span></p></span><span><p><span><strong><!---->🏢Client<!----></strong></span><!---->: Quant Fund<!----></p></span><span><p><!---->💰<!----><span><strong><!---->Compensation:<span class="white-space-pre"> </span></strong></span><!---->Up to $18,000 p/m + Benefits<!----></p></span><span><p><!---->🕒<!----><span><strong><!---->Duration:<!----></strong></span><span class="white-space-pre"> </span>3–6 Months<!----></p></span><span><p><span><strong><!---->📍Location:<!----></strong></span><span class="white-space-pre"> </span>New York, NY<!----></p></span><span><p><span><br></span></p></span><span><p><span><strong><!---->Kickstart Your Career<!----></strong></span></p></span><span><p><!---->Just graduated or seeking an exciting internship? Join a leading global firm focused on innovation, with no legacy systems. Work in a fast-paced, intellectually stimulating environment with cutting-edge tech and mentorship from top engineers. Contribute to high-impact projects and shape the future of tech.<!----></p></span><span><p><span><br></span></p></span><span><p><span><strong><!---->What You’ll Be Doing<!----></strong></span></p></span><span><p><!---->🧠 Collaborate with clients to understand their challenges and develop AI-driven solutions.<!----></p></span><span><p><!---->📊 Build AI applications with computer vision, language models, and trading systems<!----></p></span><span><p><!---->🤝 Collaborate with top engineers to tackle complex challenges<!----></p></span><span><p><!---->🚀 Learn rapidly and grow within a firm that thrives on initiative<!----></p></span><span><p><span><br></span></p></span><span><p><span><strong><!---->What You Bring<!----></strong></span></p></span><span><p><!---->🎓 Degree in Mathematics, Computer Science, Physics, Engineering, or related STEM field<!----></p></span><span><p><!---->💻 Proficiency in at least one core programming language (Python, C++, Java, C#, KDB+/Q, etc.)<!----></p></span><span><p><!---->🔍 Analytical mindset with a passion for solving complex problems<!----></p></span><span><p><!---->⚡ Strong drive and a desire to learn in a fast-paced, high-stakes environment<!----></p></span><span><p><span><br></span></p></span><span><p><span><strong><!---->Why This Role?<!----></strong></span></p></span><span><p><!---->🌍 Work on greenfield projects from day one — your contributions have real impact<!----></p></span><span><p><!---->🧠 Collaborate with some of the brightest minds in both tech and finance<!----></p></span><span><p><!---->🛠 Access to top-of-the-line tools, systems, and infrastructure<!----></p></span><span><p><!---->📈 Unmatched career growth in a high-performance, meritocratic culture<!----></p></span><span><p><span><br></span></p></span><span><p><!---->Apply now or reach out to me directly:<span class="white-space-pre"> </span><span><strong><!---->hrubin@hunterbond.com<!----></strong></span></p></span>
                </p>
<!---->            </div>
          </div>
          <div class="jobs-description__details">
<!---->          </div>
        </div>
      </article>
<!---->    </div>
  
              <section class="artdeco-card job-details-module">
                
    <section class="jobs-company jobs-box--fadein mb4" data-view-name="job-details-about-company-module">
      <div class="jobs-company__box">
        <h2 class="text-heading-large">
          About the company
        </h2>

        <div class="display-flex align-items-center mt5">
          <div id="ember2522" class="artdeco-entity-lockup artdeco-entity-lockup--size-5 ember-view flex-grow-1">
            <div id="ember2523" class="artdeco-entity-lockup__image artdeco-entity-lockup__image--type-square ember-view" type="square">
              <a href="/company/hunter-bond/life/" id="ember2524" class="ember-view link-without-hover-state inline-block" data-view-name="job-details-about-company-logo-link">
                <img title="Hunter Bond" src="https://media.licdn.com/dms/image/v2/D4E0BAQE1Y_eqO9hb2g/company-logo_100_100/B4EZifBl3ZGoAY-/0/1755014651786/hunter_bond_logo?e=1761782400&amp;v=beta&amp;t=OErLRJJ37QWyOapQIAvMBQJESAIzcsi7QRPMXN7jOxo" alt="Hunter Bond company logo" id="ember2525" class="evi-image ember-view">
              </a>
            
</div>
            <div id="ember2526" class="artdeco-entity-lockup__content ember-view flex-grow-1">
              <div id="ember2527" class="artdeco-entity-lockup__title ember-view t-20">
                <a href="/company/hunter-bond/life/" id="ember2528" class="ember-view link-without-visited-state inline-block t-black" data-view-name="job-details-about-company-name-link">
                  Hunter Bond
                </a>
              
</div>
              <div id="ember2529" class="artdeco-entity-lockup__subtitle ember-view t-16">
                709,383 followers
              </div>
            </div>
          
</div>
          
    <button class="follow   artdeco-button artdeco-button--secondary ml5" aria-label="Follow" aria-pressed="false" type="button">
        <span aria-hidden="true">Follow</span>
    </button>
  
        </div>

        <div class="t-14 mt5">
          Staffing and Recruiting
            <span class="jobs-company__inline-information">
              11-50 employees
            </span>
            <span class="jobs-company__inline-information">
              91 on LinkedIn
            </span>
        </div>
        <p class="jobs-company__company-description text-body-small-open">
          
    <div class="SkPLIMvbQfLGwnSrpACNkxttKCckmlUdsXyVU
        inline-show-more-text--is-collapsed
        inline-show-more-text--is-collapsed-with-line-clamp
        
        
        
        " style="-webkit-line-clamp:3;" dir="ltr" tabindex="-1">

        Hunter Bond is a global firm specialising in the finance and technology recruitment sectors with the aim to provide a thorough, effective and transparent solution to their client and candidates needs.  Hunter Bond directors have 20 years experience specialising in financial and technology jobs. With this experience comes a desire to provide the best recruitment service. Integrity is delivered by Hunter Bond at its upmost. Clients and candidates alike will have transparency and dedication from start to finish. Founding Directors, Lee Ballen and Stephen Perkins both have successful careers with a strong track record working with the world's leading financial institutions.  Today they bring their passion, knowledge and work ethic to the forefront of their business.<br><br>Hunter Bond specialises in the following markets: <br><br>Big Data - Architecture, Business Analysis, Business Intelligence, Consultancy, Data Governance, Data Analysis, Hadoop, Project Management, Programming, Testing and Support. <br><br>Change, Tranformation &amp; Regulatory -  Change Management, Change Analysis, Change Co-Ordination, Project Management, PRINCE2, Agile, Waterfall, P3O, Six Sigma, Programme Management, Business Analysis, Business Transformation, Transition Management.<br><br>Consultancies - Information Security, Business Continuity Planning, Disaster Recovery, Programme Management, Performance Management, Management Information, Business Process Transformation, Customer Relationship Management, Supply Chain and Purchasing, Governance, Audit, Risk and Policy Implementation.<br><br>Finance - Advisory &amp; Strategy, Products Advisory, Monitoring &amp; Surveillance, Compliance Reviews, Disclosures, Shareholder Reporting, and<br>AML/Financial Crime. <br><br>Finance Technology - .NET, C#, C++, Java, Solution Architect, Windows, Linux, Networks &amp; Security, Business Analysis, Programme Manager, Change Analyst and Testing.<br><br>Risk - Market Risk, Credit Risk, Collateral Management, Liquidity Risk, CVA (Credit Value Adjustment) and Actuarial.
      
          <span class="inline-show-more-text__link-container-collapsed">
              <span>…</span>
            <button class="inline-show-more-text__button
                inline-show-more-text__button--light
                link" aria-expanded="false" role="button" type="button">
              show more
            </button>
          </span>

<!---->    </div>
  
        </p>

<!---->
            
  

<!---->      </div>
    </section>
  
              
</section>

<!----><!---->        </div>
      </div>

<!---->
<!---->
      
    <div id="ember65" class="ember-view"><!----></div>

    <div id="ember66" class="ember-view"><div id="ember67" class="ember-view"><!----></div></div>
  

      
  <div id="ember68" class="ember-view"><!----></div>


<!---->
<!---->
<!---->
      
    <div>
        
    <div id="ember69" class="ember-view"><!----></div>
  
    </div>
  

<!---->
<!----><!---->    </div>
  
      </div>
  
      </div>
  

      <!---->
    </div>
~~~
