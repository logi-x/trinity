/** @type {import("prettier").Config} */
const config = {
	printWidth: 100,
	semi: true,
	useTabs: false,
	singleQuote: false,
	bracketSameLine: false,
	bracketSpacing: true,
	tabWidth: 2,
	trailingComma: "all",
	// plugins: [require.resolve("prettier-plugin-tailwindcss")],
	overrides: [
		{
			files: "**/*.{js,jsx}",
			options: {
				parser: "babel",
				bracketSameLine: true,
				bracketSpacing: true,
				jsxSingleQuote: true,
				printWidth: 120,
				useTabs: true,
				tabWidth: 2,
				trailingComma: "es5",
			},
		},
		{
			files: "**/*.{ts,tsx}",
			options: {
				parser: "babel-ts",
				endOfLine: "auto",
				arrowParens: "always",
			},
		},
		{
			files: "**/*.css",
			options: {
				parser: "css",
				semi: false,
				singleQuote: false,
				trailingComma: "none",
			},
		},
		{
			files: "**/*.scss",
			options: {
				bracketSpacing: true,
				htmlWhitespaceSensitivity: "css",
				parser: "scss",
				singleQuote: false,
				trailingComma: "none",
				useTabs: false,
			},
		},
		{
			files: "**/*.json",
			options: {
				parser: "json",
				semi: false,
				singleQuote: true,
				trailingComma: "none",
			},
		},
		{
			files: "**/*.md",
			options: {
				parser: "markdown",
				printWidth: 80,
				semi: true,
				tabWidth: 2,
				singleQuote: false,
				trailingComma: "all",
			},
		},
	],
};
module.exports = config;
