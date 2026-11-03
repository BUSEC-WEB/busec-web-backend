BUSEC Blog PRD

# BUSEC Blog: Product Requirements Document

Bells University Student Editorial Committee (BUSEC) · Web Team · Draft v0.1 · October 2026

Owner: Demi, Web Dev Lead

## 1. Overview

BUSEC is the Bells University Student Editorial Committee. This project is a public website where BUSEC writers and journalists publish articles, poems, literature, and an e- magazine. The reference point is Zikoko, but for student journalism at Bells University.

The site also serves as BUSEC's home online: it explains what the committee stands for, how it promotes student journalism on campus, and who the people behind it are, including past executives.

## 2. Goals and success metrics

#### **Goals**

- Give BUSEC a permanent, branded home for student journalism at Bells University.

- Make it easy for non-technical journalists to write and edit, and for executives to review and publish.

- Make the e-magazine readable on any phone through a flipbook viewer.

- Build everything on BUSEC-owned accounts so the next tenure can take over without friction.

#### **Success metrics (to be confirmed by the committee)**

- Site live within 1 month of project start.

- At least one e-magazine issue and a starter set of articles published at launch.

- Pages load quickly on mobile data (target: main pages usable in under 3 seconds on a typical 4G connection).

- Newsletter signups tracked from launch.

- The next tenure can publish and manage content with no help from the original developers.

Page 1 of 9

BUSEC Blog PRD

## 3. Users and roles

|Role|Who|Can do|
|---|---|---|
|Reader|Students and the wider<br>public|Read content, browse the committee page,<br>subscribe to the newsletter. No sign-in<br>required.|
|Journalist|BUSEC writers|Create, write, and edit their content. Submit it<br>for review.|
|Executive|BUSEC executives|Everything a journalist can do, plus publish<br>content and delete content.|
|Site<br>admin|Web team (technical)|Manage accounts, roles, and site settings.|

**Open question:** can journalists edit each other's posts, or only their own? Recommended default: journalists edit only their own drafts; executives can edit anything.

## 4. Scope

### 4.1 MVP (month 1)

#### **Public site**

- **Landing page:** what BUSEC is, what it stands for as an editorial committee, and how it promotes student journalism at Bells University.

- **Featured posts section:** a small set of highlighted posts with a "read more" link.

- **Content pages:** articles, poems, and literature, each with its own listing and individual post page.

- **E-magazine:** issues viewable as a flipbook.

- **Meet the committee:** member profiles with a **filter by year** to see executives from previous tenures.

- **Newsletter subscription:** a form where readers enter their details.

#### **Staff side**

Login for journalists and executives.

- Rich text editor for writing and editing.

- Draft, submitted, and published statuses.

- Executives can publish and delete content.

- Media upload for images used in posts.

Page 2 of 9

BUSEC Blog PRD

### 4.2 Not in the MVP (candidates for later)

- Reader accounts and comments

- Full-text search (basic category browsing is enough for launch)

- Automated newsletter sending from the site

- Likes, shares counters, and reading analytics dashboards

- Dark mode and multiple languages

## 5. Functional requirements

### 5.1 Content

- Content types: **article** , **poem** , **literature** (for example short stories and essays), and **magazine issue** .

- Each piece has a title, author byline, category, cover image, body, status, and publish date.

- Poems and literature must preserve line breaks and spacing exactly as written. Featured posts are chosen by an executive (a "featured" flag on a post).

- Image credits are supported on each piece.

### 5.2 Editorial workflow

1. A journalist creates a draft and edits it.

2. The journalist submits it for review.

3. An executive reviews, edits if needed, and either publishes it or sends it back.

4. Published content appears on the public site.

5. Only executives can delete. Recommended: deletion is a soft delete, so removed content can be restored if it was a mistake.

### 5.3 E-magazine

- Each issue is uploaded as a PDF and shown in a flipbook viewer (page-turn style). It must work on phones, with a fallback download link for the PDF.

- Each issue has a cover, title, issue date, and a short description. An archive page lists past issues.

### 5.4 Committee page

Profiles include name, position, photo, and tenure year.

A year filter shows the executives of each tenure.

Page 3 of 9

BUSEC Blog PRD

- Executives can add and update members, so the site does not depend on developers each new tenure.

### 5.5 Newsletter

- A signup form (email required; name optional) on the landing page and footer. Confirmation message after signup, with duplicate and invalid email handling. Subscriber list stored securely and exportable by executives.

- Includes an unsubscribe path and a short consent statement.

- Sending the newsletter itself is done through a tool such as Brevo or MailerLite for the MVP, not built into the site.

## 6. Non-functional requirements

- **Mobile first:** most readers will be on phones with limited data. Compress and resize images, lazy-load media, and keep pages light.

- **Performance:** fast initial load and no heavy scripts on article pages.

- **SEO and sharing:** clean URLs, page titles, descriptions, and social preview images (Open Graph), since articles will be shared on WhatsApp and X.

- **Accessibility:** readable type, sufficient contrast, alt text on images, keyboard navigation.

- **Security:** hashed passwords, role-based permissions enforced on the backend (not just hidden in the interface), HTTPS, rate limiting on the signup form, and spam protection.

- **Reliability:** automated database backups and uptime monitoring.

- **Maintainability:** clear README, documented setup, and code that a student team can pick up in the next tenure.

- **Data protection:** subscriber data is handled according to the Nigeria Data Protection Act (consent, purpose, secure storage, and a way to unsubscribe).

## 7. Tech stack

**Decided:** Python backend, React frontend.

#### **Still to decide**

- **Python framework:** Django (with Django REST Framework) or FastAPI. Django comes with a built-in admin panel, authentication, and permissions, which covers much of the journalist and executive workflow and could save a lot of time within a one-month window. FastAPI is lighter but means building those parts yourselves.

Page 4 of 9

BUSEC Blog PRD

- **Database:** PostgreSQL is the usual choice.

- **Frontend tooling:** React with Tailwind CSS. Consider Next.js if SEO and fast first loads matter most, since plain client-side React is weaker for search and link previews.

- **Rich text editor:** for example TipTap or CKEditor.

- **Media storage:** a managed service such as Cloudinary rather than storing files on the server.

- **Flipbook library:** a free React flipbook library, or a hosted service such as Heyzine if budget allows.

- **Hosting:** see section 9.

## 8. Design and branding

- Design owners: Demi and Mayor.

- Needed before frontend build: logo and brand colors, typography, and wireframes for the landing page, article page, committee page, and e-magazine page.

- Tone: editorial and youthful, in the spirit of Zikoko but with BUSEC's own identity.

## 9. Costs

Prices below are indicative and change often, so each line must be checked on the provider's current pricing page before the budget is finalized.

|Item|What it is|Likely cost|
|---|---|---|
|Domain (busec.online,<br>Hostinger)|Web address|₦1,590 for the first term, then<br>₦55,290 on renewal|
|Backend hosting|Where the Python API runs|Free tiers exist (Render,<br>Railway, and similar) but may<br>sleep when idle, which slows<br>the first visit. A small paid plan<br>is usually more reliable.|
|Database|PostgreSQL|Often free at small scale<br>(Neon, Supabase, or bundled<br>with the host). Paid when<br>storage or usage grows.|
|Frontend hosting|The React site|Usually free (Vercel, Netlify,<br>Cloudflare Pages).|

Page 5 of 9

BUSEC Blog PRD

|Item|What it is|Likely cost|
|---|---|---|
|Media storage|Images and uploads|Cloudinary has a free tier.<br>Large e-magazine PDFs may<br>need separate file storage.|
|Newsletter tool|Collecting and sending to<br>subscribers|Brevo and MailerLite have<br>free tiers with sending limits.|
|Flipbook viewer|E-magazine display|Free if self-built with a library.<br>Hosted services are paid.|
|Email on the domain|For example<br><editorial@busec.online>|Optional. Extra cost or free<br>forwarding.|
|Monitoring and<br>backups|Uptime alerts, error tracking,<br>database backups|Mostly free tiers<br>(UptimeRobot, Sentry).<br>Backups may need a paid<br>database plan.|
|Analytics|Visitor stats|Free (Google Analytics, or<br>self-hosted Umami).|
|Payment method|Many of these bill in USD|A dollar-capable card is<br>needed, held by the<br>committee and not by one<br>person.|

#### **Notes**

- The domain renewal (₦55,290 a year) is the biggest predictable cost, and it is a jump from the first-term price. Put the renewal date on the handover checklist and agree who pays.

- The committee should confirm whether the university will provide a subdomain, which would avoid the domain cost entirely.

- Because most services bill in dollars, exchange rate changes can raise costs during the year.

- Everything should be registered under a BUSEC committee email and billing account.

## 10. Timeline (1 month)

Kickoff is Saturday, Oct 24, 2026. Launch is Tuesday, Nov 24, 2026, with Nov 25 to 27 held as buffer.

Page 6 of 9

BUSEC Blog PRD

|Milestone|Date|Backend|Frontend and design|Editorial and<br>content|
|---|---|---|---|---|
|Kickoff|Sat Oct<br>24|Repo and account<br>access for<br>everyone|Repo and account<br>access for everyone|Name a content<br>lead|
|M0: Setup|Wed<br>Oct 28|Decide Django vs.<br>FastAPI. Create<br>BUSEC repos and<br>accounts|Decide plain React<br>vs. Next.js. Start<br>branding and<br>wireframes|Agree on<br>categories|
|M1:<br>Foundations|Wed<br>Nov 4|Data models,<br>login, and roles on<br>a dev server.<br>Agree the API<br>shape with<br>frontend|Brand and<br>wireframes approved<br>for landing, article,<br>committee, and e-<br>magazine pages.<br>Project scaffold<br>ready|Draft the "about<br>BUSEC" copy.<br>Collect<br>committee<br>photos and bios|
|M2: Core flow|Wed<br>Nov 11|Draft, submit,<br>publish, and<br>delete workflow<br>plus media upload<br>through the API|Landing page, article<br>and poem/literature<br>pages, and staff<br>editor connected to<br>the API|Hand over the e-<br>magazine PDF<br>and committee<br>data|
|M3: Feature<br>complete|Wed<br>Nov 18|Committee year<br>filter, newsletter<br>signup endpoint,<br>backups, staging<br>deployment|Committee page,<br>newsletter form,<br>flipbook, mobile<br>polish|Journalists enter<br>real articles on<br>staging|
|M4: Launch-<br>ready|Mon<br>Nov 23|Bug fixes, security<br>checks, domain<br>connected|Bug fixes and testing<br>on real phones|Training session<br>for journalists<br>and executives.<br>Handover docs<br>reviewed|
|Launch|Tue Nov<br>24|Live on the<br>domain|Live on the domain|Announce on<br>BUSEC channels|
|Buffer|Wed<br>Nov 25<br>to Fri<br>Nov 27|Slippage only|Slippage only|Slippage only|

Page 7 of 9

BUSEC Blog PRD

One month is tight for this scope. The plan only works if the stack decisions are made by Oct 28 and the e-magazine PDF and committee content arrive by Nov 11. If time slips, cut in this order: flipbook polish (use a simple PDF viewer with a download link), newsletter automation (collect emails and send manually), then featured post controls (show the latest posts).

## 11. Team and ownership

|Area|Owner|
|---|---|
|Product and coordination|Demi|
|Backend|Daniel (lead), Greatness (co-lead), David,<br>Jesutofunmi|
|Frontend|Demi, Mayor|
|Design and branding|Demi, Mayor|
|Content and editorial workflow (editorial<br>side)|TBD|
|Content migration and seeding|TBD|

## 12. Handover plan

- All repositories, hosting, domain, and third-party services are created under a BUSEC committee email and the BUSEC account, not personal ones.

- Credentials stored in a shared password manager that the executives can access.

- A README for setup and deployment, plus a short guide for journalists and executives on writing, publishing, and updating the committee page.

- A handover checklist listing every account, renewal date, and who is responsible.

- A short walkthrough session with the incoming tenure.

## 13. Risks

|Risk|Mitigation|
|---|---|
|One-month timeline is tight|Hold the MVP scope firmly. Defer search,<br>comments, and automated newsletters.|

Page 8 of 9

BUSEC Blog PRD

|Risk|Mitigation|
|---|---|
|Free hosting tiers sleep or hit limits|Test early. Budget for a small paid plan on the<br>backend if needed.|
|Domain renewal is missed or unaffordable|Put the renewal on the handover checklist.<br>Explore a school subdomain.|
|Team turnover|Documentation, shared accounts, and a clean<br>codebase.|
|Journalists find the editor hard to use|Test the editor with real journalists in week 3.|
|Large PDFs make the flipbook slow on<br>phones|Compress PDFs, load pages progressively, and<br>offer a download fallback.|

## 14. Open questions

1. Django or FastAPI?

2. Plain React or Next.js (for SEO and link previews)?

3. Who owns the editorial workflow and content migration on the editorial side?

4. Can journalists edit only their own posts, or others' too?

5. How is the newsletter sent, and by whom?

6. What are the post categories and how are poems and literature organized?

7. Are there existing articles or past issues to migrate?

Page 9 of 9
