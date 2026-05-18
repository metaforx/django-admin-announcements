import js from "@eslint/js";

export default [
  {
    ignores: ["**/*.min.js"],
  },
  js.configs.recommended,
  {
    files: ["admin_announcements/static/admin_announcements/js/**/*.js"],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: "script",
      globals: {
        document: "readonly",
        localStorage: "readonly",
        URL: "readonly",
        window: "readonly",
      },
    },
  },
];
