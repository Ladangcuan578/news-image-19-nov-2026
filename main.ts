// A working news-image-daily entry (Node 22, standard library only): its image
// is the entry.png beside this file, and the program copies it to
// /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB and
// 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const dst = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

// Self-check: the output must be a whole 1024x1024 PNG of at most 1 MiB.
const bytes = readFileSync(dst);
const size = statSync(dst).size;
if (size > 1048576) {
  throw new Error(`entry.png too large: ${size} bytes (cap 1048576)`);
}
// Full 8-byte PNG signature, IHDR chunk type, and trailing IEND chunk:
// the gate requires a whole PNG, not just a valid header.
const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < signature.length; i++) {
  if (bytes[i] !== signature[i]) {
    throw new Error('entry.png is not a PNG');
  }
}
if (bytes.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk');
}
const iend = bytes.subarray(size - 12);
if (iend.readUInt32BE(0) !== 0 || iend.toString('ascii', 4, 8) !== 'IEND') {
  throw new Error('entry.png has no trailing IEND chunk');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
console.log(`entry.png OK: 1024x1024, ${size} bytes`);
