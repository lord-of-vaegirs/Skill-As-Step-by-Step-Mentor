/**
 * Contract tests for the DeepSeek Harness skill provider.
 *
 * Run with `node --test tests/provider.test.mjs`.
 */

import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { after, test } from "node:test";
import { fileURLToPath } from "node:url";

import {
	BUNDLED_SKILL_RANK,
	PROVIDER_NAME,
	SKILL_NAME,
	apply,
	createProvider,
	frontmatterField,
	skillBody,
} from "../lib/index.js";

const PACKAGE_ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const scratch = [];

/** Create a throw-away skill bundle for one test. */
function bundle(files) {
	const dir = mkdtempSync(join(tmpdir(), "step-mentor-"));
	scratch.push(dir);
	for (const [name, content] of Object.entries(files)) {
		const path = join(dir, name);
		mkdirSync(dirname(path), { recursive: true });
		writeFileSync(path, content, "utf8");
	}
	return dir;
}

/** A minimal skill file with the given frontmatter value. */
function skillFile(description) {
	return `---\nname: ${SKILL_NAME}\ndescription: ${description}\n---\n\n# Body\n\nInstructions.\n`;
}

after(() => {
	for (const dir of scratch) rmSync(dir, { recursive: true, force: true });
});

test("apply registers one provider over the packaged bundle", async () => {
	const registered = [];
	apply({ skills: { registerProvider: (create) => registered.push(create()) } });
	assert.equal(registered.length, 1);

	const provider = registered[0];
	assert.equal(provider.name, PROVIDER_NAME);

	const candidates = await provider.list();
	assert.equal(candidates.length, 1);

	const [candidate] = candidates;
	assert.equal(candidate.name, SKILL_NAME);
	assert.equal(candidate.provider, PROVIDER_NAME);
	assert.equal(candidate.source, "bundled");
	assert.equal(candidate.rank, BUNDLED_SKILL_RANK);
	assert.deepEqual(candidate.invocation, { modelInvocable: true, userInvocable: true });
	assert.equal(candidate.path, join(PACKAGE_ROOT, "SKILL.md"));
	assert.equal(candidate.resourceBase.kind, "directory");
	assert.ok(candidate.description.length > 0);
	assert.ok(candidate.description.length <= 500);

	const skill = await provider.get(candidate, {});
	assert.equal(skill.name, candidate.name);
	assert.ok(skill.content.startsWith("# Skill As Step by Step Mentor"));
	assert.ok(!skill.content.startsWith("---"));
	assert.notEqual(skill.content, "");
});

test("apply rejects a bundle without a single-line description", () => {
	const dir = bundle({ "SKILL.md": "---\nname: x\n---\n\n# Body\n" });
	assert.throws(
		() => apply({ skills: { registerProvider: () => {} } }, { skillDir: dir }),
		/no single-line description/u,
	);
});

test("an absent bundle yields an empty catalog instead of an error", async () => {
	const dir = join(tmpdir(), "step-mentor-missing-bundle");
	rmSync(dir, { recursive: true, force: true });
	const provider = createProvider({ skillDir: dir });
	assert.deepEqual(await provider.list(), []);
	assert.equal(await provider.get({ description: "x" }, {}), undefined);
});

test("a description edited on disk reaches the next catalog and load", async () => {
	const dir = bundle({ "SKILL.md": skillFile("First description.") });
	const provider = createProvider({ skillDir: dir });
	const [before] = await provider.list();
	assert.equal(before.description, "First description.");

	writeFileSync(join(dir, "SKILL.md"), skillFile("Second description."), "utf8");
	const [afterEdit] = await provider.list();
	assert.equal(afterEdit.description, "Second description.");

	const skill = await provider.get(afterEdit, {});
	assert.equal(skill.description, "Second description.");
	assert.equal(skill.content, "# Body\n\nInstructions.");
});

test("frontmatter decoding accepts plain, double-quoted, and single-quoted scalars", () => {
	const plain = skillFile("Plain text: with a colon.");
	assert.equal(frontmatterField(plain, "description"), "Plain text: with a colon.");
	assert.equal(frontmatterField(skillFile('"Quoted \\"inner\\" value"'), "description"), 'Quoted "inner" value');
	assert.equal(frontmatterField(skillFile("'It''s quoted'"), "description"), "It's quoted");
	assert.equal(frontmatterField(skillFile("").replace("description: \n", "description:\n"), "description"), undefined);
	assert.equal(frontmatterField("# no frontmatter\n", "description"), undefined);
});

test("skillBody drops the frontmatter block only", () => {
	assert.equal(skillBody(skillFile("x")), "# Body\n\nInstructions.");
	assert.equal(skillBody("# Plain body\n"), "# Plain body");
});
