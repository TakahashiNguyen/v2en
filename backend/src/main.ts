const mainAPP = import('./main.mjs');

async function main() {
	(await mainAPP).bootstrap();
}

main();
