import { lstat, rm } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const generatedPaths = [".next", "out"].map((directory) => path.resolve(projectRoot, directory));

for (const generatedPath of generatedPaths) {
  if (path.dirname(generatedPath) !== projectRoot) {
    throw new Error(`Refusing to clean a generated path outside the project: ${generatedPath}`);
  }

  try {
    const info = await lstat(generatedPath);
    if (info.isSymbolicLink() || !info.isDirectory()) {
      throw new Error(`Refusing to clean a non-directory generated path: ${generatedPath}`);
    }
    await rm(generatedPath, { recursive: true });
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
}
