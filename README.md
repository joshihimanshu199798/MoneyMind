# MoneyMind
Standalone Flutter Android expense manager. Local SQLite storage, income/expense dashboard, categories, budgets, duplicate suppression and CSV export.
## Build
GitHub Actions runs `flutter create --platforms=android .`, dependency resolution, analyzer, tests and release APK build. Download the APK from Actions artifacts after a successful run.
## Privacy and scanning status
Transaction records are stored in app-private SQLite. CSV leaves the app only when explicitly shared. Notification capture requires explicit Android Notification Access permission. This repository is a starter and notification ingestion needs device validation. SMS permissions are not requested; SMS access is restricted by Google Play policies. Never enter banking PINs or OTPs in this app.
