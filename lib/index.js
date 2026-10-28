/**
 * DeepSeek Harness skill provider for Skill As Step by Step Mentor.
 *
 * The package root is also the skill bundle: `SKILL.md`, `references/`, and
 * `scripts/` ship with this module, so the provider registers one candidate and
 * serves the body straight from disk. It imports only Node built-ins, which
 * keeps a profile installation free of registry dependencies.
 *
 * @module dsh-skill-step-by-step-mentor
 */

import { readFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { dirname, join, sep } from "node:path";
import { fileURLToPath } from "node:url";

/** Cordis plugin name. */
export const name = "skill-step-mentor";

/** Service this plugin registers on. */
export const inject = ["skills"];

/** Provider name reported by skill inspection. */
export const PROVIDER_NAME = "step-mentor";

/** Skill name; the bundle directory carries the same name in both hosts. */
export const SKILL_NAME = "skill-as-step-by-step-mentor";

/**
 * Rank of a packaged skill provider. Mirrors `BUNDLED_SKILL_RANK` from
 * `@deepseek-ai/dsh-skill`, repeated here so the package has no runtime
 * dependency on the harness.
 */
export const BUNDLED_SKILL_RANK = 600;

/** Directory holding this package, and therefore this skill bundle. */
export const PACKAGE_ROOT = dirname(
	fileURLToPath(new URL("../package.json", import.meta.url)),
);

const FRONTMATTER = /^---\r?\n(?<yaml>[\s\S]*?)\r?\n---(?:\r?\n|$)/u;

/**
 * Read one scalar field from the YAML frontmatter.
 *
 * Only a single-line plain or quoted scalar is accepted, matching the contract
 * this repository enforces in `tests/test_harness_contract.py`; anything else
 * is reported as absent instead of guessed at.
 * @param raw - Complete `SKILL.md` text.
 * @param key - Frontmatter key to read.
 * @returns The decoded value, or undefined when the key is absent.
 */
export function frontmatterField(raw, key) {
	const match = FRONTMATTER.exec(raw);
	if (match?.groups?.yaml === undefined) return undefined;
	const pattern = new RegExp(`^${key}\\s*:(.*)$`, "u");
	for (const line of match.groups.yaml.split(/\r?\n/u)) {
		const found = pattern.exec(line);
		if (found === null) continue;
		const value = found[1].trim();
		if (value.length === 0) return undefined;
		if (value.startsWith('"') && value.endsWith('"') && value.length > 1) {
			return value.slice(1, -1).replaceAll("\\\\", "\\").replaceAll('\\"', '"');
		}
		if (value.startsWith("'") && value.endsWith("'") && value.length > 1) {
			return value.slice(1, -1).replaceAll("''", "'");
		}
		return value;
	}
	return undefined;
}

/**
 * Strip the frontmatter block from a skill body.
 * @param raw - Complete `SKILL.md` text.
 * @returns The instruction body without frontmatter.
 */
export function skillBody(raw) {
	const match = FRONTMATTER.exec(raw);
	return (match === null ? raw : raw.slice(match[0].length)).trim();
}

/**
 * Build the provider for one skill directory.
 * @param options - Skill bundle location.
 * @param options.skillDir - Absolute directory containing `SKILL.md`.
 * @returns A `ctx.skills` provider.
 */
export function createProvider(options) {
	const skillDir = options.skillDir;
	const skillPath = join(skillDir, "SKILL.md");
	const resourceBase = {
		kind: "directory",
		path: skillDir.split(sep).join("/"),
	};

	/** Read the skill file, distinguishing an absent bundle from a broken one. */
	async function readSkill(signal) {
		try {
			return await readFile(skillPath, { encoding: "utf8", signal });
		} catch (error) {
			if (error?.code === "ENOENT") return undefined;
			throw error;
		}
	}

	return {
		name: PROVIDER_NAME,
		async list() {
			const raw = await readSkill(undefined);
			if (raw === undefined) return [];
			const description = frontmatterField(raw, "description");
			if (description === undefined) {
				throw new Error(
					`${SKILL_NAME}: ${skillPath} has no single-line description in its frontmatter`,
				);
			}
			return [
				{
					name: SKILL_NAME,
					path: skillPath,
					description,
					invocation: { modelInvocable: true, userInvocable: true },
					source: "bundled",
					provider: PROVIDER_NAME,
					rank: BUNDLED_SKILL_RANK,
					resourceBase,
				},
			];
		},
		async get(candidate, providerOptions) {
			const raw = await readSkill(providerOptions?.signal);
			if (raw === undefined) return undefined;
			return {
				name: SKILL_NAME,
				path: skillPath,
				description: frontmatterField(raw, "description") ?? candidate.description,
				invocation: candidate.invocation,
				source: candidate.source,
				provider: candidate.provider,
				resourceBase,
				content: skillBody(raw),
			};
		},
	};
}

/**
 * Fail fast at mount time, so an unpacked or corrupted bundle reports its
 * problem instead of registering an empty catalog.
 * @param skillPath - Absolute `SKILL.md` path.
 */
function assertReadable(skillPath) {
	const raw = readFileSync(skillPath, "utf8");
	if (frontmatterField(raw, "description") === undefined) {
		throw new Error(
			`${SKILL_NAME}: ${skillPath} has no single-line description in its frontmatter`,
		);
	}
}

/**
 * Register the packaged skill on `ctx.skills`.
 * @param ctx - Cordis context carrying the skill registry.
 * @param config - Optional override; `skillDir` points at another bundle.
 */
export function apply(ctx, config) {
	const skillDir = config?.skillDir ?? PACKAGE_ROOT;
	assertReadable(join(skillDir, "SKILL.md"));
	ctx.skills.registerProvider(() => createProvider({ skillDir }));
}
