import { Image, ScrollView, Text, TouchableOpacity, View } from "react-native";
import HomeStyle from "../styles/HomeStyle";
import { useEffect, useState } from "react";
import { useNavigation } from "@react-navigation/native";
import Apis, { endpoints } from "../utils/Apis";

const CategoryFoodsSection = ({ category }) => {
    const [foods, setFoods] = useState([]);
    const nav = useNavigation();
    const loadFoodsPreview = async () => {
        try {
            let res = await Apis.get(
                `${endpoints['foods']}?category=${category.uuid}&page_size=3`
            );
            setFoods(res.data.results);
        } catch (ex) {
            console.error("Loi: ", ex);
        }
    };

    useEffect(() => {
        loadFoodsPreview();
    }, [category.uuid])

    return (
        <View style={HomeStyle.ProductContainer}>
            <View style={HomeStyle.ProductHeader}>
                <Text style={HomeStyle.ProductTitle}>
                    {category.name}
                </Text>

                <TouchableOpacity onPress={() => nav.navigate("Search", {categoryId: category.uuid})}>
                    <Text style={HomeStyle.ProductViewAll}>
                        Xem tất cả
                    </Text>
                </TouchableOpacity>
            </View>

            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ paddingHorizontal: 10 }} >
                {foods?.slice(0,3).map(item => (
                    <TouchableOpacity key={item.uuid} activeOpacity={0.7} onPress={() => nav.navigate("FoodDetail", { foodUuid: item.uuid })}>
                        <View style={HomeStyle.ProductCard}>
                            <Image source={{ uri: item.image }} style={HomeStyle.ProductImage} />
                            <Text numberOfLines={1} style={HomeStyle.ProductName}>
                                {item.name}
                            </Text>
                            <Text style={HomeStyle.ProductPrice}>
                                {Number(item.price).toLocaleString("vi-VN")}đ
                            </Text>
                            <View style={HomeStyle.AddToCartBtn}>
                                <Text style={HomeStyle.ShowDetails}>
                                    Xem chi tiết
                                </Text>
                            </View>
                        </View>
                    </TouchableOpacity>
                ))}
            </ScrollView>
        </View>
    );
};

export default CategoryFoodsSection;