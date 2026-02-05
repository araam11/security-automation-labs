\# Offline SOC Pipeline (Normalizer → SOAR Simulator)



This pipeline runs \*\*entirely offline\*\* and produces a full SOC lifecycle artifact set:



1\. \*\*Normalize\*\* a mock Sentinel incident (raw JSON → normalized model)

2\. Generate an \*\*incident report\*\* (Markdown)

3\. Generate a \*\*SOAR response plan\*\* + \*\*decision trace\*\*



\## No cloud dependencies

\- ❌ No Azure

\- ❌ No Sentinel APIs

\- ❌ No tenant access

\- ✅ GitHub-only, mock-data-driven



\## How to run



From this folder:



```bash

python pipeline.py



