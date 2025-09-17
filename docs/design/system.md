````markdown
# GroundedCounselling Design System

A comprehensive design system for the GroundedCounselling platform, focused on accessibility, professionalism, and trust.

## Brand Philosophy

### Core Values
- **Trust & Safety**: Professional, secure, and reliable
- **Accessibility**: Inclusive design for all users
- **Warmth**: Approachable and human-centered
- **Clarity**: Clear communication and simple interactions

### Design Principles
1. **Accessibility First**: WCAG 2.1 AA compliance as a baseline
2. **Progressive Disclosure**: Show information when needed
3. **Consistent Patterns**: Familiar interactions across the platform
4. **Inclusive Design**: Works for diverse users and abilities
5. **Professional Warmth**: Balance between clinical and friendly

## Color System

### Primary Palette

#### Evergreen (#2E6F4E)
**Usage**: Primary actions, links, focus states, branding
- **50**: #f0f9f4
- **100**: #dcf2e4
- **200**: #bce4cd
- **300**: #8dd0ab
- **400**: #56b382
- **500**: #2E6F4E (Primary)
- **600**: #265a40
- **700**: #1f4832
- **800**: #1a3a29
- **900**: #162f22

**Meaning**: Growth, healing, stability, nature

#### Sand (#F5F1EA)
**Usage**: Page backgrounds, card surfaces, subtle sections
- **50**: #fefffe
- **100**: #fdfdfc
- **200**: #faf8f6
- **300**: #f7f4f0
- **400**: #f6f2ed
- **500**: #F5F1EA (Primary)
- **600**: #e6e1d6
- **700**: #d7d0c2
- **800**: #c8bfae
- **900**: #b9ae9a

**Meaning**: Calm, neutral, grounding

### Secondary Palette

#### Charcoal (#1E1E1E)
**Usage**: Primary text, headings, high contrast elements
- **50**: #f7f7f7
- **100**: #e3e3e3
- **200**: #c8c8c8
- **300**: #a4a4a4
- **400**: #818181
- **500**: #666666
- **600**: #515151
- **700**: #434343
- **800**: #383838
- **900**: #1E1E1E (Primary)

#### Slate (#6B7280)
**Usage**: Secondary text, muted elements, placeholders
- **50**: #f8fafc
- **100**: #f1f5f9
- **200**: #e2e8f0
- **300**: #cbd5e1
- **400**: #94a3b8
- **500**: #6B7280 (Primary)
- **600**: #475569
- **700**: #334155
- **800**: #1e293b
- **900**: #0f172a

#### Sky (#3BA6FF)
**Usage**: Interactive elements, information, accents
- **50**: #eff9ff
- **100**: #daf2ff
- **200**: #bee9ff
- **300**: #92dcff
- **400**: #5fc6fd
- **500**: #3BA6FF (Primary)
- **600**: #1d85e0
- **700**: #1669b5
- **800**: #185796
- **900**: #1a497c

### Semantic Colors

#### Success (Green)
**Usage**: Success states, confirmations, positive feedback
- **500**: #22c55e
- **Background**: #f0fdf4
- **Border**: #bbf7d0

#### Warning (Amber)
**Usage**: Warnings, caution states, important notices
- **500**: #eab308
- **Background**: #fefce8
- **Border**: #fef08a

#### Danger (Red)
**Usage**: Errors, destructive actions, critical alerts
- **500**: #ef4444
- **Background**: #fef2f2
- **Border**: #fecaca

#### Info (Blue)
**Usage**: Informational messages, neutral notifications
- **500**: #3b82f6
- **Background**: #eff6ff
- **Border**: #dbeafe

### Accessibility Considerations

#### Contrast Ratios
- **Normal text**: Minimum 4.5:1 contrast ratio
- **Large text**: Minimum 3:1 contrast ratio
- **UI components**: Minimum 3:1 contrast ratio

#### Color Usage Guidelines
- Never use color alone to convey information
- Provide alternative indicators (icons, text, patterns)
- Test with color blindness simulators
- Support high contrast mode

## Typography

### Font Families

#### Primary: Inter
**Usage**: UI text, body content, forms, navigation
- **Characteristics**: Highly legible, modern, optimized for screens
- **Weights**: 400 (Regular), 500 (Medium), 600 (Semibold), 700 (Bold)
- **Loading**: Variable font with `font-display: swap`

#### Secondary: Source Serif 4
**Usage**: Headings, marketing content, editorial text
- **Characteristics**: Warm, readable, professional serif
- **Weights**: 400 (Regular), 600 (Semibold), 700 (Bold)
- **Loading**: Variable font with `font-display: swap`

#### Monospace: JetBrains Mono
**Usage**: Code, technical content, data displays
- **Characteristics**: Clear distinction between characters
- **Weight**: 400 (Regular)

### Type Scale

```css
/* Base: 16px (1rem) */
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */
--font-size-5xl: 3rem;      /* 48px */
```

### Line Heights

```css
--line-height-tight: 1.25;
--line-height-snug: 1.375;
--line-height-normal: 1.5;
--line-height-relaxed: 1.625;
--line-height-loose: 2;
```

### Typography Hierarchy

#### Headings
- **H1**: Source Serif 4, 3rem (48px), Semibold, 1.25 line-height
- **H2**: Source Serif 4, 2.25rem (36px), Semibold, 1.25 line-height
- **H3**: Source Serif 4, 1.875rem (30px), Semibold, 1.375 line-height
- **H4**: Inter, 1.5rem (24px), Semibold, 1.375 line-height
- **H5**: Inter, 1.25rem (20px), Semibold, 1.5 line-height
- **H6**: Inter, 1.125rem (18px), Semibold, 1.5 line-height

#### Body Text
- **Large**: Inter, 1.125rem (18px), Regular, 1.625 line-height
- **Base**: Inter, 1rem (16px), Regular, 1.5 line-height
- **Small**: Inter, 0.875rem (14px), Regular, 1.5 line-height
- **Extra Small**: Inter, 0.75rem (12px), Regular, 1.5 line-height

## Spacing System

### Base Unit: 4px

```css
--spacing-0: 0px;
--spacing-1: 4px;      /* 0.25rem */
--spacing-2: 8px;      /* 0.5rem */
--spacing-3: 12px;     /* 0.75rem */
--spacing-4: 16px;     /* 1rem */
--spacing-5: 20px;     /* 1.25rem */
--spacing-6: 24px;     /* 1.5rem */
--spacing-8: 32px;     /* 2rem */
--spacing-10: 40px;    /* 2.5rem */
--spacing-12: 48px;    /* 3rem */
--spacing-16: 64px;    /* 4rem */
--spacing-20: 80px;    /* 5rem */
--spacing-24: 96px;    /* 6rem */
```

### Layout Spacing
- **Component padding**: 16px (spacing-4) or 24px (spacing-6)
- **Section spacing**: 48px (spacing-12) or 64px (spacing-16)
- **Page margins**: 24px (spacing-6) mobile, 32px (spacing-8) desktop

## Component Library

### Buttons

#### Primary Button
- **Background**: Evergreen-500
- **Text**: White
- **Border**: None
- **Border Radius**: 8px
- **Padding**: 12px 24px
- **Font**: Inter Medium, 16px
- **States**: Hover (Evergreen-600), Focus (ring), Disabled (50% opacity)

#### Secondary Button
- **Background**: Transparent
- **Text**: Evergreen-500
- **Border**: 1px solid Evergreen-500
- **Border Radius**: 8px
- **Padding**: 12px 24px
- **Font**: Inter Medium, 16px

#### Ghost Button
- **Background**: Transparent
- **Text**: Slate-700
- **Border**: None
- **Padding**: 12px 16px
- **Font**: Inter Medium, 16px
- **States**: Hover (background: Slate-100)

### Form Elements

#### Input Fields
- **Border**: 1px solid Slate-300
- **Border Radius**: 8px
- **Padding**: 12px 16px
- **Font**: Inter Regular, 16px
- **Focus**: Border Evergreen-500, ring shadow
- **Error**: Border Danger-500

#### Labels
- **Font**: Inter Medium, 14px
- **Color**: Charcoal-700
- **Margin**: 8px bottom

### Cards

#### Base Card
- **Background**: White
- **Border**: 1px solid Slate-200
- **Border Radius**: 12px
- **Padding**: 24px
- **Shadow**: 0 1px 3px rgba(0,0,0,0.1)

#### Elevated Card
- **Background**: White
- **Border**: None
- **Border Radius**: 12px
- **Padding**: 24px
- **Shadow**: 0 4px 6px rgba(0,0,0,0.1)

## Accessibility Guidelines

### WCAG 2.1 AA Compliance

#### Color and Contrast
- Text contrast ratio: 4.5:1 minimum
- Large text contrast ratio: 3:1 minimum
- UI component contrast ratio: 3:1 minimum
- Don't rely on color alone for meaning

#### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Visible focus indicators required
- Logical tab order
- Skip links for main content

#### Screen Reader Support
- Semantic HTML structure
- Proper heading hierarchy
- Alt text for images
- ARIA labels for complex interactions
- Form labels and error messages

#### Motion and Animation
- Respect `prefers-reduced-motion`
- Provide pause controls for auto-playing content
- Avoid seizure-inducing animations
- Use animation to enhance, not distract

### Implementation Guidelines

#### CSS Variables
```css
:root {
  /* Colors */
  --color-primary: #2E6F4E;
  --color-surface: #F5F1EA;
  --color-text: #1E1E1E;
  --color-muted: #6B7280;
  --color-accent: #3BA6FF;
  
  /* Typography */
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-family-serif: 'Source Serif 4', Georgia, serif;
  
  /* Spacing */
  --spacing-unit: 4px;
  
  /* Borders */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: #1E1E1E;
    --color-text: #F5F1EA;
    /* Adjust other colors as needed */
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  :root {
    --color-text: #000000;
    --color-surface: #ffffff;
    /* Increase contrast ratios */
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Usage Guidelines

### Do's
✅ Use the defined color palette consistently  
✅ Maintain proper contrast ratios  
✅ Follow the typography hierarchy  
✅ Test with assistive technologies  
✅ Provide alternative text for images  
✅ Use semantic HTML elements  

### Don'ts
❌ Create new colors outside the palette  
❌ Use color alone to convey information  
❌ Skip heading levels in hierarchy  
❌ Rely on hover states for essential functionality  
❌ Use placeholder text as labels  
❌ Ignore keyboard navigation  

## Tools and Resources

### Design Tools
- **Figma**: Design system components and tokens
- **Contrast Checker**: WebAIM Contrast Checker
- **Color Blindness**: Stark or Colorblinding.com

### Development Tools
- **Tailwind CSS**: Utility classes matching design tokens
- **Headless UI**: Accessible component primitives
- **Radix UI**: Unstyled, accessible components

### Testing Tools
- **axe-core**: Automated accessibility testing
- **Screen Readers**: NVDA, JAWS, VoiceOver
- **Keyboard Testing**: Manual navigation testing

---

**Version**: 1.0  
**Last Updated**: January 2024  
**Maintained By**: Design System Team  
**Review Cycle**: Quarterly
````