from pathlib import Path
import re

PACKAGE = "in.moneymind.expenses"
PACKAGE_PATH = Path(*PACKAGE.split("."))
main = Path("android/app/src/main")
manifest = main / "AndroidManifest.xml"
gradle = Path("android/app/build.gradle.kts")

# Set the Android application identity to the package registered in Developer Console.
g = gradle.read_text(encoding="utf-8")
g = re.sub(r'(?m)^\s*namespace\s*=\s*"[^"]+"', f'    namespace = "{PACKAGE}"', g, count=1)
g = re.sub(r'(?m)^\s*applicationId\s*=\s*"[^"]+"', f'        applicationId = "{PACKAGE}"', g, count=1)

# Configure the persistent release key only when CI has supplied key.properties.
props = Path("android/key.properties")
if props.exists():
    if 'import java.util.Properties' not in g:
        g = "import java.util.Properties\nimport java.io.FileInputStream\n\n" + g
    if "val keystoreProperties = Properties()" not in g:
        anchor = "android {"
        setup = """val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

"""
        g = g.replace(anchor, setup + anchor, 1)
    if 'create("moneymindRelease")' not in g:
        g = g.replace("    buildTypes {", """    signingConfigs {
        create("moneymindRelease") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
        }
    }
    buildTypes {""", 1)
    # Apply release signing without affecting debug builds.
    g = re.sub(
        r'(?m)(getByName\("release"\)\s*\{)',
        r'\1\n            signingConfig = signingConfigs.getByName("moneymindRelease")',
        g,
        count=1,
    )
gradle.write_text(g, encoding="utf-8")

# Ensure the notification-listener service is registered once.
m = manifest.read_text(encoding="utf-8")
if "NotificationCaptureService" not in m:
    m = m.replace("</application>", """<service
            android:name=".NotificationCaptureService"
            android:label="MoneyMind payment notification access"
            android:permission="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE"
            android:exported="true">
            <intent-filter>
                <action android:name="android.service.notification.NotificationListenerService" />
            </intent-filter>
        </service>
    </application>""")
manifest.write_text(m, encoding="utf-8")

# Replace Flutter's generated default activity with the app's native bridge in the correct package.
kotlin_root = main / "kotlin"
old_default = kotlin_root / "com" / "example" / "moneymind"
if old_default.exists():
    for p in old_default.glob("*.kt"):
        p.unlink()
    for p in sorted(old_default.parents, key=lambda x: len(x.parts), reverse=True):
        if p == kotlin_root:
            break
        try:
            p.rmdir()
        except OSError:
            pass
kotlin = kotlin_root / PACKAGE_PATH
kotlin.mkdir(parents=True, exist_ok=True)
for name in ("MainActivity.kt", "NotificationCaptureService.kt"):
    source = Path("android_template") / name
    content = source.read_text(encoding="utf-8")
    content = content.replace("package com.example.moneymind", f"package {PACKAGE}")
    content = content.replace("com.example.moneymind.PAYMENT_MESSAGE", f"{PACKAGE}.PAYMENT_MESSAGE")
    (kotlin / name).write_text(content, encoding="utf-8")
