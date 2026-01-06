---
ID: 15
TITLE: Fix Docusaurus blog authors map error
STAGE: general
DATE_ISO: 2025-12-10
SURFACE: agent
MODEL: gemini-1.5-pro
FEATURE: none
BRANCH: main
USER: Pcw
COMMAND: "Fix Docusaurus blog authors map error. Generate a valid authors.yml with keys, names, titles, URLs, image paths for all referenced authors (e.g., 'sebastienlorber', 'yangshuntay') and provide example blog front matter using these keys correctly so the dev server starts without errors."
LABELS: ["docusaurus", "blog", "error", "authors"]
LINKS:
  SPEC: "null"
  TICKET: "null"
  ADR: "null"
  PR: "null"
FILES_YAML:
  - blog/authors.yml
  - example_blog_frontmatter.md
TESTS_YAML: []
PROMPT_TEXT: "Fix Docusaurus blog authors map error. Generate a valid authors.yml with keys, names, titles, URLs, image paths for all referenced authors (e.g., 'sebastienlorber', 'yangshuntay') and provide example blog front matter using these keys correctly so the dev server starts without errors."
RESPONSE_TEXT: "I have created the `blog/authors.yml` file with the specified authors and provided an example of how to correctly reference these authors in a blog post's front matter."
OUTCOME: Success
EVALUATION: The Docusaurus blog authors map error should be resolved.
---
