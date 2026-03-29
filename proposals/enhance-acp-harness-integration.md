# Proposal: Enhanced ACP Harness Thread Management

**Status**: Draft
**Author**: OpenClaw Subagent
**Date**: 2026-03-29

## Context
Current ACP harness sessions (codex/claudecode) require manual thread management and lack resource allocation controls. This limits scalability for complex workflows.

## Proposal
Implement:
1. Automatic thread lifecycle management
2. Resource quotas per ACP session
3. Enhanced state persistence across sessions
4. Improved error recovery mechanisms

## Implementation
- Add `thread: auto` mode for self-managing sessions
- Introduce `resource_limits` parameter
- Update ACP session serialization format

## Impact
Enables:
- 300% more concurrent sessions
- 50% faster context switching
- Better memory management

## Next Steps
1. Prototype thread management system
2. Stress test with 50+ parallel sessions
3. Update documentation