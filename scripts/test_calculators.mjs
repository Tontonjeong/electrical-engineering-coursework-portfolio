import assert from "node:assert/strict";
import { transformerCase } from "../docs/tools/transformer-case-calculator/transformer-case-calculator.js";
import { motorCurrentPi } from "../docs/tools/motor-pi-calculator/motor-pi-calculator.js";
import { lineCase } from "../docs/tools/transmission-line-calculator/transmission-line-calculator.js";

const transformer = transformerCase({
  output: 900,
  copper: 10.2267,
  core: 23.776,
  vnl: 111.2496,
  vfl: 110,
});
assert.ok(Math.abs(transformer.loss - 34.0027) < 1e-9);
assert.ok(Math.abs(transformer.efficiency - 96.3594644855) < 1e-8);
assert.ok(Math.abs(transformer.regulation - 1.136) < 1e-10);

const motor = motorCurrentPi({
  ra: 0.1,
  la: 0.02,
  j: 0.075,
  kt: 1.9,
  fcc: 500,
  fcs: 25,
});
assert.ok(Math.abs(motor.kpCurrent - 62.8318530718) < 1e-9);
assert.ok(Math.abs(motor.kiCurrent - 314.159265359) < 1e-9);
assert.ok(Math.abs(motor.inertiaTerm - 11.780972451) < 1e-9);

const line = lineCase({ vll: 765, x: 0.3, b: 4.6, length: 350 });
assert.ok(Math.abs(line.zc - 255.3769592276) < 1e-9);
assert.ok(Math.abs(line.silMW - 2291.6123747811) < 1e-8);
assert.ok(Math.abs(line.currentA - 1729.4941456969) < 1e-8);

for (const fn of [transformerCase, motorCurrentPi, lineCase]) {
  assert.throws(() => fn({}), /숫자/);
}

console.log("PASS calculators: transformer, motor PI, transmission line");
