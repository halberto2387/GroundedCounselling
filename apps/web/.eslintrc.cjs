module.exports = {
  extends: [
    "eslint:recommended",
    "next/core-web-vitals",
  ],
  env: {
    browser: true,
    es2022: true,
    node: true
  },
  rules: {
    "prefer-const": "error",
    "no-var": "error",
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  },
  ignorePatterns: [
    "node_modules/",
    ".next/",
    "out/",
    "dist/",
    "build/",
    "coverage/"
  ]
};