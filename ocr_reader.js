import fs from "fs/promises";
import path from "path";

/**
 * Read OCR text files from the output directory and return combined text.
 * Looks for files named page_*.txt and concatenates them in numeric order.
 */
export async function readOCRFromOutput(outputDir = "output") {
	const dir = path.resolve(process.cwd(), outputDir);
	let entries;
	try {
		entries = await fs.readdir(dir);
	} catch (e) {
		throw new Error(`Failed to read output directory '${dir}': ${e.message}`);
	}

	const pageFiles = entries
		.filter((n) => /^page_\d+\.txt$/.test(n))
		.sort((a, b) => {
			const na = parseInt(a.match(/page_(\d+)\.txt/)[1], 10);
			const nb = parseInt(b.match(/page_(\d+)\.txt/)[1], 10);
			return na - nb;
		});

	if (pageFiles.length === 0) {
		throw new Error(`No page_*.txt files found in ${dir}`);
	}

	const parts = [];
	for (const fname of pageFiles) {
		const p = path.join(dir, fname);
		const txt = await fs.readFile(p, "utf8");
		parts.push(txt);
	}

	return parts.join("\n\n");
}

export default readOCRFromOutput;
