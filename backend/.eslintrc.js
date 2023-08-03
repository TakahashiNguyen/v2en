module.exports = {
	parser: '@typescript-eslint/parser',
	parserOptions: {
		project: 'tsconfig.json',
		sourceType: 'module',
	},
	plugins: [],
	root: true,
	env: {
		node: true,
		jest: true,
	},
	ignorePatterns: ['.eslintrc.js'],
	extends: [
		'eslint:recommended',
		'plugin:@typescript-eslint/recommended',
		'plugin:graphql/recommended',
		'plugin:import/recommended',
		'plugin:prettier/recommended',
	],
	plugins: [
		'@typescript-eslint',
		'graphql',
		'import',
		'prettier',
		'@typescript-eslint/eslint-plugin',
	],
	rules: {
		'@typescript-eslint/interface-name-prefix': 'off',
		'@typescript-eslint/explicit-function-return-type': 'on',
		'@typescript-eslint/no-explicit-any': 'off',
		'unused-imports/no-unused-imports': 'error',
		'@typescript-eslint/no-var-requires': 'off',
	},
};
