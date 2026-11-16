# AI Workspace

[한국어](./README.md) | English

This is a personal repository where I keep the documents and skills I use to build software with AI agents. It covers what an agent reads before starting work, how we divide up the work, and what we write down when we're done.

Most of what’s here is Markdown and skill definitions. The only runnable code is a small sample product that shows the approach in practice. I use this with Claude Code and Codex. There’s no library or CLI to install.

- [`reference-project/`](./reference-project/) is a working example of the approach applied to a sample product. Start here to see how it works.
- [`.agents/skills/apply-context-harness/`](./.agents/skills/apply-context-harness/) contains the skill for bringing the reference project's setup into another project.
- [`context/`](./context/) holds the work records from designing and revising this approach. They account for most of the files in the repository. You can skip them if you just want to understand the approach.

## The problem I’m trying to solve

This actually happened. An agent read the previous session’s notes, picked up the work, and suggested fixing two bugs first. What I wanted at that point was to revisit the structure and the reasoning behind it. The notes were there. The agent had read them. What hadn’t carried over was a sense of what mattered *now*.

When I develop with AI agents, the work itself carries over fairly well. The goal, scope, and criteria for finishing are written down, and the next session can pick up from there. The reasoning is easier to lose. Why we chose a particular structure, where the evidence was thin, and what would make us revisit the choice rarely make it into the notes. The next session then treats the choice as a given.

The things that are easy to measure also tend to get written down first. A passing test or a checked box is visible immediately. Whether the code is ready for the next change takes longer to judge, and the answer is less clear. Soon “implemented,” “passed the checks,” and “accepted by the person doing the work” blur together. The next session starts from a claim of completion that the evidence doesn’t support.

Writing more careful notes didn’t get me very far on its own. I started by deciding which document is responsible for what, then built the practices for reading, developing, and keeping records around that.

## Three layers of context

| Layer | What it holds | When it changes |
| --- | --- | --- |
| Personal | The criteria I use to make decisions and what I’ve learned about working with others, across projects | When I adopt or revise a criterion |
| Project | What a product means, how it is currently structured, its contracts, and the reasoning behind choices that span tasks | When the product or its implementation changes |
| Work | The goal, current state, source material, and history of one task | Throughout the task |

Two rules apply to all three layers.

- Keep each fact in one place. If another document is responsible for it, point there.
- A decision made in one task stays at that level until someone considers it separately and decides to adopt it for the product or as a personal criterion.

**Personal** currently covers five areas of development judgment: what to share across the codebase, contracts and lifetimes, naming and when work counts as complete, how code is expressed and problems are diagnosed, and design systems. Each topic has general criteria, with code examples where they help. This layer also holds lessons from working with AI and possible improvements I haven’t adopted yet. The person decides which criteria to adopt.

**Project** is organized around how long information stays useful. It separates enduring product concepts and constraints (`common`), the more changeable details of the current implementation and what it supports (`current`), contracts and criteria that work must satisfy (`guidance`), and the reasons for important choices and signals to revisit them (`decisions`). When the current implementation and the meaning of the product share a document, each change means working out all over again which parts need revising.

**Work** has one Workspace per task.

```text
reference-project/
├── AGENTS.md                 Instructions an agent reads first (CLAUDE.md is a symlink to this file)
├── .agents/skills/           Skill definitions (.claude/skills and .codex/skills point here)
├── src/, tests/              Sample product and checks
└── context/
    ├── personal/             Personal criteria and experience
    ├── project/              Product concepts, current structure, contracts, and decisions
    └── work/workspaces/
        └── 001-default-timeout/
            ├── recover.md    What to read when resuming, and why
            ├── current/      Current goal, Spec, Ticket, and state
            ├── source/       Source material selected for this task and where it came from
            ├── output/       Where to find the actual deliverables
            └── records/      Options considered, comparisons, attempts, and verification
```

`current/` holds the Spec and Ticket. A Spec defines the problem, the intended outcome, and the criteria for judging it. A Ticket is a unit of work that produces a verifiable result within those criteria. The distinction is what each is responsible for, regardless of size. The Spec sets out what the user should be able to do and what is out of scope this time. Decisions such as which module to use or whether to keep an existing abstraction stay open until someone looks at the code.

## How a task unfolds

These four practices come into play as needed, with no fixed sequence.

**1. Resuming.** A new session starts with the Workspace’s `recover.md`. This file points to what to read and explains why. Anything an agent needs to understand the goal or the next action goes in the default reading. Material needed only for a particular decision comes with a condition for reading it. Here are three entries, shortened from the sample Workspace’s [`recover.md`](./reference-project/context/work/workspaces/001-default-timeout/recover.md).

| Request or decision | What to read |
| --- | --- |
| Explain or change the default, rejected inputs, or return value | Compare the Project guide to selecting context, the required behavior, and the input/output contract with the actual code |
| Decide why the default is `5000` or whether to keep the current implementation | Read the default-timeout decision and its constraints, design, and assumptions |
| Reuse an earlier verification result as evidence | Find the run in the records index and compare its conditions with the code as it stands |

The idea is to avoid reading the entire Workspace every time. The guide gives the agent a place to start. If it finds a gap, it reads further.

**2. Development.** The [`development`](./reference-project/.agents/skills/development/SKILL.md) skill connects implementation through verification. There are four roles.

- The lead agent talks with the user, connects the goal to the relevant context, decides which review findings to act on, and judges when the work as a whole is complete.
- The implementer takes the assigned usage scenario through implementation and checks it. Known gaps are the implementer’s to address before review.
- The improvement reviewer compares the current choice with meaningful alternatives.
- The verifier checks whether the requirements have been met and stays independent of implementation and fixes.

For changes to behavior or a contract, the default is one separate verifier. For a typo, the lead agent’s own check is enough. The number of agents depends on the work.

**3. Keeping records.** Calling [`record-work`](./reference-project/.agents/skills/record-work/SKILL.md) brings in an agent that reads the original conversation, checks the actual results, and edits the Work documents directly. I call it when wrapping up a task or when the work changes direction, and use the same agent again within a conversation. If what to read or why to read it has changed, it updates `recover.md` too.

**4. Making improvements.** When the user asks to look back over a conversation, [`improvement-loop`](./reference-project/.agents/skills/improvement-loop/SKILL.md) looks for possible improvements in the conversation and related documents. We apply the ones we choose together. Experiences and suggestions we haven’t adopted go into Personal so we can revisit them. Finishing a task doesn’t trigger this automatically.

Throughout the work, passing a check, receiving human acceptance, and completing a task are recorded as distinct states.

## Skills

The reference project has eight skills. Their definitions live in [`reference-project/.agents/skills/`](./reference-project/.agents/skills/README.md).

| Skill | When to use it | What it does |
| --- | --- | --- |
| `development` | Implementing a feature, fixing a bug, refactoring, or reviewing a result | Connects requirements to context and coordinates implementation, improvement review, and verification |
| `record-work` | When asked to keep a record or when wrapping up work | Updates the Work documents from the original conversation and the results |
| `improvement-loop` | When the user asks to look back over a conversation | Finds possible improvements, helps choose and apply them together, and records what was learned |
| `explain` | When asked about a concept, code, a result, or something said earlier | Explains relationships and reasons for choices by referring to the thing being discussed |
| `work-discussion` | Only when the user explicitly invokes it | Agrees on the desired outcome and scope with the user and turns them into a Spec before implementation |
| `reconsider-work` | When results, new conditions, or a blocker call the approach into question | Reassesses whether the approach still serves the original goal |
| `context-update` | When a lasting change to Personal or Project has been established | Revises the relevant content and the path readers follow to find it, within the authorized scope |
| `create-context-workspace` | When starting a new, independent task | Creates a Workspace and its guide to resuming work |

There’s no common sequence to run for every task. I add a skill once I’ve seen the same procedure recur in practice. Each document keeps its content and its responsibilities even if a skill is removed or changed.

## Take a look

If this is your first visit, I’d read these in order.

1. [Reference project README](./reference-project/README.md) for the three layers and where to start.
2. The sample Workspace’s [`recover.md`](./reference-project/context/work/workspaces/001-default-timeout/recover.md) to see what a guide to resuming work looks like.
3. The [`development` skill](./reference-project/.agents/skills/development/SKILL.md) for the roles and how they work together.
4. [Personal development criteria](./reference-project/context/personal/development/INDEX.md) for examples of how I write down the criteria I use when developing software.

The sample product is a small Python module that reads request policy settings. To run its checks:

```bash
cd reference-project && python3 -B -m unittest tests.test_config_loader -v
```

To try the setup in your own project, open this repository with an agent and give it the target path. The repository’s top-level `apply-context-harness` skill handles the request.

```text
Bring the reference-project setup into ~/code/my-app.
Only create new files under context/ and .agents/, and leave existing documents alone.
Use the payment module separation I’m working on now as the first Workspace.
```

The agent first reads the target’s existing instructions and documents and checks its Git status. It shows you which files it plans to create and which it will leave alone, then waits for approval. It fills the Project context with facts from the target project itself. The sample product’s content stays in the reference project. A commit to the target project requires separate approval.

## How the setup has changed

The setup looks quite different from where it started.

Originally it centered on three Python runners. Recover assembled a set of documents for a new session to read. Maintain automatically wrote changes back to the documents after every response. Verify pinned the evidence files, ran the checks, and saved the results as JSON.

I brought that setup into a product under active development and took stock of what it was like to use. I spent less time explaining things again. But as in the incident above, I still had to refocus an agent that had read the notes. Sometimes I had to ask a second time before I got a better explanation of the result. I broadened the scope from the structure of context documents to how we develop, explain the work, and act on experience. That’s when I added `development`, `improvement-loop`, and the Personal layer, and merged two explanation skills into `explain`.

I retired all three runners.

- **I replaced Maintain with `record-work`.** Running it automatically after every response felt too costly. That was a judgment call. I didn’t measure the cost. Now I call in the agent that keeps the records when I need it.
- **I replaced Recover with `recover.md`.** The guide says what to read, why, and under what conditions. The reader decides what’s relevant, without being handed a fixed bundle of documents.
- **I archived Verify.** The product checks could run on their own, and `development` already handled the judgment about whether the work met the requirements.

I lost a few things in the change. The current setup doesn’t automatically snapshot inputs before a run, save result files, compare earlier evidence to see whether it’s stale, or forcibly terminate a check and its child processes. The test tools and Git can still do the same jobs, but those actions no longer run together automatically.

## What I’ve checked and what’s still open

| What I’ve checked | What I haven’t established yet |
| --- | --- |
| All seven sample product checks pass | Whether context actually holds up over a long period |
| The reference project’s document links and skill connections are in place | Whether agent tools consistently discover and invoke the skills |
| I brought the setup into one real product, used it, and spent less time explaining things again | How well the agent that keeps the records judges what to preserve from the original conversation |
| I tried resuming work in a new session, within a limited scope | Whether other projects and other people see the same results |

Personal currently lives in a folder inside each project. There’s no mechanism for distributing or syncing it across repositories.

## Repository map

- [`reference-project/`](./reference-project/) holds the reference project, including its documents, skills, and sample product.
- [`.agents/skills/`](./.agents/skills/) contains `apply-context-harness`, the skill for bringing the setup into another project.
- [`context/workspaces/`](./context/workspaces/) holds the state and records of the fifteen tasks that shaped this approach. Some were finished, some put on hold, and some stopped. I kept the reasons for dropping work, too. The experimental inputs and comparison material account for much of the volume.
- [`context/source/`](./context/source/) holds source material used by more than one task.
- [`AGENTS.md`](./AGENTS.md) and [`CODE-QUALITY.md`](./CODE-QUALITY.md) set out the instructions agents follow here and the criteria for code work.

I keep revising this repository as I use it, so the structure and skill list will change. I haven’t chosen a license yet.
