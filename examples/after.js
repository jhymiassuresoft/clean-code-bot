/**
 * OUTPUT: SOLID refactor of `before.js` (same data and console output).
 *
 * S — Single responsibility: LineItem (data/line math), VipDiscountPolicy (discount rule),
 *     OrderBook (collection), OrderTotalsService (aggregation), ConsoleOrderReporter (I/O).
 * O — Open/closed: new discount rules = new policy class implementing DiscountPolicy.
 * L — Liskov: any DiscountPolicy can replace VipDiscountPolicy for OrderTotalsService.
 * I — Interface segregation: small DiscountPolicy typedef, not a fat interface.
 * D — Dependency inversion: OrderTotalsService depends on DiscountPolicy, not concrete VIP logic.
 *
 * Expected output (matches before.js):
 *   TOTAL: 42.5
 *   Widget x2
 *   Gadget x1
 */

/**
 * @typedef {{ discountFor: (line: LineItem) => number }} DiscountPolicy
 */

/** Represents one line on an order. */
class LineItem {
  /**
   * @param {string} name
   * @param {number} price
   * @param {number} qty
   * @param {boolean} [vip=false]
   */
  constructor(name, price, qty, vip = false) {
    this.name = name;
    this.price = price;
    this.qty = qty;
    this.vip = Boolean(vip);
  }

  /**
   * Subtotal before discounts (same as price * qty in before.js).
   * @returns {number}
   */
  baseAmount() {
    return this.price * this.qty;
  }
}

/**
 * Applies a 10% discount on VIP lines only (same rule as before.js calc()).
 */
class VipDiscountPolicy {
  /**
   * @param {number} rate e.g. 0.1 for 10%
   */
  constructor(rate) {
    this._rate = rate;
  }

  /**
   * @param {LineItem} line
   * @returns {number} Discount amount (non-negative).
   */
  discountFor(line) {
    if (!line.vip) return 0;
    return line.baseAmount() * this._rate;
  }
}

/** In-memory order lines; replaces global `orders`. */
class OrderBook {
  constructor() {
    /** @type {LineItem[]} @private */
    this._lines = [];
  }

  /** @param {LineItem} line */
  add(line) {
    this._lines.push(line);
  }

  /** @returns {readonly LineItem[]} */
  get lines() {
    return Object.freeze([...this._lines]);
  }
}

/**
 * Computes grand total using an injected discount policy.
 */
class OrderTotalsService {
  /**
   * @param {DiscountPolicy} discountPolicy
   */
  constructor(discountPolicy) {
    this._discountPolicy = discountPolicy;
  }

  /**
   * @param {OrderBook} book
   * @returns {number}
   */
  totalFor(book) {
    return book.lines.reduce((sum, line) => {
      const discount = this._discountPolicy.discountFor(line);
      return sum + line.baseAmount() - discount;
    }, 0);
  }
}

/**
 * Prints total and each line (same strings as before.js printReport).
 */
class ConsoleOrderReporter {
  /**
   * @param {OrderTotalsService} totalsService
   */
  constructor(totalsService) {
    this._totalsService = totalsService;
  }

  /**
   * @param {OrderBook} book
   */
  print(book) {
    const total = this._totalsService.totalFor(book);
    console.log("TOTAL: " + total);
    for (const line of book.lines) {
      console.log(line.name + " x" + line.qty);
    }
  }
}

const VIP_DISCOUNT_RATE = 0.1;

const book = new OrderBook();
book.add(new LineItem("Widget", 10, 2, false));
book.add(new LineItem("Gadget", 25, 1, true));

const policy = new VipDiscountPolicy(VIP_DISCOUNT_RATE);
const totals = new OrderTotalsService(policy);
const reporter = new ConsoleOrderReporter(totals);
reporter.print(book);
