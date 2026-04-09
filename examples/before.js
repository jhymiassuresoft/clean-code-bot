/**
 * INPUT for The Clean Code Bot (Python CLI: `clean-code-bot`)
 *
 * This file is the “before” snapshot: messy, procedural code you pass to the tool.
 * Groq refactors it toward OOP + SOLID + JSDoc (see project `requirements.md`).
 *
 * Example (from repo root `clean-code-bot/`, venv active, `GROQ_API_KEY` set):
 *
 *   clean-code-bot examples/before.js -o examples/after.js
 *
 * Or print to stdout and redirect yourself:
 *
 *   clean-code-bot examples/before.js > examples/after.js
 *
 * ---
 * Scenario preserved by the refactor (same console output):
 * - Line A: Widget, price 10, qty 2, not VIP
 * - Line B: Gadget, price 25, qty 1, VIP → 10% off that line’s subtotal
 *
 * Expected output:
 *   TOTAL: 42.5
 *   Widget x2
 *   Gadget x1
 */

// Legacy: global state, no structure, magic numbers — typical refactor input.
var orders = [];

function add(o) {
  orders.push(o);
}

function calc() {
  var t = 0;
  for (var i = 0; i < orders.length; i++) {
    t = t + orders[i].price * orders[i].qty;
    if (orders[i].vip) {
      t = t - orders[i].price * orders[i].qty * 0.1;
    }
  }
  return t;
}

function printReport() {
  console.log("TOTAL: " + calc());
  for (var j = 0; j < orders.length; j++) {
    console.log(orders[j].name + " x" + orders[j].qty);
  }
}

add({ name: "Widget", price: 10, qty: 2, vip: false });
add({ name: "Gadget", price: 25, qty: 1, vip: true });
printReport();
