---
id: {{ID}}
title: {{TITLE}}
stage: {{STAGE}}
date: {{DATE_ISO}}
surface: {{SURFACE}}
model: {{MODEL}}
feature: {{FEATURE}}
branch: {{BRANCH}}
user: {{USER}}
command: {{COMMAND}}
<<<<<<< HEAD
labels: {{LABELS_YAML}}
links:
  spec: {{LINK_SPEC}}
  ticket: {{LINK_TICKET}}
  adr: {{LINK_ADR}}
  pr: {{LINK_PR}}
=======
labels: [{{LABELS}}]
links:
  spec: {{LINKS_SPEC}}
  ticket: {{LINKS_TICKET}}
  adr: {{LINKS_ADR}}
  pr: {{LINKS_PR}}
>>>>>>> a669881 (Initial commit from Specify template)
files:
{{FILES_YAML}}
tests:
{{TESTS_YAML}}
---
<<<<<<< HEAD
## Prompt{{PROMPT_TEXT}}## Response snapshot{{RESPONSE_TEXT}}## Outcome- ✅ Impact: {{OUTCOME_IMPACT}}- 🧪 Tests: {{TESTS_SUMMARY}}- 📁 Files: {{FILES_SUMMARY}}- 🔁 Next prompts: {{NEXT_PROMPTS}}- 🧠 Reflection: {{REFLECTION_NOTE}}## Evaluation notes (flywheel)- Failure modes observed: {{FAILURE_MODES}}- Graders run and results (PASS/FAIL): {{GRADER_RESULTS}}- Prompt variant (if applicable): {{PROMPT_VARIANT_ID}}- Next ex
=======

## Prompt

{{PROMPT_TEXT}}

## Response snapshot

{{RESPONSE_TEXT}}

## Outcome

- ✅ Impact: {{OUTCOME_IMPACT}}
- 🧪 Tests: {{TESTS_SUMMARY}}
- 📁 Files: {{FILES_SUMMARY}}
- 🔁 Next prompts: {{NEXT_PROMPTS}}
- 🧠 Reflection: {{REFLECTION_NOTE}}

## Evaluation notes (flywheel)

- Failure modes observed: {{FAILURE_MODES}}
- Graders run and results (PASS/FAIL): {{GRADER_RESULTS}}
- Prompt variant (if applicable): {{PROMPT_VARIANT_ID}}
- Next experiment (smallest change to try): {{NEXT_EXPERIMENT}}
>>>>>>> a669881 (Initial commit from Specify template)
