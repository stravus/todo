from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

def replace_once(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    s = s.replace(old, new, 1)

replace_once("<title>Doctrin Todo</title>", "<title>Todo</title>", "page title")

replace_once(
    '.brand{font-weight:780;font-size:22px;letter-spacing:-.025em;padding:0 12px 20px}.brand span{color:var(--accent)}',
    '.brand{display:flex;align-items:center;gap:10px;font-weight:780;font-size:22px;letter-spacing:-.025em;padding:0 12px 20px}.brand-mark{width:32px;height:32px;border-radius:11px;background:linear-gradient(145deg,#ff765f 0%,#df503d 55%,#bd372b 100%);box-shadow:0 6px 16px rgba(183,73,59,.24),inset 0 1px 0 rgba(255,255,255,.35);position:relative;flex:none;transform:rotate(-3deg)}.brand-mark:before{content:"";position:absolute;left:9px;top:7px;width:9px;height:14px;border:solid #fff;border-width:0 3px 3px 0;transform:rotate(45deg)}.brand-mark:after{content:"";position:absolute;right:5px;top:5px;width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,.7)}.brand-word{font-weight:820;letter-spacing:-.045em;color:var(--text)}',
    "brand css",
)

replace_once(
    '<div class="brand">Doctrin <span>Todo</span></div>',
    '<div class="brand" aria-label="Todo"><span class="brand-mark" aria-hidden="true"></span><span class="brand-word">Todo</span></div>',
    "brand markup",
)

replace_once('const APP_VERSION="4.2.0";', 'const APP_VERSION="4.2.1";', "app version")

replace_once(
    'const VERSION_HISTORY=[\n {version:"4.2.0",date:"2026-08-16",text:"Development jobs from backlog plus local friction monitoring for repeated/no-op actions, undo/toggle loops, edit churn, navigation bounce, failed searches and sync trouble."},',
    'const VERSION_HISTORY=[\n {version:"4.2.1",date:"2026-08-16",text:"Neutral Todo branding with a new checkmark logo; removed Doctrin from the visible app identity while retaining compatibility keys."},\n {version:"4.2.0",date:"2026-08-16",text:"Development jobs from backlog plus local friction monitoring for repeated/no-op actions, undo/toggle loops, edit churn, navigation bounce, failed searches and sync trouble."},',
    "version history",
)

s = s.replace('app:"Doctrin Todo"', 'app:"Todo"')
replace_once(
    '<div class="selftest"><h1>Doctrin Todo v${APP_VERSION} self-test</h1>',
    '<div class="selftest"><h1>Todo v${APP_VERSION} self-test</h1>',
    "selftest heading",
)
replace_once(
    'await test("Current version is 4.2.0",()=>assert(VERSION_HISTORY[0].version==="4.2.0"));',
    'await test("Current version is 4.2.1",()=>assert(VERSION_HISTORY[0].version==="4.2.1"));',
    "version selftest",
)

if "Doctrin Todo" in s:
    raise SystemExit("visible legacy product name remains")
if 'const STORAGE_KEY="doctrin-things-todo-v1";' not in s:
    raise SystemExit("storage compatibility key changed unexpectedly")
if 'const DATA_VERSION=6;' not in s:
    raise SystemExit("data schema changed unexpectedly")

p.write_text(s, encoding="utf-8")
print(f"Patched {len(s)} bytes")
