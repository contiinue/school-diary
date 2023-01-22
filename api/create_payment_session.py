import stripe
from dataclasses import dataclass

from django.urls import reverse_lazy
from schooldiary.settings import STRIPE_SECRET_KEY, PRICE_SCHOOL_MOTH, BASE_URL

stripe.api_key = STRIPE_SECRET_KEY


@dataclass
class PaymentData:
    count_month: int
    price: int


def _get_data_for_payment(month) -> PaymentData:
    return PaymentData(count_month=month, price=month * PRICE_SCHOOL_MOTH * 100)


def create_session(month: int, school_id: int) -> stripe.checkout.Session:
    data = _get_data_for_payment(month)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "rub",
                    "unit_amount": data.price,
                    "product_data": {
                        "name": "Лицензия на услуги платформы",
                    },
                },
                "quantity": data.count_month,
            },
        ],
        payment_intent_data={
            "metadata": {"school_id": school_id, "count_month": data.count_month}
        },
        mode="payment",
        success_url=BASE_URL + reverse_lazy("success-payment"),
        cancel_url=BASE_URL + reverse_lazy("cansel-payment"),
    )
    return checkout_session
