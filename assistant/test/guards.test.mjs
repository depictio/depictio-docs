/* The worker's guardrails, exercised without Cloudflare bindings.
 *
 *     node assistant/test/guards.test.mjs
 *
 * These four functions are the ones standing between the model and a confident
 * wrong answer, so they are worth testing directly rather than only end to end.
 * They are pulled out of the source by name so the worker itself stays a single
 * file with no exports to keep in sync.
 */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const src = readFileSync(join(here, "..", "src", "worker.js"), "utf8");

const grab = (name) => {
  const start = src.indexOf(`function ${name}(`);
  if (start === -1) throw new Error(`${name} not found in worker.js`);
  let depth = 0;
  let i = src.indexOf("{", start);
  for (; i < src.length; i++) {
    if (src[i] === "{") depth++;
    else if (src[i] === "}" && --depth === 0) break;
  }
  return src.slice(start, i + 1);
};

const ISSUES_URL = "github.com/depictio/depictio/issues";
const mod = new Function(
  "ISSUES_URL",
  `${grab("outsideFences")}\n${grab("parseAnswer")}\n${grab("postProcess")}\n${grab("leaksUrl")}\n` +
    "return { parseAnswer, postProcess, leaksUrl };",
)(ISSUES_URL);

let pass = 0;
let fail = 0;
const check = (label, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  console.log(`${ok ? "  ok  " : "  FAIL"}  ${label}`);
  if (!ok) console.log(`        got  ${JSON.stringify(got)}\n        want ${JSON.stringify(want)}`);
  ok ? pass++ : fail++;
};

console.log("\nparseAnswer — a model that emits slightly-invalid JSON must not break the answer");
check("clean json", mod.parseAnswer('{"answer":"Use depictio-cli.","section_ids":["S1"]}'), {
  answer: "Use depictio-cli.",
  section_ids: ["S1"],
});
check("prose wrapped around the json", mod.parseAnswer('Sure!\n{"answer":"Hello","section_ids":[]}\nok'), {
  answer: "Hello",
  section_ids: [],
});
check(
  "unescaped quote inside answer — the most common failure shape",
  mod.parseAnswer('{"answer":"Set the "type" key.","section_ids":["S2"]}'),
  { answer: 'Set the "type" key.', section_ids: ["S2"] },
);
check("total garbage falls through to the canned reply", mod.parseAnswer("I am not JSON"), null);

console.log("\npostProcess — style rules enforced in code, so they hold every time");
check(
  "markdown link collapses to its label",
  mod.postProcess("See [Cross-DC Filtering](https://docs/x/) for more."),
  "See Cross-DC Filtering for more.",
);
check("stray excerpt markers dropped", mod.postProcess("As shown [S1] here [S12]."), "As shown  here .");
check("headings dropped", mod.postProcess("## Title\nBody text here."), "Title\nBody text here.");
check(
  "code fences are left exactly alone",
  mod.postProcess("Run:\n```bash\n# [S1] not a marker\ndepictio-cli run\n```"),
  "Run:\n```bash\n# [S1] not a marker\ndepictio-cli run\n```",
);

console.log("\nleaksUrl — fail closed; a surviving link voids the whole answer");
check("plain prose", mod.leaksUrl("Set project_type to advanced."), false);
check("the issues tracker is the one allowed url", mod.leaksUrl(`Open an issue at ${ISSUES_URL}.`), false);
check("a docs url leaks", mod.leaksUrl("See https://depictio.github.io/depictio-docs/stable/x/"), true);
check("a bare www leaks", mod.leaksUrl("Go to www.example.com now"), true);
check(
  "a url inside a code fence is content, not a citation",
  mod.leaksUrl("Configure it:\n```yaml\nurl: https://example.com/thing\n```"),
  false,
);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
