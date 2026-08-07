from django.test import TestCase
from django.urls import reverse

from .models import User


class ProfileLinkTests(TestCase):
    def test_guest_sees_login_link_on_home(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, reverse("login"))

    def test_logged_in_user_sees_profile_link_on_home(self):
        user = User.objects.create(
            first_name="Test",
            middle_name="",
            last_name="User",
            username="testuser",
            email="test@example.com",
            phone="1234567890",
            password="secret123",
        )
        session = self.client.session
        session["user_id"] = user.id
        session.save()

        response = self.client.get(reverse("home"))

        self.assertContains(response, reverse("profile"))
        self.assertNotContains(response, reverse("login"))
