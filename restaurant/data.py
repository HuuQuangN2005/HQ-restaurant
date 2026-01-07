import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant.settings")

django.setup()

from products.models import Category, Ingredient, Food

# Category
c1, _ = Category.objects.get_or_create(
    name="Món Mới",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674690/restaurant/categories/pipzrn8vsyhkk2l5udjy.jpg",
)

c2, _ = Category.objects.get_or_create(
    name="Món Chay",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767771413/restaurant/categories/bam3igp08pp0dwhrobd6.jpg",
)

c3, _ = Category.objects.get_or_create(
    name="Điểm Tâm",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767771608/restaurant/categories/igyqtexlilcl5heyscht.jpg",
)

c4, _ = Category.objects.get_or_create(
    name="Bánh Bao",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767771774/restaurant/categories/goxg9nrhhhhl3cxdpnjm.jpg",
)

c5, _ = Category.objects.get_or_create(
    name="Bánh Cuốn",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767771977/restaurant/categories/sepqisasow9qqb4al8nj.jpg",
)

c6, _ = Category.objects.get_or_create(
    name="Dimsum",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767772107/restaurant/categories/xaqnwz85eihpoeteq4ej.jpg",
)

c7, _ = Category.objects.get_or_create(
    name="Cơm",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767773923/restaurant/categories/hy5m6w0aveqz7jwa6c8r.jpg",
)

c8, _ = Category.objects.get_or_create(
    name="Hủ tiếu - Mì",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767772372/restaurant/categories/kgel640sf9kmrbtegysz.jpg",
)

c9, _ = Category.objects.get_or_create(
    name="Cháo",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767772491/restaurant/categories/mfmwi76y2dzbawdllfa8.jpg",
)

c10, _ = Category.objects.get_or_create(
    name="Canh - Súp",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767772592/restaurant/categories/h3qjyqn6devahrgqbxjh.jpg",
)

c11, _ = Category.objects.get_or_create(
    name="Đậu Hũ",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767772673/restaurant/categories/keyre4qbeg0iqz3muide.jpg",
)

c12, _ = Category.objects.get_or_create(
    name="Heo",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767772769/restaurant/categories/nthzflruhx3hlcbv6pyc.jpg",
)

c13, _ = Category.objects.get_or_create(
    name="Vịt & Gà",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767772883/restaurant/categories/nko0xjuafxfqfbc6xccv.jpg",
)

c14, _ = Category.objects.get_or_create(
    name="Hải Sản",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767773217/restaurant/categories/fjjbvnotbr92sajm8ujm.jpg",
)

c15, _ = Category.objects.get_or_create(
    name="Tráng Miệng",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767773251/restaurant/categories/s7iun0bdzrduxeui7nnt.jpg",
)

c16, _ = Category.objects.get_or_create(
    name="Thức Uống",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767773279/restaurant/categories/kbegoces8altfqoxxo3e.jpg",
)

# Ingredient
ingredients_list = [
    "Đường",
    "Thịt bò",
    "Thịt heo",
    "Thịt gà",
    "Thịt cá",
    "Gạo",
    "Muối",
    "Chanh",
    "Chanh dây",
    "Tắc",
    "Bột ngọt",
    "Nui",
    "Trứng gà",
    "Trứng vịt",
    "Rau muống",
    "Cải thìa",
    "Hành tây",
    "Hành lá",
    "Tỏi",
    "Ớt",
    "Gừng",
    "Sả",
    "Riềng",
    "Tiêu",
    "Nước mắm",
    "Dầu ăn",
    "Dầu hào",
    "Tương ớt",
    "Tương cà",
    "Bột năng",
    "Bột mì",
    "Bột chiên xù",
    "Bột bắp",
    "Sữa tươi",
    "Sữa đặc",
    "Bơ",
    "Phô mai",
    "Nấm mèo",
    "Nấm hương",
    "Nấm kim châm",
    "Cà rốt",
    "Khoai tây",
    "Khoai lang",
    "Bí đỏ",
    "Bí xanh",
    "Dưa leo",
    "Cà chua",
    "Giá đỗ",
    "Đậu hũ",
    "Đậu phộng",
    "Mè trắng",
    "Mè đen",
    "Mắm tôm",
    "Mắm nêm",
    "Giấm",
    "Rượu mai quế lộ",
    "Ngũ vị hương",
    "Bột nghệ",
    "Bột quế",
    "Hồi",
    "Thảo quả",
    "Tôm khô",
    "Mực khô",
    "Lạp xưởng",
    "Thịt xông khói",
    "Xúc xích",
    "Bún tươi",
    "Phở tươi",
    "Hủ tiếu",
    "Mì gói",
    "Rau cải xanh",
    "Rau mồng tơi",
    "Rau ngót",
    "Khổ qua",
    "Đậu bắp",
    "Cần tây",
    "Tàu hủ ky",
    "Măng chua",
    "Măng tươi",
    "Hạt nêm",
    "Mật ong",
    "Siro bắp",
    "Bột cacao",
    "Vani",
    "Baking soda",
    "Men nở",
    "Cốt dừa",
    "Lá dứa",
    "Lá chanh",
    "Rau quế",
    "Ngò rí",
    "Ngò gai",
    "Húng quế",
    "Húng lủi",
    "Rau răm",
    "Thì là",
    "Tía tô",
    "Kinh giới",
    "Xà lách",
    "Bông cải xanh",
]

for name in ingredients_list:
    obj, created = Ingredient.objects.get_or_create(name=name)



