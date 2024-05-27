module.exports = {
	globDirectory: 'public/',
	globPatterns: [
		'**/*.{ico,png}'
	],
	swDest: 'public/sw.js',
	ignoreURLParametersMatching: [
		/^utm_/,
		/^fbclid$/
	]
};