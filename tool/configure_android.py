from pathlib import Path

main = Path("android/app/src/main")
manifest = main / "AndroidManifest.xml"
text = manifest.read_text(encoding="utf-8")
if "NotificationCaptureService" not in text:
    text = text.replace("</application>", """<service
            android:name=".NotificationCaptureService"
            android:label="MoneyMind payment notification access"
            android:permission="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE"
            android:exported="true">
            <intent-filter>
                <action android:name="android.service.notification.NotificationListenerService" />
            </intent-filter>
        </service>
    </application>""")
    manifest.write_text(text, encoding="utf-8")
kotlin = main / "kotlin" / "com" / "example" / "moneymind"
kotlin.mkdir(parents=True, exist_ok=True)
(kotlin / "MainActivity.kt").write_text(Path("android_template/MainActivity.kt").read_text(encoding="utf-8"), encoding="utf-8")
(kotlin / "NotificationCaptureService.kt").write_text(Path("android_template/NotificationCaptureService.kt").read_text(encoding="utf-8"), encoding="utf-8")
