# Claude Code Subagents for Evolution of Todo

Custom subagents for the Spec-Driven Development workflow. Using these agents earns **+200 bonus points** for "Reusable Intelligence via Claude Code Subagents."

## Setup

Copy these files to your project:

```
your-project/.claude/agents/
├── spec-validator.md
├── spec-refiner.md
├── test-spec-writer.md
├── acceptance-checker.md
├── python-cli-agent.md
├── mcp-tool-builder.md
└── cloud-native-blueprint.md
```

Or use `/agents` command in Claude Code to create them.

## Available Subagents

### Core SDD Workflow

| Agent | Description | Use When |
|-------|-------------|----------|
| `spec-validator` | Validates specs against constitution | Before `/speckit.plan` |
| `spec-refiner` | Fixes specs when code gen fails | After failed generation |
| `test-spec-writer` | Creates test specs (test-first) | After `/speckit.specify` |
| `acceptance-checker` | Validates implementation | After `/speckit.implement` |

### Phase-Specific

| Agent | Phase | Description |
|-------|-------|-------------|
| `python-cli-agent` | I | Rich + Questionary patterns |
| `mcp-tool-builder` | III | MCP SDK tool creation |
| `cloud-native-blueprint` | IV, V | Docker/Helm/K8s patterns (+200 bonus) |

## Usage

Subagents are invoked automatically by Claude Code when appropriate, or explicitly:

```
Use the spec-validator subagent to check my Add Task spec

Have the acceptance-checker validate my implementation

Use python-cli-agent to show me table formatting patterns
```

## SDD Workflow Integration

```
/speckit.specify
       │
       ▼
┌─────────────────┐
│ spec-validator  │ ──── Valid? ──── NO ──► Refine spec
└────────┬────────┘
         │ YES
         ▼
┌──────────────────┐
│ test-spec-writer │
└────────┬─────────┘
         │
         ▼
   /speckit.plan
         │
         ▼
   /speckit.tasks
         │
         ▼
  /speckit.implement
         │
         ▼
┌────────────────────┐
│ acceptance-checker │ ─── Pass? ─── NO ──► spec-refiner
└────────┬───────────┘
         │ YES
         ▼
      ✅ DONE
```

## Bonus Points

- **+200 Reusable Intelligence:** Using these subagents consistently
- **+200 Cloud-Native Blueprints:** Using `cloud-native-blueprint` agent for Phase IV/V
