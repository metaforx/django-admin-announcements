export default {
  extends: ["stylelint-config-standard"],
  ignoreFiles: ["**/*.min.css"],
  rules: {
    "alpha-value-notation": null,
    "color-function-alias-notation": null,
    "color-function-notation": null,
    "selector-class-pattern": [
      "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:__[a-z0-9]+(?:-[a-z0-9]+)*)?(?:--[a-z0-9]+(?:-[a-z0-9]+)*)?$",
      {
        message: "Expected class selector to use kebab-case or BEM naming",
      },
    ],
  },
};
