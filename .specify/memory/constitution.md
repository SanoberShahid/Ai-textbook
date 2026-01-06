<<<<<<< HEAD
# Constitution: Physical AI & Humanoid Robotics Textbook

This document outlines the guiding principles, architectural decisions, and core tenets for the AI-Native textbook on Physical AI & Humanoid Robotics.

## 1. Project Vision

To create a clean, professional, and accessible AI-native textbook that serves as a foundational resource for learning about Physical AI and Humanoid Robotics. The book will be designed from the ground up to be "AI-native," meaning it will be interactive, always up-to-date, and optimized for machine-augmented learning.

## 2. Core Principles

These principles guide our development and architectural choices.

*   **Simplicity:** The content and architecture will be easy to understand and maintain. We prefer simple solutions over complex ones.
*   **Accuracy:** All information in the textbook must be fact-checked, correct, and up-to-date.
*   **Minimalism:** We will avoid unnecessary features, dependencies, and complexity. The project should remain lightweight and focused.
*   **Fast Builds:** The textbook and any accompanying code or examples must build and deploy quickly. This enables rapid iteration and contributions.
*   **Free-Tier Architecture:** The entire project must be hostable on free-tier services. This ensures accessibility and longevity without incurring costs.
*   **RAG Answers ONLY from Book Text:** The Retrieval-Augmented Generation (RAG) system for the interactive Q&A feature will *only* use the textbook's content as its knowledge source. This prevents hallucinations and ensures all answers are grounded in the material.

## 3. Mandates

*   **Free-tier Friendly:** All technologies and platforms used must have a generous free tier, avoiding any vendor lock-in or future costs.
*   **Lightweight Embeddings:** For the RAG system, we will use lightweight embedding models that are efficient and can run on low-resource infrastructure.

## 4. Key Features

*   **Documentation as Code:** The entire textbook is written in Markdown and managed through Git. This allows for version control, collaboration, and automated checks.
*   **Interactive Q&A:** An integrated AI-powered chat interface that allows students to ask questions and get answers sourced directly from the textbook content (leveraging the RAG principle).
*   **Code Examples:** All code examples will be executable and testable directly within the platform where possible.

## 5. Architecture & Stack

*   **Frontend:** Docusaurus with React.
*   **Content:** Markdown files stored in the repository.
*   **AI/RAG:** A lightweight, self-hosted RAG implementation using a free-tier friendly embedding model and a simple vector store.
*   **Deployment:** Vercel or a similar platform with a generous free tier.

This constitution is a living document. Any proposed changes should be discussed and approved by the project maintainers.
=======
# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

### [PRINCIPLE_6_NAME]


[PRINCIPLE__DESCRIPTION]

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
>>>>>>> a669881 (Initial commit from Specify template)
