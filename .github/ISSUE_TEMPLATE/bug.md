name: 🐛 Bug Report
description: Report a bug or issue
title: "[BUG] "
labels: ["type/bug", "status/triage"]
assignees:
  - halberto2387

body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug! Please provide the following information to help us understand and fix the issue.

  - type: textarea
    id: summary
    attributes:
      label: Bug Summary
      description: A clear and concise description of what the bug is.
      placeholder: "Describe the bug..."
    validations:
      required: true

  - type: textarea
    id: steps-to-reproduce
    attributes:
      label: Steps to Reproduce
      description: Detailed steps to reproduce the behavior.
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. Scroll down to '...'
        4. See error
    validations:
      required: true

  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected Behavior
      description: What you expected to happen.
      placeholder: "I expected..."
    validations:
      required: true

  - type: textarea
    id: actual-behavior
    attributes:
      label: Actual Behavior
      description: What actually happened.
      placeholder: "Instead, what happened was..."
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Information about your environment.
      placeholder: |
        - OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
        - Browser: [e.g. Chrome 95, Firefox 94, Safari 15]
        - Device: [e.g. Desktop, Mobile, Tablet]
        - Version: [e.g. v1.0.0]
    validations:
      required: false

  - type: textarea
    id: notes
    attributes:
      label: Additional Notes
      description: Any additional context, screenshots, or logs.
      placeholder: "Include any relevant screenshots, logs, or additional context..."
    validations:
      required: false

  - type: dropdown
    id: severity
    attributes:
      label: Severity
      description: How severe is this bug?
      options:
        - Critical - System is unusable
        - High - Major functionality broken
        - Medium - Some functionality affected
        - Low - Minor issue or cosmetic
      default: 2
    validations:
      required: true

  - type: dropdown
    id: area
    attributes:
      label: Area
      description: Which part of the system is affected?
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
      description: How urgent is this fix?
      options:
        - priority/P0 - Critical
        - priority/P1 - High
        - priority/P2 - Medium
        - priority/P3 - Low
      default: 2
    validations:
      required: true