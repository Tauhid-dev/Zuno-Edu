---
name: zuno-object-storage
description: "Apply s3-compatible private storage adapter rules when the selected Zuno Edu chunk changes this boundary."
---
# S3-compatible private storage adapter

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/FILE_STORAGE_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Use private scoped bucket, random staging keys, immutable promoted versions and short-lived authorized downloads. Metadata remains PostgreSQL authority.

## Verification requirements
Test presign expiry/overwrite, checksum, size validation and orphan deletion races. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
