from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Product, Baho


User = get_user_model()


class ProductViewSetAPITest(APITestCase):

    def setUp(self):
        # Staff user — yozish huquqi bo'lishi kerak
        self.staff_user = User.objects.create_user(
            username="staff",
            password="staff12345",
            is_staff=True
        )

        # Oddiy user — faqat ko'rish huquqi
        self.normal_user = User.objects.create_user(
            username="normal",
            password="normal12345",
            is_staff=False
        )

        self.category = Category.objects.create(
            nomi="Elektronika"
        )

        self.product1 = Product.objects.create(
            nomi="Telefon",
            izoh="Smartfon",
            narxi=Decimal("1000.00"),
            category=self.category,
            ombor=10
        )

        self.product2 = Product.objects.create(
            nomi="Noutbuk",
            izoh="Kompyuter",
            narxi=Decimal("2000.00"),
            category=self.category,
            ombor=5
        )

        self.product3 = Product.objects.create(
            nomi="Zaryadnik",
            izoh="Telefon uchun",
            narxi=Decimal("50.00"),
            category=self.category,
            ombor=20
        )

        # Router'da basename='product' deb hisoblayapmiz
        self.list_url = reverse("product-list")

        self.detail_url = reverse(
            "product-detail",
            kwargs={"pk": self.product1.pk}
        )

        self.top_rating_url = reverse(
            "product-yuqori-reyting"
        )

        self.average_rating_url = reverse(
            "product-ortacha-reyting",
            kwargs={"pk": self.product1.pk}
        )

    # =========================================
    # LIST — MAHSULOTLAR RO'YXATI
    # =========================================

    def test_user_can_view_product_list(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_staff_can_view_product_list(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_product_list_pagination(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # CustomPagination page_size = 3
        self.assertEqual(
            len(response.data["results"]),
            3
        )

    # =========================================
    # CATEGORY FILTER
    # =========================================

    def test_filter_products_by_category(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(
            self.list_url,
            {"category": self.category.pk}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data["results"]),
            3
        )

    # =========================================
    # SEARCH
    # =========================================

    def test_search_products_by_name(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(
            self.list_url,
            {"search": "Telefon"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        names = [
            product["nomi"]
            for product in response.data["results"]
        ]

        self.assertIn("Telefon", names)

    # =========================================
    # RETRIEVE — BITTA MAHSULOT
    # =========================================

    def test_user_can_view_product_detail(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("product", response.data)
        self.assertIn("related_products", response.data)

        self.assertEqual(
            response.data["product"]["nomi"],
            "Telefon"
        )

    def test_related_products_are_returned(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        related_products = response.data["related_products"]

        # Shu kategoriyadagi boshqa 2 ta mahsulot
        self.assertEqual(
            len(related_products),
            2
        )

        related_names = [
            product["nomi"]
            for product in related_products
        ]

        self.assertNotIn("Telefon", related_names)

    # =========================================
    # PERMISSIONS — ODDIY USER
    # =========================================

    def test_normal_user_cannot_create_product(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.post(
            self.list_url,
            {
                "nomi": "Planshet",
                "izoh": "Yangi planshet",
                "narxi": "500.00",
                "category": self.category.pk,
                "ombor": 4
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_normal_user_cannot_update_product(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.patch(
            self.detail_url,
            {"nomi": "O'zgartirilgan telefon"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.product1.refresh_from_db()

        self.assertEqual(
            self.product1.nomi,
            "Telefon"
        )

    def test_normal_user_cannot_delete_product(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            Product.objects.filter(
                pk=self.product1.pk
            ).exists()
        )

    # =========================================
    # PERMISSIONS — STAFF USER
    # =========================================

    def test_staff_can_create_product(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.post(
            self.list_url,
            {
                "nomi": "Planshet",
                "izoh": "Yangi planshet",
                "narxi": "500.00",
                "category": self.category.pk,
                "ombor": 4
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Product.objects.filter(
                nomi="Planshet"
            ).exists()
        )

    def test_staff_can_update_product(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.patch(
            self.detail_url,
            {"nomi": "Yangi telefon"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.product1.refresh_from_db()

        self.assertEqual(
            self.product1.nomi,
            "Yangi telefon"
        )

    def test_staff_can_delete_product(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Product.objects.filter(
                pk=self.product1.pk
            ).exists()
        )

    # =========================================
    # YUQORI REYTING
    # =========================================

    def test_yuqori_reyting_returns_products(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(self.top_rating_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # ViewSet'da [:2] ishlatilgan
        self.assertLessEqual(
            len(response.data),
            2
        )

    # =========================================
    # ORTACHA REYTING
    # =========================================

    def test_ortacha_reyting_without_ratings(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(
            self.average_rating_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data,
            {"orta_baho": "Baholar yoq"}
        )