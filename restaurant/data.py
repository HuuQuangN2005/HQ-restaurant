import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant.settings")

django.setup()

from products.models import Category, Ingredient

# Category
c2, _ = Category.objects.get_or_create(
    name="Cơm",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674217/restaurant/categories/lyvppo7mvc5f9dofs94c.jpg",
)

c3, _ = Category.objects.get_or_create(
    name="Món chay",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674313/restaurant/categories/xedsoudlkiwsrdibtd4k.jpg",
)

c4, _ = Category.objects.get_or_create(
    name="Món nướng",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674392/restaurant/categories/dajsooaadezphlfopibf.jpg",
)

c5, _ = Category.objects.get_or_create(
    name="Món chiên",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674512/restaurant/categories/mroprrevzoum44ps8p8x.jpg",
)

c6, _ = Category.objects.get_or_create(
    name="Món xào",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674611/restaurant/categories/dxb6lq7op4wnzfzflnxt.jpg",
)
c7, _ = Category.objects.get_or_create(
    name="Món hấp",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674690/restaurant/categories/pipzrn8vsyhkk2l5udjy.jpg",
)

c1, _ = Category.objects.get_or_create(
    name="Lẩu",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674759/restaurant/categories/mag8ovpucsbklhkjtiul.jpg",
)

c8, _ = Category.objects.get_or_create(
    name="Món súp",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674833/restaurant/categories/ilh6rj1sgiznckefmnmr.png",
)

c9, _ = Category.objects.get_or_create(
    name="Tráng miệng",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674899/restaurant/categories/iucjlusxppeerpcgaazg.jpg",
)

c10, _ = Category.objects.get_or_create(
    name="Đồ uống",
    image="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674966/restaurant/categories/s4nsumaegqhviszjcphf.jpg",
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
