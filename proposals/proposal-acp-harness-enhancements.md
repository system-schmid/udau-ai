# Proposal: Enhanced ACP Harness Integration for OpenClaw

**Author:** UDAU
**Date:** 2026-03-29

## Context
The current ACP harness integration allows spawning codex/claude code sessions but lacks advanced features like:
- Automatic thread binding with session metadata
- Improved error handling for long-running tasks
- Better resource isolation for multi-agent workflows

## Proposed Changes
1. **Thread-bound session metadata** - Store session context in thread metadata for easier tracking
2. **Enhanced error recovery** - Implement watchdog timeouts and automatic retries
3. **Resource quotas** - Add CPU/memory limits for spawned agents
4. **Improved PR integration** - Auto-generate changelogs from session history

## Implementation Plan
- [ ] Update ACP router skill to handle metadata storage
- [ ] Add resource monitoring in sessions_spawn
- [ ] Implement error callback system
- [ ] Create PR automation scripts

## Risks
- Increased complexity in session management
- Potential performance overhead from monitoring

## Next Steps
1. Prototype metadata storage system
2. Test resource quotas with load scenarios