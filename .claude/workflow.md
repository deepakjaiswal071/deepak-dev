# Development Workflow Steps

## Execution Sequence
1. **Schema Generation Check**: Ensure backend data models strictly map to `.claude/schema.json`.
2. **Backend Construction**: Build FastAPI core, setup Pydantic verification, and implement LLM calling logic.
3. **Frontend Construction**: Build UI shell, add states for loading/error handling, and hook up the backend endpoint.
4. **Integration Validation**: Perform an end-to-end test execution by passing an actual user story to verify response accuracy.
