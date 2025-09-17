name: 🚀 Feature Request
description: Suggest a new feature or enhancement
title: "[FEATURE] "
labels: ["type/feature", "status/triage"]
assignees:
  - halberto2387

body:
  - type: markdown
    attributes:
      value: |
        Thank you for suggesting a feature! Please provide the following information to help us understand your request.

  - type: textarea
    id: summary
    attributes:
      label: Feature Summary
      description: A clear and concise description of the feature you'd like to see implemented.
      placeholder: "I would like to..."
    validations:
      required: true

  - type: textarea
    id: acceptance-criteria
    attributes:
      label: Acceptance Criteria
      description: Define what needs to be done for this feature to be considered complete.
      placeholder: |
        - [ ] Criterion 1
        - [ ] Criterion 2
        - [ ] Criterion 3
    validations:
      required: true

  - type: textarea
    id: user-story
    attributes:
      label: User Story
      description: Who will benefit from this feature and why?
      placeholder: "As a [user type], I want [goal] so that [benefit]"
    validations:
      required: false

  - type: textarea
    id: notes
    attributes:
      label: Additional Notes
      description: Any additional context, mockups, or technical considerations.
      placeholder: "Include any relevant details, mockups, or technical considerations..."
    validations:
      required: false

  - type: dropdown
    id: milestone
    attributes:
      label: Target Milestone
      description: When should this feature be implemented?
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
      description: Which part of the system does this affect?
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
      description: How important is this feature?
      options:
        - priority/P0 - Critical
        - priority/P1 - High
        - priority/P2 - Medium
        - priority/P3 - Low
      default: 2
    validations:
      required: true