# UI design system

Use a single token vocabulary for color, spacing, typography, radius, focus and responsive breakpoints. Base spacing4px, comfortable touch targets >=44px where practical, default body16px, readable line length and consistent heading scale. shadcn primitives are owned in packages/ui and wrap accessible behavior without replacing semantics. Components expose variants and typed props, never role authority.

Shared primitives include Button, Input, Select, Checkbox, Textarea, FormField, Dialog, Alert, Toast, Tabs, Card, Badge, Skeleton, EmptyState and DataTable. Domain components include ScheduleView, FileUpload, LessonBlockRenderer and ProgressSummary with surface-safe inputs. Finance-specific modules live only in parent/admin features. Course experience follows Learn → Attend/Watch → Try → Build → Submit → Review/Reflect. Every data component defines loading/empty/error states and responsive behavior before review; use story/interaction fixtures where useful, no duplicated role-specific forms with differing validation.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
