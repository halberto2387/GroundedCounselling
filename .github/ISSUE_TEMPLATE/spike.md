name: 🔍 Research Spike
description: Investigate a technical question or explore a solution
title: "[SPIKE] "
labels: ["type/spike", "status/triage"]
assignees:
  - halberto2387

body:
  - type: markdown
    attributes:
      value: |
        Research spikes help us investigate technical questions or explore potential solutions before implementation.

  - type: textarea
    id: summary
    attributes:
      label: Research Question
      description: What do you need to investigate or explore?
      placeholder: "What technical question needs to be answered?"
    validations:
      required: true

  - type: textarea
    id: acceptance-criteria
    attributes:
      label: Success Criteria
      description: What information or decisions should this spike produce?
      placeholder: |
        - [ ] Research outcome 1
        - [ ] Decision on approach
        - [ ] Documentation of findings
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: Context & Background
      description: Why is this research needed? What's the current situation?
      placeholder: "Provide context for why this investigation is needed..."
    validations:
      required: true

  - type: textarea
    id: scope
    attributes:
      label: Research Scope
      description: What should be included/excluded from this investigation?
      placeholder: |
        Include:
        - ...
        
        Exclude:
        - ...
    validations:
      required: false

  - type: textarea
    id: time-box
    attributes:
      label: Time Box
      description: How much time should be allocated to this research?
      placeholder: "e.g., 2 days, 1 week, etc."
    validations:
      required: false

  - type: textarea
    id: notes
    attributes:
      label: Additional Notes
      description: Any additional context, constraints, or resources.
      placeholder: "Include any relevant links, constraints, or resources..."
    validations:
      required: false

  - type: dropdown
    id: milestone
    attributes:
      label: Target Milestone
      description: When is this research needed?
      options:
        - M0 - Foundation
        - M1 - Core Platform
        - M2 - User Management
        - M3 - Booking System
        - M4 - Communications
        - M5 - Compliance & Security
        - M6 - Analytics & Reporting
        - M7 - Advanced Features
      default: 0
    validations:
      required: false

  - type: dropdown
    id: area
    attributes:
      label: Area
      description: Which part of the system does this research relate to?
      options:
        - area/frontend
        - area/backend
        - area/infra
        - area/docs
        - area/security
        - area/compliance
      default: 0
    validations:
      required: true

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: How urgent is this research?
      options:
        - priority/P0 - Critical
        - priority/P1 - High
        - priority/P2 - Medium
        - priority/P3 - Low
      default: 2
    validations:
      required: true