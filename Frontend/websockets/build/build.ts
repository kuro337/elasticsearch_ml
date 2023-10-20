await Bun.build({
  entrypoints: ["../index.ts"],
  outdir: "./artifact",
  target: "browser", // default
});

// CLI - bun build ./index.tsx --outdir ./out
