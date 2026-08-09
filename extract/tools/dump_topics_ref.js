const fs = require("fs");
const path = require("path");
const vm = require("vm");

const dir = path.join(__dirname, "..", "..", "data", "topics");
const files = fs.readdirSync(dir).filter(f => f.startsWith("topic-") && f.endsWith(".js")).sort();
const sandbox = { console };
vm.createContext(sandbox);
let out = [];
let topics = [];
for (const f of files) {
  const src = fs.readFileSync(path.join(dir, f), "utf8");
  const m = src.match(/const (_t_\w+)\s*=\s*(\[)/);
  let s = src;
  if (m) s = src + "\n;globalThis.__dump = " + m[1] + ";\n";
  try {
    vm.runInContext(s, sandbox, { filename: f });
    if (sandbox.__dump) {
      for (const t of sandbox.__dump) topics.push(t);
      sandbox.__dump = null;
    }
  } catch (e) {
    out.push("EVAL FAIL " + f + " " + e.message);
    continue;
  }
}
let ref = [];
for (const t of topics) {
  ref.push("\n-- topic id=" + t.id + " name=" + t.name);
  for (const e of t.entries || []) {
    ref.push("  * " + e.concept);
  }
}
out.push("TOPICS=" + topics.length);
fs.writeFileSync(path.join(__dirname, "..", "generated_assets", "phase7d_topics_ref.txt"), out.join("\n") + "\n" + ref.join("\n"), "utf8");
console.log("wrote ref, topics:", topics.length);
