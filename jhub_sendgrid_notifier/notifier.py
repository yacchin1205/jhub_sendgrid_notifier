from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Mail, From, To
from jupyterhub.notifier import Notifier
from traitlets import Unicode


class SendGridNotifier(Notifier):
    """SendGrid Notifier

    This notifier sends notifications using SendGrid
    """

    api_key = Unicode(
        config=True,
        help="""
        The API key of SendGrid
        """
    )

    from_mail = Unicode(
        config=True,
        help="""
        E-mail address for From field
        """
    )

    async def notify(self, handler, to, title, body):
        if not self.api_key:
            self.log.error("The API key is not set")
            return
        if not self.from_mail:
            self.log.error("E-mail address for From field is not set")
            return
        sg = SendGridAPIClient(api_key=self.api_key)
        from_email = From(self.from_mail)
        content = Content("text/plain", body)
        for to_user in to:
            to_email = To(to_user.mail_address)
            mail = Mail(from_email, to_email, title, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            self.log.info("Processed: %s, %d, %r" % (to_user.mail_address,
                                                     response.status_code,
                                                     response.body))
