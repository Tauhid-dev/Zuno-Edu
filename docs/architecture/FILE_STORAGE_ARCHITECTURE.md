# File and object storage

FileAsset metadata is authoritative: UUID, purpose, owner student/family or course/cohort context, uploader, original display filename, generated staging key, immutable promoted key/version, declared/detected MIME, bytes, SHA-256, status, created/expires/deleted timestamps and scan result. Do not use user filenames as storage keys. LearningResource and Submission reference an asset only after CLEAN state; Certificate points to a generated private PDF.

| Purpose | Allowed types | Maximum | Who uploads | Who downloads |
|---|---|---|---|---|
| Student work | PDF, PNG, JPEG, TXT, constrained ZIP | 25 MiB per file, 100 MiB per submission | owner student | owner, guardian, currently assigned marker, education admin |
| Curriculum document/image | PDF, PNG, JPEG, TXT | 50 MiB | education admin | enrolled released-course users, assigned teacher; explicit public copy only if separately published |
| Learning video | MP4 | 500 MiB | education admin | released-course users and assigned staff |
| Certificate | generated PDF | 5 MiB | trusted worker | owner, guardian, education admin |
| Internal operational asset | PDF, PNG, JPEG, TXT | 25 MiB | privileged admin | matching admin privilege only |

FileService initiates authorized upload intent with immutable owner/context and random staging key. Signed upload expires in 5 minutes and binds content type/checksum where supported. Apply storage policy length range or server streaming limit; independently HEAD/check bytes on completion. Browser report is insufficient. CompleteUpload checks expected key, actual size/type, checksum; scanner in quarantine reads without executing. ZIP limits: <=100 entries, <=100 MiB expanded, <=20:1 expansion ratio; reject encrypted entries, symlinks, traversal paths, executables and nested archives. Reject active SVG/HTML and office macro formats. Failed/unknown scans are not downloadable.

Promotion copies verified bytes to new immutable key with version/checksum binding. Original staging presign can remain valid briefly, so never serve staging or let replacement bytes overwrite approved objects. Database transition CLEAN records immutable version only after promotion verified. Server authorizes purpose/ownership/release for every download and returns 60-second presign with attachment disposition except safe image/video delivery. Signed URLs are bearer secrets and cannot be instantly revoked; very short expiry bounds access after revocation. Content Security Policy restricts safe renderers, never embeds arbitrary uploaded HTML. [S3 presigned behavior](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html), [OWASP file handling](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html).

Delete marks asset pending-deletion, refuses new URLs, removes references per retention policy, queues deletion of all object versions after legal hold check and records audit. Quarantine uploads uncompleted after 24h are swept; failed scans after 7 days; orphan promoted objects after 7 days and two reference scans. Reconciliation proves reference absence before deleting. Approved retention settings from DATA_ACCESS_BOUNDARIES.md govern child work and financial records; backup expiry is disclosed and restoration replays deletion tombstones before reopening service.

Verification: family/teacher/student ID guessing, forged purpose, MIME spoofing, oversized upload, ZIP traversal/bomb, post-scan overwrite, failed scan, stale presign, object deletion/retry, orphan race and restored deleted records.

Exact limits: 1 MiB = 1,048,576 bytes; per student file 26,214,400 bytes and per submission all files combined 104,857,600 bytes. Check the total under the submission transaction so concurrent attachments cannot exceed it.
