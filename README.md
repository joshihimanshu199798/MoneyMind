# MoneyMind
Standalone Flutter Android expense manager. Local SQLite storage, income/expense dashboard, categories, budgets, duplicate suppression and CSV export.

## Privacy
MoneyMind does **not** read payment notifications, SMS, or other apps' notifications. All transactions must be added manually by the user. Transaction records are stored in app-private SQLite. CSV leaves the app only when the user explicitly shares an export. Never enter banking PINs or OTPs in this app.

## Build
GitHub Actions runs `flutter create --platforms=android .`, dependency resolution, analyzer, tests and release APK build. Download the APK from Actions artifacts after a successful run.
