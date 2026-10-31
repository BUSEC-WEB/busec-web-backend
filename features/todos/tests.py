from rest_framework.test import APITestCase  # pyright: ignore[reportMissingTypeStubs]


class TodoTests(APITestCase):
    def test_create_list_update_delete(self):
        todo = self.client.post(
            "/api/todos/", {"title": "Ship it"}, format="json"
        ).json()
        self.assertEqual(todo["title"], "Ship it")
        self.assertFalse(todo["done"])

        self.assertIn(todo, self.client.get("/api/todos/").json())

        r = self.client.patch(
            f"/api/todos/{todo['id']}/", {"done": True}, format="json"
        )
        self.assertTrue(r.json()["done"])

        self.assertEqual(
            self.client.delete(f"/api/todos/{todo['id']}/").status_code, 204
        )
        self.assertEqual(self.client.get(f"/api/todos/{todo['id']}/").status_code, 404)
