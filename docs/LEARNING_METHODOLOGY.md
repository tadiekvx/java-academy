# Learning Methodology

Date: 2026-11-05 · Companion to `CURRICULUM_AUDIT.md`. This replaces the earlier methodology scattered across `01-curriculum-design.md`.

## 0. Provenance: what research was and wasn't done

**Before this document**, the course's research base was the peer-reviewed list in `docs/curriculum/sources.md`, mostly cited from memory, plus a single "community" entry (C1) that described advice from Reddit-style communities **without any source being consulted**. That entry was not evidence and is withdrawn.

**This session I fetched and read** the sources listed in §6. Each register entry says what was actually read. Some things I tried and could not do, and they are *not* claimed:

| Attempt | Outcome |
|---|---|
| Read the top comments of the r/learnprogramming "tutorial hell" thread (Jul 2020) | `old.reddit.com` is blocked for this tool; a mirror host did not resolve. **Not read.** The thread is listed as a lead only |
| Read r/learnjava's FAQ/sidebar | Search results show several Reddit threads saying it recommends the University of Helsinki MOOC. I read **search snippets only**, not the FAQ |
| Stack Overflow discussion threads | Not read. I used the **Stack Overflow Developer Survey 2024** page (read) instead, which is data about how developers learn rather than discussion |
| Engineering interviews | Read a secondary summary of *Coders at Work* (Ben Kuhn's notes), **not the book** |
| 2025 Stack Overflow survey | Only press-release numbers via search; the full report was not reached. Not relied on |

Where I say a "theme recurs", I mean it appeared in at least two independently written sources that I read. Community posts are anecdotes about what felt useful to the writer. They are weaker evidence than controlled studies, and the register labels them that way.

## 1. Evidence classes

| Class | Examples | How we use it |
|---|---|---|
| **Research** | Controlled studies, meta-analyses, reviews | Basis for design rules, with the caveat of each study's population (usually school pupils or university CS1) |
| **Practitioner testimony** | Experienced developers' essays and interviews | Source of hypotheses about what produces independent engineers; never presented to learners as fact |
| **Community** | HN, Reddit, DEV, forums | Signal of recurring learner pain and advice; weakest class |
| **Platform data** | Our own attempt and retrieval data | The tie-breaker once learners exist |

## 2. Recurring themes

Each theme lists the sources that support it (register IDs in §6) and the disagreements found.

### T1. Build things; consume less

Experienced developers repeatedly say they got good by **making things**, often their own, and by finishing and maintaining them. *Support:* HN-2022 (mediocregopher, timoteostewart, matthewmacleod), HN-2023 (x86x87, topkai22), HN-2024 (crq-yml, yodsanklai), Norvig 2001 ("program"), Coders at Work notes (Armstrong: good programmers "spend a lot of time programming"). Community "tutorial hell" posts say the same from the learner side (DEV and Medium posts located; thread comments not read).

*Disagreement/caveat:* none about the principle. Blog advice on *how small* varies. We take "small, finishable, extended later" (T6).

### T2. Read other people's code

The single most repeated practice. *Support:* HN-2022 (rektide, jcranmer, timoteostewart), HN-2023 (x86x87, karmakaze, sibeliuss), HN-2024 (gregjor), Norvig ("talk with other programmers and read their code", "work on projects after other programmers"), Coders at Work notes (Crockford: reading code is "the most useful thing" a community can do), Atwood 2012.

*Disagreement:* Atwood argues the source is the ultimate reference because docs are poor; HN commenters (philosopher1234, tomcam) and Hanselman push back that docs are valuable. *Our position:* teach both. Reading *small, well-chosen* programs early; reading library docs *and* source later.

### T3. Debugging, tools and "dig deeper"

Practitioners credit debuggers, reading errors and pushing past the first failure. *Support:* HN-2022 (rektide), HN-2023 (japhyr: testing as the biggest leap), HN-2024 (sandreas: know your tools, deployment). McCauley et al. 2008 review: debugging is a distinct skill that is rarely taught.

*Disagreement:* HN-2023: testing vs. profiling priority (japhyr vs karmakaze). We introduce testing before performance.

### T4. Feedback, review and mentors

Feedback exposes blind spots. *Support:* HN-2024 (bilsbie: code review; al_borland: users' feedback; gregjor: mentors), HN-2022 (PaulDavisThe1st), Coders at Work notes (work with very capable people), Norvig.

*Disagreement (important for the AI mentor):* PaulDavisThe1st valued a mentor who **would not just give answers**; philosopher1234 argued answers must sometimes be given; don-code reports the approach frustrates others. *Our position:* graded help (H0–H4) with transparent unlocks, which is how we reconcile both views; the Bastani et al. 2025 field experiment (R13) supports guardrails.

### T5. Fundamentals before frameworks; look beneath abstractions

*Support:* HN-2022 (betwixthewires, matthewmacleod: data structures first), HN-2024 (ThePhysicist: build your own ORM/interpreter; sandreas: learn concepts, not frameworks), Norvig (know performance characteristics; learn several languages).

*Disagreement:* HN-2024: throwaway38375 says the stack matters less than users think and to avoid unnecessary complexity; SeanAnderson emphasises business communication over technical depth. *Position:* keep Spring and tools in the curriculum, but after fundamentals, and teach trade-offs rather than frameworks as magic.

### T6. Incremental, finishable projects; maintain old code

*Support:* DEV "tutorial hell" posts (add one feature, test, commit, repeat; located by search, **posts not individually read**), HN-2023 (karmakaze: maintain old code you wrote; contingencies: maintenance teaches design for maintainers; topkai22: write code more than once), Norvig ("work on projects after other programmers").

*Position:* this is the basis for **project continuity**: one application evolves across stages (see master curriculum).

### T7. Structured guidance for novices, less for experts

*Support (research):* Kirschner, Sweller & Clark 2006 (minimal guidance fails for novices), Kalyuga et al. 2003 (expertise reversal: guidance that helps novices can hurt experienced learners), Ericson et al. 2017 (Parsons problems as efficient scaffold), Kapur 2008 (struggle before instruction can help, under some conditions).

*Disagreement:* Kirschner/Sweller and Kapur disagree about when struggle first is productive. *Position:* guided early; fade scaffolds by stage; use "try it first" only after Stage 1, and measure.

### T8. Practice that is retrieved and spaced

*Support:* Roediger & Karpicke 2006 (retrieval beats re-reading), Cepeda et al. 2006 (spacing; **but** only about a third of the intellectual-skill studies it reviewed showed a benefit, so programming transfer is untested).

### T9. Tracing and reading precede writing

*Support:* Leeds Group 2004 (many novices could not trace short code, which may explain later failure), Qian & Lehman 2017 (review of misconceptions: mental models, syntax, strategy), Guo 2013 (an embeddable step-through visualiser used by hundreds of thousands in its first three years).

### T10. Disagreements to keep visible

- **Talent vs effort** (HN-2024: riehwvfbk vs Jaedon_Proctor vs confidantlake). We do not claim a position; the course measures progress per learner instead.
- **Formal education vs self-teaching** (HN-2022: jcranmer vs LeftHandPath; Norvig: college helps but isn't required).
- **Whether "great" is meaningful** (HN-2024: gregjor, aristofun). We use "independent competence" as the goal instead.

## 3. Common learner failure modes and how the design answers them

| Failure mode (source) | Design answer |
|---|---|
| "Tutorial hell": can follow but cannot start from blank (community posts; T1, T6) | Independent challenges from Stage 1; projects with requirements only; no-hints assessments |
| Cannot trace code (Leeds Group; T9) | Trace tables, step-through visualiser, predict-then-run in every lesson |
| Over-reliance on AI answers (R13) | Graded mentor, attempt-first mode, assisted vs independent recorded separately |
| Never read code written by others (T2) | Code-reading exercises on unfamiliar programs from Stage 1 onwards; inherited-codebase projects from Stage 2 |
| Forgetting (T8) | Spaced retrieval checks and cumulative assessments |
| Skipped fundamentals, then stuck on frameworks (T5) | Frameworks placed after OOP, collections, testing, SQL; every framework lesson starts from what the framework replaces |
| Jumping straight to hard projects without scaffolding (T7) | Guided → independent → professional project categories with scaffolding that fades |

## 4. The six-activity cycle, as now justified

| Activity | What it is | Support |
|---|---|---|
| Understand | Worked examples, predict-before-run | T7; Leeds Group; subgoal labels are used as a *design choice*: the Morrison et al. 2015 results were **mixed** and are not cited as proof |
| Apply | Parsons → write | Ericson 2017 (Parsons are efficient scaffolds, not proof of independent ability) |
| Investigate | Tracing, debugging, reading code | T2, T3, T9 |
| Build | Projects | T1, T6 |
| Explain | Written explanations, mentor follow-ups | Chi et al. 1989 (unverified; not relied on beyond design intent) |
| Reinforce | Spaced retrieval | T8, with the transfer caveat |

## 5. What this means for the platform (decisions taken)

1. **Projects move earlier and become central.** Stage 1 gets two guided mini-projects and one independent project, plus an independent assessment. (`JAVA_MASTER_CURRICULUM.md`)
2. **Project continuity:** one application (a bank) evolves from Stage 1 to a Spring Boot backend; see the master curriculum.
3. **Code reading becomes a graded activity** with its own evidence type.
4. **A step-through visualiser** shows variable state line by line (modelled on Guo 2013).
5. **Curated external resources** (videos, courses) are attached to lessons through content files, not frontend code.
6. **Claims to learners are limited to what the sources support.**

## 6. Source register

Status: **Read** = I opened it this session and the entry reflects what it says. **Snippet** = I saw only search-result text. **Lead** = located but not read.

### 6.1 Community and practitioner sources

| ID | Title / source | Contributor | URL | Date | Type | Status | Insight used | Influence |
|---|---|---|---|---|---|---|---|---|
| C3 | Ask HN: What helped you get good at programming? | Many; notable: rektide, PaulDavisThe1st, jcranmer, mediocregopher, philosopher1234 | https://news.ycombinator.com/item?id=31240927 | 2 May 2022 | Community thread | Read (summary of top-level comments) | Read library source and learn tools; mentors who don't hand over answers (disputed); many side projects; data structures first | T1–T5; mentor policy |
| C4 | Ask HN: What took you from being a good programmer to a great one? | Many; notable: ThePhysicist, SeanAnderson, bilsbie, gregjor | https://news.ycombinator.com/item?id=39656745 | 10 Mar 2024 | Community thread | Read | Look beneath abstractions; code review; build for users; talent-vs-effort dispute | T4, T5, T10 |
| C5 | Ask HN: How did you become a "good enough" programmer? | Many; notable: topkai22, japhyr, karmakaze, contingencies | https://news.ycombinator.com/item?id=34390205 | 15 Jan 2023 | Community thread | Read | Write code more than once; testing as biggest leap; maintain old code | T3, T6 |
| C6 | Teach Yourself Programming in Ten Years | Peter Norvig | https://norvig.com/21-days.html | 2001 (© 2001–2014) | Essay | Read | Program a lot; read and work after others' code; deliberate practice; no shortcuts | T1, T2, T4, T5 |
| C7 | Learn to Read the Source, Luke | Jeff Atwood | https://blog.codinghorror.com/learn-to-read-the-source-luke/ | 16 Apr 2012 | Blog | Read | Source is the reliable reference; reading code is a learnable skill | T2 (with disagreement) |
| C8 | Study recommendations from *Coders at Work* | Ben Kuhn (about Peter Seibel's 2009 book) | https://benkuhn.net/caw-study | Aug 2015 | Secondary summary of interviews | Read (the book itself not read) | Reading code is the most emphasised practice; work with strong people; program a lot | T2, T4 |
| C9 | Stack Overflow Developer Survey 2024, Developer Profile | Stack Overflow | https://survey.stackoverflow.co/2024/developer-profile/ | 2024 | Survey data | Read | Among those learning to code, 84.9% use online resources, 55.6% school, 39.5% books, 13.1% on-the-job. Documentation is the top online resource across all respondents (83.9%) | Documentation-reading is taught; books are a minor source for learners |
| C10 | r/learnprogramming: "How students get themselves into tutorial hell…" | (author not retrieved) | https://redlib.hackliberty.org/r/learnprogramming/comments/i0kld3/how_students_get_themselves_into_tutorial_hell | 30 Jul 2020 | Reddit thread | **Lead** (comments not read) | None used | none |
| C11 | Several DEV Community and Medium posts on escaping "tutorial hell" | various | e.g. https://dev.to/lanrewaju/getting-out-of-tutorial-hell-2fm4 | various | Blog posts | **Snippet** | Start small; build alongside tutorials; add features incrementally | T6 (stated as low confidence) |
| C12 | r/learnjava and r/learnprogramming threads recommending the University of Helsinki Java MOOC | various | e.g. https://redlib.hbubli.cc/r/learnjava/comments/o3otnf/helsinki_mooc/h2dkypd/ | 2021–2026 | Reddit threads | **Snippet** | Repeated recommendation of the Helsinki MOOC; some note setup friction and outdated tooling | Candidate external resource, to be reviewed directly |

### 6.2 Educational research

| ID | Citation | URL / DOI | Status | Finding used | Caveat |
|---|---|---|---|---|---|
| R1 | Roediger & Karpicke (2006), *Psychological Science* 17(3), 249–255 | doi 10.1111/j.1467-9280.2006.01693.x (DOI from memory, not opened) | Snippet (bibliographic + secondary summaries) | Retrieval practice beat re-reading after a week | Prose passages, not programming |
| R2 | Cepeda et al. (2006), *Psychological Bulletin* 132(3), 354–380 | https://pubmed.ncbi.nlm.nih.gov/16719566/ | Snippet | Spacing helps verbal recall; best gap grows with retention interval | Only a third of "intellectual skill" studies showed a benefit |
| R3 | Kalyuga, Ayres, Chandler & Sweller (2003), *Educational Psychologist* 38(1), 23–31 | https://ro.uow.edu.au/edupapers/136 | Snippet | Guidance helpful to novices can hurt experienced learners | |
| R4 | Morrison, Margulieux & Guzdial (2015), ICER '15, 21–29 | doi 10.1145/2787622.2787733 | Snippet | **Mixed results** on subgoal labels in intro CS | Previously mis-summarised as positive |
| R5 | Lister et al. (2004), "A multi-national study of reading and tracing skills in novice programmers", SIGCSE Bulletin 36(4), 119–150 | https://www.cs.auckland.ac.nz/~j-hamer/ITiCSE04-wg.pdf | Snippet | Many novices struggle to predict the result of short code | Findings beyond abstract not read |
| R6 | Sentance, Waite & Kallia (2019), *Computer Science Education* 29(2–3) | doi 10.1080/08993408.2019.1608781 | Read earlier (bibliographic + design) | PRIMM evaluated in 13 schools, 493 pupils | Pupils aged 11–14, teacher-led |
| R7 | Ericson, Margulieux & Rick (2017), Koli Calling | doi 10.1145/3141880.3141895 | Snippet (via later papers) | Parsons problems faster than writing code with similar learning gains | CS1 students |
| R8 | Qian & Lehman (2017), *ACM TOCE* 18(1), 1:1–24 | doi 10.1145/3077618 | Snippet (abstract) | Misconceptions in syntax, concepts and strategy | |
| R9 | Altadmri & Brown (2015), SIGCSE '15, 522–527 | doi 10.1145/2676723.2677258 | Read earlier | Frequencies of real novice Java mistakes | BlueJ users 2013–14 |
| R13 | Bastani et al. (2025), *PNAS* 122(26), e2422633122 | doi 10.1073/pnas.2422633122 | Read earlier (abstract-level) | Unrestricted GPT-4 helped practice, hurt later performance; guardrails reduced harm | High-school maths |
| R14 | Kapur (2008), *Cognition and Instruction* 26(3), 379–424 | doi 10.1080/07370000802212669 | Snippet | Struggle before instruction can help transfer | Domain of the study not confirmed |
| R16 | McCauley et al. (2008), *Computer Science Education* 18(2), 67–92 | doi 10.1080/08993400802114581 | Snippet | Debugging literature review: causes, types, process, teaching | |
| R17 | Kirschner, Sweller & Clark (2006), *Educational Psychologist* 41(2), 75–86 | doi 10.1207/s15326985ep4102_1 | Snippet | Argument that minimal guidance is ineffective for novices | Contested by proponents of inquiry learning |
| R18 | Guo (2013), "Online Python Tutor", SIGCSE '13, 579–584 | https://pg.ucsd.edu/publications/Online-Python-Tutor-web-based-program-visualization_SIGCSE-2013.pdf | Snippet | Embeddable step-through visualiser; 200,000+ users in three years; adopted in a dozen universities | Reports adoption, not learning gains |

### 6.3 Not verified

R10, R11, R12, R15, Lopez et al. (2008), Sweller & Cooper (1985) remain unverified in `docs/curriculum/sources.md`. The publication gate blocks lessons citing them as `published`.

## 7. Review cycle

Re-verify the register annually. Replace snippets and leads with full reads before any claim from them is shown to learners. When platform data exists (retrieval pass rates, hint dependency), compare it with these themes and record where the course's learners disagree with the literature.
