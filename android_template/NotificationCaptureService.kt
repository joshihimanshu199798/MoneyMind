package com.example.moneymind

import android.app.Notification
import android.content.Intent
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification

class NotificationCaptureService : NotificationListenerService() {
    override fun onNotificationPosted(sbn: StatusBarNotification) {
        val pkg = sbn.packageName ?: return
        val hints = listOf("paytm", "phonepe", "google.android.apps.nbu.paisa.user", "bhim", "bank", "sbi", "hdfc", "icici", "axis", "kotak", "amazon")
        if (hints.none { pkg.contains(it, ignoreCase = true) }) return
        val extras = sbn.notification.extras ?: return
        val title = extras.getCharSequence(Notification.EXTRA_TITLE)?.toString().orEmpty()
        val body = extras.getCharSequence(Notification.EXTRA_TEXT)?.toString().orEmpty()
        val message = "$title $body".trim()
        if (message.isBlank()) return
        val money = Regex("(?i)(₹|rs\\.?|inr)\\s*[0-9,]+|[0-9,]+\\s*(₹|rs\\.?|inr)").containsMatchIn(message)
        val txn = Regex("(?i)debited|credited|paid|received|sent|spent|refund|transaction|payment").containsMatchIn(message)
        if (!money || !txn) return
        sendBroadcast(Intent("com.example.moneymind.PAYMENT_MESSAGE").setPackage(applicationContext.packageName)
            .putExtra("text", message).putExtra("source", "notification:$pkg"))
    }
}