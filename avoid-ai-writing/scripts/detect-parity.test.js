"use strict";

// Parity between the bundled ai-writing-detector script and the root CLI
// (#244). Both load detector/patterns.js, but detect.js had drifted: it could
// not reach rendered-Markdown mode, so a Markdown file with YAML frontmatter
// scored "Minimal AI signals" through detect.js and "Clean" through the root
// CLI, and passing the flag threw an uncaught "unknown argument" stack trace.

const assert = require("assert");
const { spawnSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const ROOT_CLI = path.join(__dirname, "..", "bin", "avoid-ai-writing.js");
const DETECT = path.join(__dirname, "..", "..", "ai-writing-detector", "scripts", "detect.js");

function run(cli, args) {
  return spawnSync(process.execPath, [cli, ...args], { encoding: "utf8" });
}

// The standalone skill carries two additional diagnostic counters. Compare
// the shared scoring contract while allowing those implementation-specific
// counters to remain available to callers of that skill.
function sharedResult(result) {
  const normalized = { ...result, stats: { ...result.stats } };
  delete normalized.stats.ignoredRegions;
  delete normalized.stats.maskedQuotes;
  if (result.label === "Empty" || result.tooShort || result.tooLong || result.unsupportedScript) {
    normalized.stats = {
      contextMode: result.stats.contextMode,
      sourceMode: result.stats.sourceMode,
    };
  }
  return normalized;
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "aaw-detect-"));
const draft = path.join(tmp, "draft.md");
fs.writeFileSync(
  draft,
  [
    "---",
    "title: Delve into the vibrant landscape",
    "description: A testament to seamless synergy",
    "tags: [draft]",
    "---",
    "",
    "The team met on Tuesday and agreed the next steps for the release.",
    "",
  ].join("\n"),
  "utf8",
);

// The same file and the same flags produce the same analysis through both entry
// points. The root CLI takes a positional path, detect.js takes --file; that
// difference is deliberate and stays.
//
// Every context the shared detector accepts is exercised here, because the
// bundled parser is a second copy of the root CLI's validation: a context the
// root CLI accepts but detect.js rejects is a parity break that only shows up
// on the invocation that uses it.
const CONTEXTS = ["general", "technical", "marketing", "personal"];

for (const context of CONTEXTS) {
  const rootOut = run(ROOT_CLI, ["--context", context, "--source-mode", "rendered-markdown", draft]);
  assert.strictEqual(rootOut.status, 0, `root CLI --context ${context}: ${rootOut.stderr}`);
  const detectOut = run(DETECT, ["--file", draft, "--context", context, "--source-mode", "rendered-markdown"]);
  assert.strictEqual(detectOut.status, 0, `detect.js --context ${context}: ${detectOut.stderr}`);
  assert.deepStrictEqual(
    sharedResult(JSON.parse(detectOut.stdout)),
    sharedResult(JSON.parse(rootOut.stdout)),
    `--context ${context} must agree between the two entry points`,
  );
  assert.strictEqual(JSON.parse(detectOut.stdout).stats.contextMode, context);
}

const detectOut = run(DETECT, ["--file", draft, "--context", "general", "--source-mode", "rendered-markdown"]);
assert.strictEqual(detectOut.status, 0, detectOut.stderr);
assert.strictEqual(JSON.parse(detectOut.stdout).stats.sourceMode, "rendered-markdown");

// The flag is not a no-op: plain mode still scores the YAML frontmatter as
// prose, which is the false positive rendered-markdown removes.
const plainOut = run(DETECT, ["--file", draft, "--context", "general"]);
assert.strictEqual(plainOut.status, 0, plainOut.stderr);
const plain = JSON.parse(plainOut.stdout);
const rendered = JSON.parse(detectOut.stdout);
assert.strictEqual(plain.stats.sourceMode, "plain");
assert.strictEqual(rendered.issues.length, 0, "rendered-markdown must not score the frontmatter");
assert.strictEqual(rendered.label, "Clean");
assert.ok(
  plain.issues.length > 0,
  "plain mode must still score the frontmatter, or this flag has nothing to remove",
);

// Blank input still reports the selected modes. analyzeText() returns an empty
// stats object for it, and the root CLI fills in contextMode and sourceMode;
// without the same normalization the bundled script returned stats: {} and the
// two entry points disagreed on an explicitly selected mode.
const blank = path.join(tmp, "blank.md");
fs.writeFileSync(blank, "", "utf8");
const whitespace = path.join(tmp, "whitespace.md");
fs.writeFileSync(whitespace, "   \n\t\n", "utf8");

for (const [label, blankFile] of [["empty", blank], ["whitespace-only", whitespace]]) {
  for (const sourceMode of ["plain", "rendered-markdown"]) {
    const rootOut = run(ROOT_CLI, ["--context", "marketing", "--source-mode", sourceMode, blankFile]);
    assert.strictEqual(rootOut.status, 0, `root CLI ${label} ${sourceMode}: ${rootOut.stderr}`);
    const detectOut = run(DETECT, ["--file", blankFile, "--context", "marketing", "--source-mode", sourceMode]);
    assert.strictEqual(detectOut.status, 0, `detect.js ${label} ${sourceMode}: ${detectOut.stderr}`);
    assert.deepStrictEqual(
      sharedResult(JSON.parse(detectOut.stdout)),
      sharedResult(JSON.parse(rootOut.stdout)),
      `${label} input with --source-mode ${sourceMode} must agree between the two entry points`,
    );
    const stats = JSON.parse(detectOut.stdout).stats;
    assert.strictEqual(stats.contextMode, "marketing", `${label}: selected context must stay visible`);
    assert.strictEqual(stats.sourceMode, sourceMode, `${label}: selected source mode must stay visible`);
  }
}

const cjk = path.join(tmp, "cjk.md");
fs.writeFileSync(cjk, "这个函数返回一个承诺，调用方不应假设句柄之后仍可重用。".repeat(50), "utf8");
const rootCjk = run(ROOT_CLI, [cjk]);
const detectCjk = run(DETECT, ["--file", cjk]);
assert.strictEqual(rootCjk.status, 0, rootCjk.stderr);
assert.strictEqual(detectCjk.status, 0, detectCjk.stderr);
assert.deepStrictEqual(sharedResult(JSON.parse(detectCjk.stdout)), sharedResult(JSON.parse(rootCjk.stdout)));
assert.strictEqual(JSON.parse(rootCjk.stdout).unsupportedScript, true);
assert.strictEqual(JSON.parse(rootCjk.stdout).label, "Unsupported script");

// Usage errors exit 2 with the usage message and no stack trace.
const errorCases = [
  ["unknown argument", ["--nope"]],
  ["missing --file value", ["--file"]],
  ["missing --context value", ["--context"]],
  ["invalid context", ["--context", "nope"]],
  ["missing --source-mode value", ["--source-mode"]],
  ["invalid source mode", ["--source-mode", "nope"]],
];

for (const [label, args] of errorCases) {
  const res = run(DETECT, args);
  assert.strictEqual(res.status, 2, `${label}: expected exit 2`);
  assert.strictEqual(res.stdout, "", `${label}: expected no stdout`);
  assert.ok(res.stderr.includes("Usage: detect.js"), `${label}: expected the usage message`);
  assert.ok(!/\n\s+at /.test(res.stderr), `${label}: expected no stack trace`);
}

// --help prints the usage and exits 0.
const help = run(DETECT, ["--help"]);
assert.strictEqual(help.status, 0);
assert.ok(help.stdout.includes("Usage: detect.js"));
assert.ok(help.stdout.includes("--source-mode <plain|rendered-markdown>"));

fs.rmSync(tmp, { recursive: true, force: true });
console.log("ai-writing-detector bundled script: ok");
