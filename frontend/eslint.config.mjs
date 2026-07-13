import pluginOxfmt from 'eslint-plugin-oxfmt'

export default [
  {
    ...pluginOxfmt.configs.recommended,
    files: ['**/*.{js,ts,mjs,cjs,jsx,tsx,vue}'],
    rules: {
      'oxfmt/oxfmt': [
        'error',
        {
          // Tell ESLint to use your external configuration file directly
          useConfig: true,
          configPath: './.oxfmtrc.json',
        },
      ],
    },
  },
]
