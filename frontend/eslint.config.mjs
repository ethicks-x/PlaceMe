import pluginOxfmt from "eslint-plugin-oxfmt";

export default [
  {
    ...pluginOxfmt.configs.recommended,
    files: ["**/*.{js,ts,mjs,cjs,jsx,tsx,vue}"],
    rules: {
      "oxfmt/oxfmt": [
        "error",
        {
          // Plugin options
          useConfig: false,
          configPath: "./.oxfmtrc.json",

          // Formatting options
          semi: false,
          singleQuote: true,
          tabWidth: 2,
          useTabs: false,
          trailingComma: "all",
          printWidth: 100,
          arrowParens: "avoid",

          // File handling
          ignorePatterns: ["**/dist/**", "**/.next/**"],

          // Object formatting
          bracketSpacing: true,
          quoteProps: "as-needed",
          objectWrap: "preserve",

          // Line endings
          endOfLine: "lf",
          insertFinalNewline: true,

          // Prose / HTML
          embeddedLanguageFormatting: "auto",
          htmlWhitespaceSensitivity: "css",
          proseWrap: "preserve",

          // JSDoc
          jsdoc: {
            commentLineStrategy: "singleLine",
            lineWrappingStyle: "greedy",
            separateTagGroups: false,
          },

          // Vue
          vueIndentScriptAndStyle: false,

          // Advanced
          sortImports: {
            order: "asc",
            newlinesBetween: true,
          },
          sortPackageJson: { sortScripts: true },
          sortTailwindcss: {
            attributes: ["class", "className", ":class"],
            functions: ["clsx", "cn"],
            preserveDuplicates: false,
            preserveWhitespace: false,
          },
        },
      ],
    },
  },
];
