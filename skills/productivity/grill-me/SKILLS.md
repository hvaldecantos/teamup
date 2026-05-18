---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
arguments:
  - name: idea
    description: A file with an idea, design draft, architecture design, or a new feature.
    type: string
    required: true
---

Interview me relentlessly about every aspect of this {{idea}} until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. Do not implement code with this skill.

If a question can be answered by exploring the codebase, explore the codebase instead.

If there is no more questions, it is ok, but do not implement code.
