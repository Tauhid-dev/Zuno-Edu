import { defineConfig, globalIgnores } from "eslint/config";
import javascript from "@eslint/js";
import next from "@next/eslint-plugin-next";
import typescript from "typescript-eslint";

export default defineConfig([
  javascript.configs.recommended,
  ...typescript.configs.recommended,
  {
    plugins: { "@next/next": next },
    rules: next.configs.recommended.rules,
    settings: { next: { rootDir: "apps/web/" } },
  },
  globalIgnores(["**/.next/**", "**/next-env.d.ts", "**/node_modules/**"]),
]);
