class NotificationSender:
    def __init__(self, settings): self.settings=settings
    def send(self, channel, recipients, subject, body):
        return {"status": "dry_run", "channel": channel, "recipients": recipients, "subject": subject}
