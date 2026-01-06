---
description: "Task list for feature implementation"
---

# Tasks: Physical AI & Humanoid Robotics — Essentials Textbook with RAG Chatbot

**Input**: Design documents from `/specs/001-textbook-rag/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with `frontend` and `backend` directories.
- [ ] T002 [P] Initialize Docusaurus project in `frontend/`.
- [ ] T003 [P] Initialize FastAPI project in `backend/`.
- [ ] T004 [P] Configure linting and formatting tools for both projects.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T005 Create a service in `backend/src/services/` to load and parse the textbook content from Markdown files.
- [ ] T006 [P] Set up Qdrant client and collection in `backend/src/services/`.

---

## Phase 3: User Story 1 - Read Textbook Content (Priority: P1) 🎯 MVP

**Goal**: As a learner, I want to access and read the textbook chapters in a clean and organized Docusaurus UI.

**Independent Test**: Can be fully tested by navigating to any chapter and verifying content display and navigation.

### Implementation for User Story 1

- [ ] T007 [US1] Implement the Docusaurus UI in `frontend/src/pages/` to display the textbook chapters.
- [ ] T008 [US1] Implement the sidebar navigation in `frontend/src/components/` based on the parsed textbook content.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Ask AI about Textbook Content (Priority: P1)

**Goal**: As a learner, I want to ask the RAG chatbot questions related to the textbook content and receive accurate answers derived only from the book.

**Independent Test**: Can be fully tested by asking questions about the book content and verifying the accuracy and source-limited nature of the answers.

### Implementation for User Story 2

- [ ] T009 [US2] Implement the RAG service in `backend/src/services/rag_service.py` to generate embeddings and retrieve documents from Qdrant.
- [ ] T010 [US2] Implement the `/query` endpoint in `backend/src/api/main.py` to handle chatbot requests.
- [ ] T011 [US2] Integrate the RAG service with the `/query` endpoint.
- [ ] T012 [P] [US2] Create the chatbot UI component in `frontend/src/components/Chatbot.js`.
- [ ] T013 [US2] Integrate the chatbot UI with the backend `/query` API.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Select Text and Ask AI (Priority: P2)

**Goal**: As a learner, I want to select a specific passage of text within a chapter and directly ask the AI questions about that selected text.

**Independent Test**: Can be fully tested by selecting a text snippet, activating the "Ask AI" feature, and getting a relevant response.

### Implementation for User Story 3

- [ ] T014 [US3] Implement the "select text" feature in the frontend to capture the selected text.
- [ ] T015 [US3] Integrate the "select text" feature with the chatbot UI component in `frontend/src/components/Chatbot.js` to pre-populate the query.

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T016 Deploy the Docusaurus site to GitHub Pages.
- [ ] T017 Verify that the application operates within the free-tier limits of all services.
- [ ] T018 [P] Perform a final review of the UI and functionality for any bugs or inconsistencies.
- [ ] T019 [P] Documentation updates in `docs/`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P1)**: Can start after Foundational (Phase 2). Depends on US1 for the UI context but can be developed in parallel.
- **User Story 3 (P2)**: Depends on User Story 2 completion.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational
3.  Complete Phase 3: User Story 1
4.  Complete Phase 4: User Story 2
5.  **STOP and VALIDATE**: Test User Stories 1 & 2.
6.  Deploy/demo if ready.
