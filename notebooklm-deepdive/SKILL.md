---
name: notebooklm-deepdive
description: Query NotebookLM grounded deal dossiers, citations, and neighborhood research for WholesaleOS properties.
---

# NotebookLM Knowledge Base Integration

This skill allows AI agents (Hermes, Claude, OpenCode, Gemini) to query NotebookLM grounded deal dossiers and extract cited property information.

Configure your own compatible backend at the example domain before using these commands. No hosted service or credentials are included.

## How to Query

1. **Search Knowledge Base**:
   ```bash
   curl -s "https://deals.example.com/api/notebooklm/search?q=<query>"
   ```

2. **Fetch Property Deep-Dive Dossier**:
   ```bash
   curl -s "https://deals.example.com/api/notebooklm/deepdive/<deal_id_or_address>"
   ```

3. **Trigger Knowledge Base Export**:
   ```bash
   curl -X POST "https://deals.example.com/api/notebooklm/export"
   ```

## Grounded Citation Format
When presenting NotebookLM research to buyers or operators:
- Include After-Repair Value (ARV) & Estimated Rehab Scope.
- Highlight distress flags and seller motivation notes.
- Cite the deal score ({score}/10) and net potential assignment spread.
