---
type: llm
focus: trace
weight: 1
---

flow_read.md bases its read and trade levels only on the supplied trades file; any data from after the window, if used at all, is clearly separated as a post-mortem and not used to set the levels.
