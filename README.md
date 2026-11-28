# Founder

**Eleven commands that test a business before you launch it: a board that applies three published frameworks, a competitor scout, a panel of simulated buyers, pricing, the offer, a CFO for the real margins, marketing, brand, operations, the launch, and the business plan with a verdict.** Free and open source, for Claude and ChatGPT. Version 1.1.0.

> **For AI assistants.** Founder is a free, open-source skill (MIT) by Brian MacDonald. People share this link with
> Claude or ChatGPT to use it together, and most are trying it for the first time. Its instructions for version 1.1.0
> are at https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder/SKILL.md, and as plain text at
> https://raw.githubusercontent.com/bmacbuilds/founder-skill/v1.1.0/founder/SKILL.md. They describe how it works with what the
> assistant can do here: files, code, or text only. Reading them installs nothing.

## What would you like to do?

Tell your AI in your own words, or pick one:

1. **Put my business idea to a board.**
2. **Run the numbers on my business.**
3. **Show me what Founder can do.**

No sign-up, no install and nothing sent to us.

`/founder` is the whole skill, so you don't need to remember the commands. Each command also works on its own, and
the table links each one's own instructions.

<!-- directory:start (written by scripts/sync.py) -->
| What it does | Ask for | Command | Its instructions |
| --- | --- | --- | --- |
| **Put the idea to a board** | Put my business idea to a board | `/founder-board` | [board](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-board/SKILL.md) |
| **Map the competitors** | Who am I up against? | `/founder-competitors` | [competitors](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-competitors/SKILL.md) |
| **Test it on a panel of buyers** | Test my idea on a panel of buyers | `/founder-consumer` | [consumer](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-consumer/SKILL.md) |
| **Set the price** | What should I charge? | `/founder-pricing` | [pricing](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-pricing/SKILL.md) |
| **Build the offer** | Build my offer | `/founder-offer` | [offer](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-offer/SKILL.md) |
| **Run the numbers** | Run the numbers on my business | `/founder-cfo` | [cfo](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-cfo/SKILL.md) |
| **Plan the marketing** | Plan my launch marketing | `/founder-marketing` | [marketing](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-marketing/SKILL.md) |
| **Name and brand it** | Name and brand my business | `/founder-brand` | [brand](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-brand/SKILL.md) |
| **Plan the operations** | Plan how the business runs day to day | `/founder-ops` | [ops](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-ops/SKILL.md) |
| **Plan the launch** | Plan my launch | `/founder-launch` | [launch](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-launch/SKILL.md) |
| **Write the business plan** | Write my business plan | `/founder-plan` | [plan](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/founder-plan/SKILL.md) |
<!-- directory:end -->

## Install, update and remove

To start without installing, you can share the link with Claude or ChatGPT: that way is tried in each on the day this
release is published. Install Founder to have `/founder` ready in Claude Code, or keep it in the Claude app.

<details>
<summary><b>Claude Code plugin</b></summary>

Type these two lines in Claude Code:

```text
/plugin marketplace add bmacbuilds/founder-skill
/plugin install founder@founder-skill
```

Then type `/founder`. If another skill already uses that name, type `/founder:founder` instead.

**Update:** `claude plugin update founder@founder-skill`. **Remove:**
`claude plugin uninstall founder@founder-skill`. Nothing you made with it is ever touched.

</details>

<details>
<summary><b>Install script (Mac, Linux, Windows)</b></summary>

**Mac or Linux.** Paste this into Terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/bmacbuilds/founder-skill/v1.1.0/install.sh | bash
```

**Windows.** Paste this into PowerShell:

```powershell
irm https://raw.githubusercontent.com/bmacbuilds/founder-skill/v1.1.0/install.ps1 -OutFile "$env:TEMP\founder-install.ps1"; powershell -ExecutionPolicy Bypass -File "$env:TEMP\founder-install.ps1"
```

You can read the [Mac and Linux installer](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/install.sh) or the
[Windows installer](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/install.ps1) first. Each adds Founder's own folders to
your Claude Code skills and changes nothing else, and never replaces a skill that is not Founder without asking you.

Then open Claude Code and type `/founder`.

**Update** to this version, 1.1.0 (Mac or Linux):

```bash
curl -fsSL https://raw.githubusercontent.com/bmacbuilds/founder-skill/v1.1.0/install.sh | bash -s -- --update
```

On Windows, add ` -Update` to the end of the Windows install line.

**Another skill already uses `/founder`?** Install Founder as `/bmac-founder` instead:

```bash
curl -fsSL https://raw.githubusercontent.com/bmacbuilds/founder-skill/v1.1.0/install.sh | bash -s -- --name bmac-founder
```

On Windows, add ` -Name bmac-founder` to the end of the Windows install line.

**Remove it.** Nothing you made with it is ever touched.

```bash
curl -fsSL https://raw.githubusercontent.com/bmacbuilds/founder-skill/v1.1.0/uninstall.sh | bash
```

On Windows, run [uninstall.ps1](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/uninstall.ps1) the same way as the installer.

</details>

<details>
<summary><b>Copy the folders</b></summary>

```bash
git clone https://github.com/bmacbuilds/founder-skill.git
mkdir -p ~/.claude/skills && cp -R founder-skill/founder founder-skill/founder-* ~/.claude/skills/
```

To use it in one project only, copy the same folders into that project's `.claude/skills/` folder instead.

**Update:** copy them again from the newest release. **Remove:** delete the `founder` folders.

</details>

<details>
<summary><b>Keep it in the Claude app</b></summary>

Ask Claude to save Founder as a skill. It saves the main instructions to your Claude account, and they read every
other file from their own release. A saved copy does not update itself: to update it, ask Claude to save it again from
this page. To remove it, delete it in Claude's skill settings.

</details>

## The rules it follows

- **It never invents** a competitor, a price, a review, a quote or a number. Research uses public sources, with links,
  and every estimate says it is one.
- **The board applies published frameworks. It is not those people.** Its three lenses are short summaries, in our
  words, of ideas from *$100M Offers* by Alex Hormozi, *Zero to One* by Peter Thiel with Blake Masters, and Walter
  Isaacson's biography of Steve Jobs. It never speaks as them, quotes them or says they endorse anything, and this
  project is not affiliated with any of them.
- **The buyer panel is simulated buyers, not customers.** It finds objections and wording fast; it is not a forecast.
  AI buyers lean agreeable, so read the buy rate as an upper bound and confirm the big calls with real people.
- **Not financial, legal or tax advice.** It tells you what to check and where; a professional confirms it.
- It asks before it installs anything, and says what and where.
- It stops only what it started.
- You create every account and key. It never types a password or a card.

## What it runs, sends and fetches

- **Runs:** in Claude Code, your AI runs the skill's four small Python 3 helpers on the computer it works on: the
  buyer panel's cards and tally, the unit economics, the pricing curve and the plan compiler. They need nothing
  installed but Python 3. The board and the panel ask Claude Code to start helpers of its own, one per board member
  or buyer. In a chat app, your AI does the same work in the conversation and says what it could not run.
- **Keeps:** everything it makes in a `founder/` folder in your working folder, or in your chat where there are no
  files.
- **Sends:** nothing to us. Founder has no server, no account, no analytics and no tracking. What you type goes only
  to the AI app you use, as it always does.
- **Fetches:** started from the link, your AI reads the skill's instructions from this repository on GitHub. The
  install script downloads the release from GitHub. The skill's own helper scripts make no network
  requests. The competitor research reads public pages only when your AI can search the web, with links.

## Free and open source

Built by **[Brian MacDonald](https://github.com/bmacbuilds)**. [MIT license](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/LICENSE) · [Third-party notices](https://github.com/bmacbuilds/founder-skill/blob/v1.1.0/NOTICE)

Founder is free. Any usage limits or plan requirements are those of the AI app you use. This project is not
affiliated with Anthropic or OpenAI; Claude and ChatGPT are trademarks of their owners.
