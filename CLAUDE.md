# ClipIt Agent Pack

Read `AGENTS.md` in this directory for the full setup, verification, and working rules — it applies to Claude Code exactly as written.

Claude Code specific: if Node is available, prefer `npm install -g @clipit/cli`, store the key with `clipit auth set-key --stdin`, then `clipit agent install claude` — this writes a permission-scoped skill to `~/.claude/skills/clipit-cli/SKILL.md` rendered live from the user's actual API key permissions. Verify with `clipit videos list`.
