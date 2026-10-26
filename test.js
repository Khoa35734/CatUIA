/**
 * Test suite for dut-core-math-utils
 */
const assert = require('assert');
const { add } = require('./index');

console.log('--- STARTING UNIT TESTS FOR dut-core-math-utils ---');

const testCases = [
  { name: 'Cộng hai số nguyên dương: add(2, 3)', actual: add(2, 3), expected: 5 },
  { name: 'Cộng số âm: add(-5, -7)', actual: add(-5, -7), expected: -12 },
  { name: 'Cộng số dương và số âm: add(10, -4)', actual: add(10, -4), expected: 6 },
  { name: 'Cộng với số 0: add(0, 42)', actual: add(0, 42), expected: 42 },
  { name: 'Cộng hai số 0: add(0, 0)', actual: add(0, 0), expected: 0 },
  { name: 'Cộng số lớn: add(1_000_000, 2_000_000)', actual: add(1000000, 2000000), expected: 3000000 },
];

let passed = 0;
let failed = 0;

for (const tc of testCases) {
  try {
    assert.strictEqual(tc.actual, tc.expected);
    console.log(`[PASS] ${tc.name} => ${tc.actual}`);
    passed++;
  } catch (err) {
    console.error(`[FAIL] ${tc.name}: Expected ${tc.expected}, got ${tc.actual}`);
    failed++;
  }
}

// Float test with precision tolerance
const floatResult = add(0.1, 0.2);
if (Math.abs(floatResult - 0.3) < 1e-9) {
  console.log(`[PASS] Cộng số thực: add(0.1, 0.2) => ${floatResult.toFixed(2)} (xấp xỉ 0.3)`);
  passed++;
} else {
  console.error(`[FAIL] Cộng số thực: add(0.1, 0.2) => ${floatResult}`);
  failed++;
}

console.log(`--- TEST RESULTS: ${passed} PASSED, ${failed} FAILED ---`);
if (failed > 0) {
  process.exit(1);
}
