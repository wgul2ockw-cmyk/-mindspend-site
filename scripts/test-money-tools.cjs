const { test } = require('node:test');
const assert = require('node:assert/strict');
const { calculate, cents } = require('../assets/money-tools.js');

test('monthly plan separates allocations from the reference split', () => {
  const r = calculate('budget', { income: 32000, fixed: 12000, variable: 8000, saving: 4000 });
  assert.equal(r.remaining, 800000);
  assert.equal(r.needs + r.wants + r.goals, r.income);
  assert.equal(calculate('budget', { income: 1, fixed: 2, variable: 0, saving: 0 }).remaining, -100);
});
test('savings schedule reaches the goal exactly with a smaller final payment', () => {
  for (const target of ['0.01', '1', '100', '30000']) {
    for (const months of [1, 3, 12, 1200]) {
      const r = calculate('savings', { target, saved: 0, months });
      assert.equal((r.payments - 1) * r.monthly + r.final, cents(target));
      assert.ok(r.payments <= months);
      assert.ok(r.final > 0 && r.final <= r.monthly);
    }
  }
  const r = calculate('savings', { target: 100, saved: 0, months: 3 });
  assert.equal(r.monthly, 3334); assert.equal(r.final, 3332);
  assert.deepEqual(calculate('savings', { target: 50, saved: 100, months: 12 }), { remaining: 0, monthly: 0, payments: 0, final: 0 });
});
test('equal split conserves the exact bill and tip across group sizes', () => {
  for (const bill of ['0', '0.01', '1000.01', '1000000000']) {
    for (const people of [1, 3, 7, 1000]) {
      for (const tip of [0, 7.5, 100]) {
        const r = calculate('split', { bill, people, tip });
        assert.equal(r.base * (people - r.extra) + (r.base + 1) * r.extra, r.total);
        assert.equal(r.total, cents(bill) + r.tip);
        assert.ok(r.extra >= 0 && r.extra < people);
      }
    }
  }
  assert.equal(calculate('split', { bill: 1200, people: 4, tip: 10 }).base, 33000);
});
test('blank, negative, nonfinite, overly precise, and out-of-range inputs are rejected', () => {
  for (const value of ['', ' ', -1, Infinity, NaN, '1.005', '1e3', '1,000', 1000000001]) assert.throws(() => cents(value));
  for (const people of [0, -1, 1.5, 1001, '', '3e0']) assert.throws(() => calculate('split', { bill: 100, people, tip: 0 }));
  for (const months of [0, -1, 2.5, 1201]) assert.throws(() => calculate('savings', { target: 100, saved: 0, months }));
  for (const tip of [-1, 101, Infinity, '']) assert.throws(() => calculate('split', { bill: 100, people: 3, tip }));
});
