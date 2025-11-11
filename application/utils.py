from django.core.mail import send_mail
from django.conf import settings
from application.models import EmailTemplate


def get_email_template(name, default_subject, default_body):
    """Fetch template from DB or fallback to default."""
    try:
        template = EmailTemplate.objects.get(name=name)
        return template.subject, template.body
    except EmailTemplate.DoesNotExist:
        return default_subject, default_body


def send_welcome_email(user):
    subject, body = get_email_template(
        "welcome_email",
        "Welcome to EzfinTutor!",
        "Hi {name},\n\nWelcome to EzfinTutor! Your account has been created successfully.\n\nBest regards,\nEzfinTutor Team"
    )
    message = body.format(name=user.get_full_name() or user.username)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_enrollment_email(user, course_name):
    subject, body = get_email_template(
        "enrollment_email",
        "Enrollment Confirmation",
        "Hi {name},\n\nYou have been successfully enrolled in the course: {course_name}.\n\nBest wishes,\nEzfinTutor Team"
    )
    message = body.format(name=user.get_full_name() or user.username, course_name=course_name)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_unenrollment_email(user, course_name, reason=""):
    subject, body = get_email_template(
        "unenrollment_email",
        "Course Unenrollment Notification",
        "Hi {name},\n\nYou have been unenrolled from the course: {course_name}.\n{reason}\n\nBest regards,\nEzfinTutor Team"
    )
    message = body.format(
        name=user.get_full_name() or user.username,
        course_name=course_name,
        reason=f"Reason: {reason}" if reason else ""
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_payment_email(user, amount_paid, batch_name):
    subject, body = get_email_template(
        "payment_email",
        "Payment Confirmation",
        "Hi {name},\n\nYour payment has been successfully processed.\n\nAmount Paid: ₹{amount_paid}\nBatch: {batch_name}\n\nThank you!\nEzfinTutor Team"
    )
    message = body.format(
        name=user.get_full_name() or user.username,
        amount_paid=amount_paid,
        batch_name=batch_name
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
